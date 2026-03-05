# Kazpi Stock MVP + AI Chatbot

Бұл жоба: Flask + SQLite склад/жолда/келе жатыр есебі және **AI чат-бот** (OpenAI API арқылы).

## 1) Локально іске қосу

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

set OPENAI_API_KEY=YOUR_KEY        # Windows cmd
export OPENAI_API_KEY=YOUR_KEY     # macOS/Linux

python app.py
```

Сайт: `http://localhost:5000`

Чат: `http://localhost:5000/chat`

## 2) Docker арқылы іске қосу

> Алдымен `.env` файлға кілтті салған ыңғайлы:

`.env`:

```
OPENAI_API_KEY=YOUR_KEY
OPENAI_MODEL=gpt-5.2
SECRET_KEY=change-me
```

Сосын:

```bash
docker compose up --build
```

SQLite база `./data/app.db` ішінде сақталады.

## 3) GitHub-қа шығару

```bash
git init
git add .
git commit -m "Add AI chatbot + Docker"

# GitHub-та жаңа repo ашып, сосын:
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```
