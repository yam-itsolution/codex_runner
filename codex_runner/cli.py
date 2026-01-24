import os
import subprocess
import sys

from .access import grant_access, deny_access, have_access, AccessRight
from .commands import init_command, require_user


RUNAS = r'C:\Windows\System32\runas.exe'
CODEX = r'C:\node24\codex'

FORBIDDEN_FILES = ['local_settings.py', 'private_settings.py']

SETTABLE_RIGHTS = (AccessRight.R, AccessRight.W, AccessRight.M, AccessRight.RX)


def run_codex() -> None:
    user = require_user()
    cwd = os.getcwd()

    if not have_access(cwd, user, SETTABLE_RIGHTS):
        grant_access(cwd, user)

    for file in FORBIDDEN_FILES:
        path = os.path.join(cwd, file)
        if not os.path.exists(path) or have_access(path, user, SETTABLE_RIGHTS):
            continue
        deny_access(path, user)

    inner_cmd = f'{CODEX} --cd "{cwd}"'

    full_cmd = [
        RUNAS,
        f'/user:{user}',
        '/savecred',
        f'cmd.exe /k {inner_cmd}',
    ]

    subprocess.run(full_cmd, shell=False)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_command()
        return

    run_codex()
