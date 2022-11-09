from typer.testing import CliRunner

from loglyzer import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0
    assert f'{__app_name__} v{__version__}\n' in result.stdout

def test_help():
    result = runner.invoke(cli.app, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.stdout

def test_no_file():
    result = runner.invoke(cli.app, [])
    assert result.exit_code == 0
    assert 'No file was specified' in result.stdout

def test_eps_and_bytes():
    result = runner.invoke(cli.app, ['data/access.log','--eps','--bytes'])
    assert result.exit_code == 0
    assert '\'events_per_second\': 24' in result.stdout
    assert '\'exchanged_bytes\': 22775' in result.stdout