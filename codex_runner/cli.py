import os
import subprocess
import sys

from .access import grant_access, deny_access, have_access, AccessRight
from .commands import init_command, require_user


RUNAS = r'C:\Windows\System32\runas.exe'
CODEX = r'C:\node24\codex'

FORBIDDEN_FILES = ['local_settings.py', 'private_settings.py', '.env']

SETTABLE_RIGHTS = (AccessRight.R, AccessRight.W, AccessRight.M, AccessRight.RX)


COMMAND_ARGS_FUNCS = {
    'init': init_command,
}


def run_codex() -> None:
    user = require_user()
    cwd = os.getcwd()

    if not have_access(cwd, user, SETTABLE_RIGHTS):
        grant_access(cwd, user)

    for file in FORBIDDEN_FILES:
        path = os.path.join(cwd, file)
        if os.path.exists(path):
            deny_access(path, user)

    cmd = (
        f'{RUNAS} /user:{user} /savecred '
        f'"cmd.exe /k cd /d {cwd} && {CODEX}"'
    )

    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)


def main() -> None:
    if len(sys.argv) == 1:
        run_codex()
        return

    COMMAND_ARGS_FUNCS.get(sys.argv[1], lambda: RuntimeError('Unknown command'))()
