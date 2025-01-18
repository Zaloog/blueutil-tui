import subprocess
import shutil
import json

from rich.console import Console

console = Console()


def check_blueutil_installation():
    if shutil.which("blueutil") is None:
        Console().print(
            '[blue]"blueutil"[/] was not found, please install with e.g. [blue]"brew install blueutil"[/] '
        )
        Console().print("or use another installation method from:")
        Console().print(
            "[blue underline]https://github.com/toy/blueutil?tab=readme-ov-file#installupdateuninstall[/] "
        )
        return False
    return True


def get_paired_devices():
    command = subprocess.run(
        args=["blueutil", "--paired", "--format", "json"],
        capture_output=True,
        text=True,
    )

    handle_returncodes(errorcode=command.returncode)

    if command.stdout:
        devices = command.stdout
        formatted_devices = format_device_string(device_string=devices)
        return formatted_devices


def format_device_string(device_string: str) -> list[dict[str, str | bool]]:
    json_dict = json.loads(device_string)
    # json_dict = remove_duplicate_entries(json_dict=json_dict)
    return json_dict


def remove_duplicate_entries(
    json_list: list[dict[str, str | bool]],
) -> list[dict[str, str | bool]]:
    updated_list = []
    addresses = []
    for device in json_list:
        if device["address"] not in addresses:
            updated_list.append(device)
            addresses.append(device["address"])
        else:
            ...
    return updated_list


def handle_returncodes(errorcode: int):
    match errorcode:
        case 0:
            return 0
        case 1:
            console.print("1: General failure")
            return 1
        case 64:
            console.print(
                "64: Wrong usage like missing or unexpected arguments, wrong parameters"
            )
            return 1
        case 69:
            console.print("69 Bluetooth or interface not available")
            return 1
        case 70:
            console.print("70 Internal error")
            return 1
        case 71:
            console.print("71 System error like shortage of memory")
            return 1
        case 75:
            console.print("75 Timeout error")
            return 1
        case _:
            console.print("No standart blueutil error")
            return 1


async def connect_device(device_address: str):
    try:
        command = subprocess.run(
            args=["blueutil", "--connect", device_address],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return 1

    returncode = handle_returncodes(errorcode=command.returncode)

    return returncode


async def disconnect_device(device_address: str):
    try:
        command = subprocess.run(
            args=["blueutil", "--disconnect", device_address],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return 1

    returncode = handle_returncodes(errorcode=command.returncode)

    return returncode
