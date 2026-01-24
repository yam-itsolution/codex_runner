import subprocess
from enum import Enum
from typing import Iterable, Union


class AccessRight(str, Enum):
    R = 'R'     # Read
    W = 'W'     # Write
    M = 'M'     # Modify
    RX = 'RX'   # Read & Execute
    F = 'F'     # Full control


def grant_access(path: str, user: str) -> None:
    subprocess.run(
        ['icacls', path, '/grant', f'{user}:(OI)(CI)M'],
        check=True,
        stdout=subprocess.DEVNULL,
    )


def deny_access(path: str, user: str) -> None:
    subprocess.run(
        ['icacls', path, '/deny', f'{user}:({AccessRight.R},{AccessRight.W},{AccessRight.M},{AccessRight.RX})'],
        check=True,
        stdout=subprocess.DEVNULL,
    )


def have_access(
    path: str,
    user: str,
    rights: Union['AccessRight', Iterable['AccessRight']],
) -> bool:
    if isinstance(rights, AccessRight):
        rights = {rights.value}
    else:
        rights = {r.value for r in rights}

    result = subprocess.run(
        ["icacls", path],
        capture_output=True,
        text=True,
        check=True,
    )

    allow: set[str] = set()
    deny: set[str] = set()

    user_l = user.lower()

    for line in result.stdout.splitlines():
        line_l = line.lower()

        if f'{user_l}:' not in line_l:
            continue

        perms_part = line.split(':', 1)[1]
        is_deny = '(DENY)' in perms_part.upper()

        for part in perms_part.split(')'):
            part = part.strip('(').strip()
            if not part or part.upper() in {'OI', 'CI', 'I', 'DENY'}:
                continue

            if is_deny:
                deny.add(part)
            else:
                allow.add(part)

    if deny & rights:
        return False

    return bool(allow & rights)
