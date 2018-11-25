from click.testing import CliRunner
import imagenet_utils

def test_search():
    runner = CliRunner()
    result = runner.invoke(imagenet_utils.cli, "search")
    assert result.exit_code == 0

