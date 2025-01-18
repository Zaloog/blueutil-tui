from blueutil_tui.app import BlueUtilApp
from blueutil_tui.utils import (
    check_blueutil_installation,
    # search_new_devices,
    # get_paired_devices,
)


def main() -> None:
    if not check_blueutil_installation():
        return
    # devices = search_new_devices()
    # for dev in devices:
    #     print(dev)

    app = BlueUtilApp()
    app.run(inline=True)
