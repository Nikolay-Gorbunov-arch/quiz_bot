# Telegram Quiz Bot (aiogram v3)

Асинхронный квиз-бот на **aiogram v3** с:
- 10 вопросами (вынесены в `data/questions.json`)
- показом выбранного ответа (кнопки удаляются, текст ответа выводится)
- сохранением результата последнего прохождения
- командой `/stats` для вывода статистики последних результатов игроков

## Команды
- **/start** — приветствие и кнопка «Начать игру»
- **/quiz** — начать квиз с 10 вопросами
- **/stats** — твой последний результат и ТОП последних результатов игроков

## Как запустить
```bash
python -m venv venv
# Windows PowerShell:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env  # и вставьте токен
python main.py
