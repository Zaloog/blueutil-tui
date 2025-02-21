from textual import work
from textual.app import App, ComposeResult

from textual.widgets import Footer, Header

from blueutil_tui.utils import get_blueutil_version
from blueutil_tui.widgets import DeviceTable


class BlueUtilApp(App):
    def on_mount(self):
        self.get_blueutil_version()

    def compose(self) -> ComposeResult:
        self.screen.title = "blueutil-tui"
        yield Header(icon="")
        yield DeviceTable()
        yield Footer()
        return super().compose()

    @work(thread=True)
    def get_blueutil_version(self):
        version = get_blueutil_version()
        self.call_from_thread(self.update_title, version)
        # self.screen.title += f" using blueutil v{version}"

    def update_title(self, version):
        self.screen.title += f" using blueutil v{version}"
