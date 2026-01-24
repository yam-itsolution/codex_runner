from pathlib import Path
import json


CONFIG_PATH = Path.home() / '.config' / 'codex' / 'config.json'


class UserNotConfigured(RuntimeError):
    pass


def load_user() -> str:
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        if user := data.get('user'):
            return user

    raise UserNotConfigured(
        'User is not configured.\n'
        'Run: codex-run init\n'
    )


def save_user(user: str) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps({'user': user}, indent=2),
        encoding='utf-8',
    )
