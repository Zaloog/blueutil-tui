from textual.app import App, ComposeResult

from textual.widgets import Footer

from blueutil_tui.widgets import OverViewTable


class BlueUtilApp(App):
    def compose(self) -> ComposeResult:
        yield OverViewTable()
        yield Footer()
        return super().compose()
