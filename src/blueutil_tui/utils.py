import subprocess
import shutil
import json

from rich.console import Console

console = Console(stderr=True)
TIMEOUT = 8


def check_blueutil_installation():
    if shutil.which("blueutil") is None:
        console.print(
            '[blue]"blueutil"[/] was not found, please install with e.g. [blue]"brew install blueutil"[/]'
        )
        console.print("or use another installation method from:")
        console.print(
            "[blue underline]https://github.com/toy/blueutil?tab=readme-ov-file#installupdateuninstall[/]"
        )
        return False
    return True


def get_blueutil_version():
    command = subprocess.run(
        ["blueutil", "--version"],
        capture_output=True,
        text=True,
    )
    return command.stdout.strip()


def get_paired_devices() -> list[dict[str, str | bool]] | None:
    command = subprocess.run(
        ["blueutil", "--paired", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )

    handle_returncodes(errorcode=command.returncode)

    if command.stdout:
        devices = command.stdout
        formatted_devices = format_device_string(device_string=devices)
        return formatted_devices
    return []


def format_device_string(device_string: str) -> list[dict[str, str | bool]]:
    json_dict = json.loads(device_string)
    # json_dict = remove_duplicate_entries(json_dict=json_dict)
    return json_dict


# def remove_duplicate_entries(
#     json_list: list[dict[str, str | bool]],
# ) -> list[dict[str, str | bool]]:
#     updated_list = []
#     addresses = []
#     for device in json_list:
#         if device["address"] not in addresses:
#             updated_list.append(device)
#             addresses.append(device["address"])
#         else:
#             ...
#     return updated_list


def handle_returncodes(errorcode: int) -> int:
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


async def device_is_connected(device_address: str) -> bool:
    try:
        command = subprocess.run(
            ["blueutil", "--is-connected", device_address],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired as e:
        raise e

    return bool(int(command.stdout))


async def connect_device(device_address: str):
    try:
        command = subprocess.run(
            ["blueutil", "--connect", device_address],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1

    returncode = handle_returncodes(errorcode=command.returncode)

    return returncode


async def disconnect_device(device_address: str):
    try:
        command = subprocess.run(
            ["blueutil", "--disconnect", device_address],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1

    returncode = handle_returncodes(errorcode=command.returncode)

    return returncode


async def search_new_devices():
    command = subprocess.run(
        ["blueutil", "--inquiry", "4", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )

    handle_returncodes(errorcode=command.returncode)

    if command.stdout:
        devices = command.stdout
        formatted_devices = format_device_string(device_string=devices)
        return formatted_devices


async def pair_device(device_address: str) -> int:
    try:
        command = subprocess.run(
            ["blueutil", "--pair", device_address],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1

    returncode = handle_returncodes(errorcode=command.returncode)

    return returncode


async def unpair_device(device_address: str) -> int:
    try:
        command = subprocess.run(
            ["blueutil", "--unpair", device_address],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1

    returncode = handle_returncodes(errorcode=command.returncode)

    return returncode
