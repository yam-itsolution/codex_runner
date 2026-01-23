import os
import subprocess

from .user import USER


RUNAS = r"C:\Windows\System32\runas.exe"
CODEX = r"C:\node24\codex"


def main() -> None:
    cwd = os.getcwd()

    inner_cmd = f'{CODEX} --cd "{cwd}"'

    full_cmd = [
        RUNAS,
        f"/user:{USER}",
        "/savecred",
        f'cmd.exe /k {inner_cmd}',
    ]

    subprocess.run(full_cmd, shell=False)
