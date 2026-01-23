# codex-runner

Вспомогательная CLI-утилита для Windows, которая запускает CLI codex от имени другого пользователя Windows с помощью runas.

## Установка

1) Создайте файл codex_runner/user.py (он добавлен в .gitignore) на основе примера и укажите ваше имя пользователя Windows:

```powershell
Copy-Item codex_runner/user_example.py codex_runner/user.py
```

2) Установите проект из корня репозитория:

```bash
pip install -e .
```

## Run

После установки команда будет доступна как:

```bash
codex-run
```

Команда запускает codex --cd "<текущая директория>" в сессии cmd.exe, созданной через runas.

