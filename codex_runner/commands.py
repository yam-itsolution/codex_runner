import sys
from .config import save_user, load_user, UserNotConfigured


def init_command() -> None:
    user = input('Enter username to run codex under: ').strip()
    if not user:
        print('User cannot be empty')
        sys.exit(1)

    save_user(user)
    print('Done: User configured')


def require_user() -> str:
    try:
        return load_user()
    except UserNotConfigured as e:
        print(e)
        sys.exit(1)
