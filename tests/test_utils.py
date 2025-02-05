from blueutil_tui.utils import check_blueutil_installation


def test_check_blueutil_installation(capsys, mocker):
    mocker.patch("shutil.which", return_value=None)
    check_blueutil_installation()
    captured = capsys.readouterr()
    err_str = (
        '"blueutil" was not found, please install with e.g. "brew install blueutil"\n'
        + "or use another installation method from:\n"
        + "https://github.com/toy/blueutil?tab=readme-ov-file#installupdateuninstall\n"
    )

    assert captured.err == err_str
