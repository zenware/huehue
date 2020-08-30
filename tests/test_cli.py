import pytest
from click.testing import CliRunner

from huehue import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_bridge_list(runner):
    result = runner.invoke(cli, ['bridge', 'list'])
    assert result.exit_code == 0
    assert result.output == ""