# BrowserKeyCleaner

Десктопное Windows-приложение для удаления сохранённых паролей из установленных браузеров.

## Возможности

- Автоматически определяет установленные браузеры
- Показывает статус хранилища паролей для каждого браузера (чисто / есть данные)
- Удаляет пароли из всех поддерживаемых браузеров одним кликом
- Два варианта интерфейса: Tkinter (`tk_ui`) и Flet (`flet_ui`)

## Поддерживаемые браузеры

| Браузер | Способ хранения паролей |
|---|---|
| Google Chrome | SQLite (Login Data) |
| Microsoft Edge | SQLite (Login Data) |
| Yandex Browser | SQLite (Ya Passman Data) |
| Mozilla Firefox | JSON + key4.db |
| Internet Explorer | Реестр Windows |
| Chromium-Gost | SQLite (Login Data) |

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

По умолчанию запускается интерфейс на Tkinter. Для Flet-версии запустите `flet_ui/app.py`.

## Зависимости

- `customtkinter` — GUI на Tkinter
- `pybrowsers` — определение установленных браузеров
- `psutil` — завершение процессов браузеров перед очисткой
- `nuitka` — компиляция в исполняемый файл

## Сборка в .exe

```bash
python build_s.py
```

## Требования

- Windows
- Python 3.10+
