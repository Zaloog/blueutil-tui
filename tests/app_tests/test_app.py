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

        assert pilot.app.screen.title == "blueutil-tui using blueutil v2.11.0"
