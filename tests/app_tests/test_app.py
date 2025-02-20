from blueutil_tui.app import BlueUtilApp


async def test_app(fp, test_device_output):
    fp.allow_unregistered = True
    fp.keep_last_process(True)

    fp.register(command=["blueutil", "--version"], stdout="2.11.0")
    fp.register(
        command=["blueutil", "--paired", "--format", "json"], stdout=test_device_output
    )

    app = BlueUtilApp()
    async with app.run_test() as pilot:
        assert ["blueutil", "--version"] in fp.calls
        assert ["blueutil", "--paired", "--format", "json"] in fp.calls

        assert pilot.app.screen.title == "blueutil-tui using blueutil v2.11.0"
        assert pilot.app.focused.row_count == 3

        assert pilot.app.focused.cursor_row == 0

        await pilot.press(*"jj")
        assert pilot.app.focused.cursor_row == 2

        await pilot.press("k")
        assert pilot.app.focused.cursor_row == 1
