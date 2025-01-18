from textual import on
from textual.widgets import DataTable
from textual.binding import Binding

from blueutil_tui.utils import get_paired_devices
from blueutil_tui.constants import GREEN_RED_DICT


class OverViewTable(DataTable):
    BINDINGS = [
        Binding("j", "cursor_down", "Down"),
        Binding("k", "cursor_up", "Up"),
        Binding("space", "select_cursor", "Toggle Connection"),
    ]

    def on_mount(self):
        self.show_header = True
        self.cursor_type = "row"
        self.zebra_stripes = True

        self.add_column(":electric_plug: Connection", key="connection")
        self.add_column(":handshake: Paired", key="paired")
        self.add_column(":five_o’clock: Last Access", key="last_access")
        self.add_column(":house: Address", key="address")

        self.update_devices()
        return super().on_mount()

    def update_devices(self):
        devices = get_paired_devices()
        for device in devices:
            self.add_row(
                GREEN_RED_DICT[device["connected"]],
                GREEN_RED_DICT[device["paired"]],
                device["recentAccessDate"],
                device["address"],
                key=device["address"],
                label=f"[blue]{device['name']}[/]",
            )

    @on(DataTable.RowSelected)
    def toggle_connection(self, event: DataTable.RowSelected):
        selected_address = event.row_key.value
        self.notify(selected_address, timeout=1)
