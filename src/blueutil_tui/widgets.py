from textual import on, work
from textual.widgets import DataTable
from textual.binding import Binding

from blueutil_tui.utils import (
    get_paired_devices,
    connect_device,
    disconnect_device,
    device_is_connected,
)
from blueutil_tui.constants import GREEN_RED_DICT


class OverViewTable(DataTable):
    BINDINGS = [
        Binding("j, down", "cursor_down", "Down", key_display="j/↓"),
        Binding("k, up", "cursor_up", "Up", key_display="k/↑"),
        Binding("space", "select_cursor", "Connect/Disconnect"),
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
    @work(thread=True)
    async def toggle_connection(self, event: DataTable.RowSelected):
        selected_address = event.row_key.value

        if await device_is_connected(device_address=selected_address):
            self.update_cell(
                row_key=selected_address, column_key="connection", value="updating..."
            )

            output = await disconnect_device(device_address=selected_address)
            if output == 0:
                self.update_cell(
                    row_key=selected_address,
                    column_key="connection",
                    value=":red_circle:",
                )
                self.notify("Disconnected", timeout=1)
            else:
                self.update_cell(
                    row_key=selected_address,
                    column_key="connection",
                    value=":green_circle:",
                )
                self.notify(
                    title="Error",
                    message="Please check if the device is nearby",
                    timeout=1,
                    severity="error",
                )
        else:
            self.update_cell(
                row_key=selected_address, column_key="connection", value="updating..."
            )
            output = await connect_device(device_address=selected_address)

            if output == 0:
                self.update_cell(
                    row_key=selected_address,
                    column_key="connection",
                    value=":green_circle:",
                )
                self.notify("Connected", timeout=1)
            else:
                self.update_cell(
                    row_key=selected_address,
                    column_key="connection",
                    value=":red_circle:",
                )
                self.notify(
                    title="Error",
                    message="Please check if the device is nearby",
                    timeout=1,
                    severity="error",
                )
