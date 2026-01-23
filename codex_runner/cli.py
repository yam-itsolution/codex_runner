import os
import subprocess

try:
    from .user import USER
except ImportError:
    from warnings import warn
    warn('create codex_runner/user.py')


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
