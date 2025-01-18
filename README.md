<!-- Icons -->
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI-Server](https://img.shields.io/pypi/v/blueutil-tui.svg)](https://pypi.org/project/blueutil-tui/)
[![Pyversions](https://img.shields.io/pypi/pyversions/blueutil-tui.svg)](https://pypi.python.org/pypi/blueutil-tui)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/blueutil-tui)](https://pepy.tech/project/blueutil-tui)

# blueutil-tui

blueutil-tui is macos tui to connect bluetooth devices with the help of [blueutil].
Its written in python with the [textual] framework.

![preview](https://raw.githubusercontent.com/Zaloog/blueutil-tui/main/images/preview.png)

## Installation

You can install `blueutil-tui` with one of the following options:

```bash
# not recommended
pip install blueutil-tui
```

```bash
pipx install blueutil-tui
```

```bash
rye install blueutil-tui
```

```bash
uv tool install blueutil-tui
```
I recommend using [pipx], [rye] or [uv] to install CLI Tools into an isolated environment.


blueutil-tui requires [blueutil] to be installed on your system.
I recommend using [homebrew] for installation (Other ways can be found [here][blueutil_install]):

```bash
brew install blueutil
```
## Usage
`blueutil-tui` can be started with:

```bash
btui
```
Only the paired devices are shown. To search for more devices press `s`.
Refreshing the view with `r` removes the unpaired devices from the view again.

To close `blueutil-tui` press `ctrl+q`.

## Feedback and Issues
Feel free to reach out and share your feedback, or open an [Issue],
if something doesnt work as expected.
Also check the [Changelog] for new updates.

<!-- Repo Links -->
[Changelog]: https://github.com/Zaloog/blueutil-tui/blob/main/CHANGELOG.md
[Issue]: https://github.com/Zaloog/blueutil-tui/issues


<!-- external Links Python -->
[textual]: https://textual.textualize.io
[pipx]: https://github.com/pypa/pipx
[PyPi]: https://pypi.org/project/blueutil-tui/

<!-- external Links Others -->
[rye]: https://rye.astral.sh
[uv]: https://docs.astral.sh/uv
[homebrew]: https://brew.sh
[blueutil]: https://github.com/toy/blueutil
[blueutil_install]: https://github.com/toy/blueutil?tab=readme-ov-file#installupdateuninstall
