import click

from app import app

# from decouple import config
# app.config.from_object(config("APP_SETTINGS"))


@app.cli.command("sample_command")
def sample_command():
    click.echo("This is a sample command")
