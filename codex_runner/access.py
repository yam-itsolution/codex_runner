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
    )


def deny_access(path: str, user: str) -> None:
    subprocess.run(
        ['icacls', path, '/deny', f'{user}:(R,W,M)'],
        check=True,
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
        ['icacls', path],
        capture_output=True,
        text=True,
        check=True,
    )

    allow: set[str] = set()
    deny: set[str] = set()

    for line in result.stdout.splitlines():
        if not line.strip().startswith(user):
            continue

        perms_part = line.split(':', 1)[1]

        is_deny = '(DENY)' in perms_part

        for part in perms_part.split(')'):
            part = part.strip('(')
            if not part or part in {'OI', 'CI', 'I', 'DENY'}:
                continue

            if is_deny:
                deny.add(part)
            else:
                allow.add(part)

    if deny & rights:
        return False

    return rights <= allow
