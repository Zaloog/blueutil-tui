from blueutil_tui.app import BlueUtilApp
from blueutil_tui.utils import check_blueutil_installation, get_paired_devices


def main() -> None:
    if not check_blueutil_installation():
        return
    devices = get_paired_devices()
    for dev in devices:
        print(dev)

    app = BlueUtilApp()
    app.run(inline=True)
