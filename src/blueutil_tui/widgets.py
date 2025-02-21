from textual import on, work
from textual.reactive import reactive
from textual.widgets import DataTable, Label
from textual.binding import Binding

from blueutil_tui.utils import (
    get_paired_devices,
    connect_device,
    disconnect_device,
    device_is_connected,
    search_new_devices,
    pair_device,
    unpair_device,
)


class DeviceTable(DataTable):
    BINDINGS = [
        Binding("j, down", "cursor_down", "down", key_display="j/↓"),
        Binding("k, up", "cursor_up", "up", key_display="k/↑"),
        Binding("space", "select_cursor", "dis/connect", key_display="space/enter"),
        Binding("r", "update_devices", "refresh"),
        Binding("s", "display_new_devices", "search"),
        Binding("p", "toggle_pair_device", "un/pair"),
    ]

    search_timer: reactive[int] = reactive(4, init=False)

    def on_mount(self):
        self.show_header = True
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.timer = self.set_interval(1, self.update_time, pause=True)

        self.add_column(":electric_plug: Connection", key="connection")
        self.add_column(":handshake: Paired", key="paired")
        self.add_column(":five_o’clock: Last Access", key="last_access")
        self.add_column(":house: Address", key="address")

        self.action_update_devices()
        return super().on_mount()

    def action_update_devices(self):
        self.clear()
        devices = get_paired_devices()
        for device in devices:
            self.add_row(
                ":green_circle:" if device["connected"] else ":red_circle:",
                ":green_circle:" if device["paired"] else ":red_circle:",
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
                self.notify(
                    title="Success",
                    message=f"[blue]{self.rows[selected_address].label}[/] disconnected",
                    timeout=1.5,
                )
            else:
                self.update_cell(
                    row_key=selected_address,
                    column_key="connection",
                    value=":green_circle:",
                )
                self.notify(
                    title="Error",
                    message=f"Please check [blue]{self.rows[selected_address].label}[/] if the device is nearby",
                    timeout=1.5,
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
                self.notify(
                    title="Success",
                    message=f"[blue]{self.rows[selected_address].label}[/] connected",
                    timeout=1.5,
                )
            else:
                self.update_cell(
                    row_key=selected_address,
                    column_key="connection",
                    value=":red_circle:",
                )
                self.notify(
                    title="Error",
                    message=f"Please check if [blue]{self.rows[selected_address].label}[/] is nearby",
                    timeout=1.5,
                    severity="error",
                )

    @work(thread=True, exclusive=True, name="look-for-devices")
    async def action_display_new_devices(self):
        self.app.call_from_thread(callback=self.show_search_label)
        self.app.call_from_thread(callback=self.start_timer)
        new_devices = await search_new_devices()

        self.app.call_from_thread(
            callback=lambda: self.update_rows(new_devices=new_devices)
        )

    def start_timer(self):
        self.search_timer = 4
        self.timer.resume()

    async def update_time(self):
        if self.search_timer == 0:
            self.timer.reset()
            await self.hide_search_label()
        else:
            self.search_timer -= 1

    def watch_search_timer(self):
        self.app.query_exactly_one("#label-search", Label).update(
            f"Searching... {self.search_timer}s"
        )

    async def show_search_label(self):
        if self.app.query(Label):
            return
        await self.app.mount(Label("Searching... 4s", id="label-search"))

    async def hide_search_label(self):
        if self.app.query(Label):
            await self.app.query_exactly_one("#label-search", Label).remove()

    def update_rows(self, new_devices: list[dict]):
        for device in new_devices:
            if device["address"] in [key.value for key in self.rows.keys()]:
                continue

            self.add_row(
                ":green_circle:" if device["connected"] else ":red_circle:",
                ":green_circle:" if device["paired"] else ":red_circle:",
                device["recentAccessDate"],
                device["address"],
                key=device["address"],
                label=f"[blue]{device['name']}[/]",
            )

    @work(thread=True)
    async def action_toggle_pair_device(self):
        selected_address = self.get_row_at(self.cursor_row)[-1]
        paired = True if "green" in self.get_row_at(self.cursor_row)[1] else False

        if paired:
            self.update_cell(
                row_key=selected_address, column_key="paired", value="updating..."
            )

            output = await unpair_device(device_address=selected_address)
            if output == 0:
                self.update_cell(
                    row_key=selected_address,
                    column_key="paired",
                    value=":red_circle:",
                )
                self.notify(
                    title="Success",
                    message=f"[blue]{self.rows[selected_address].label}[/] unpaired",
                    timeout=1.5,
                )
            else:
                self.update_cell(
                    row_key=selected_address,
                    column_key="paired",
                    value=":green_circle:",
                )
                self.notify(
                    title="Error",
                    message=f"Please check [blue]{self.rows[selected_address].label}[/] if the device is nearby",
                    timeout=1.5,
                    severity="error",
                )
        else:
            self.update_cell(
                row_key=selected_address, column_key="paired", value="updating..."
            )
            output = await pair_device(device_address=selected_address)

            if output == 0:
                self.update_cell(
                    row_key=selected_address,
                    column_key="paired",
                    value=":green_circle:",
                )
                self.notify(
                    title="Success",
                    message=f"[blue]{self.rows[selected_address].label}[/] pairing",
                    timeout=1.5,
                )
            else:
                self.update_cell(
                    row_key=selected_address,
                    column_key="paired",
                    value=":red_circle:",
                )
                self.notify(
                    title="Error",
                    message=f"Please check if [blue]{self.rows[selected_address].label}[/] is nearby",
                    timeout=1.5,
                    severity="error",
                )
