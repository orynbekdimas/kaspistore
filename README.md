# Kazpi Stock MVP + AI Chatbot

Бұл жоба **Flask + SQLite** негізінде жасалған склад жүйесі.\
Жүйе Kaspi дүкеніне арналған **тауар есебі, жолдағы тапсырыстар, Excel
импорт және AI чат-бот** мүмкіндіктерін қамтиды.

AI чат-бот **Google Gemini API** арқылы жұмыс істейді.

------------------------------------------------------------------------

# Функциялар

Жүйеде келесі модульдер бар:

### Склад

-   Тауарларды қосу / өңдеу
-   Қолжетімді қалдықты есептеу
-   Складтың жалпы сомасын көрсету

### Келе жатыр (Incoming)

-   Жолда келе жатқан тауарларды тіркеу
-   Складқа қабылдау (Stock In)

### Жолда (Onway)

-   Сатылған, бірақ әлі жеткізілмеген тауарларды есептеу
-   Пайда, комиссия және доставка есептеу

### Excel импорт

Kaspi архивінен:

Название товара\
Статус\
Количество\
Сумма\
Доставка

арқылы сатылымдарды автоматты өңдеу.

### Есеп (Report)

-   Тауар бойынша пайда
-   Күн бойынша пайда
-   Excel экспорт

### AI чат-бот

Мысал сұрақтар:

Складта қанша тауар бар?\
Қай тауар жолда?\
Бүгінгі пайда қанша?

Чат беті:

/chat

------------------------------------------------------------------------

# 1. Локально іске қосу

## Репозиторийді жүктеу

git clone https://github.com/`<username>`{=html}/kaspistore.git\
cd kaspistore

## Virtual environment жасау

Windows:

python -m venv .venv\
.venv`\Scripts`{=tex}`\activate`{=tex}

Linux / Mac:

python3 -m venv .venv\
source .venv/bin/activate

## Кітапханаларды орнату

pip install -r requirements.txt

## Gemini API кілтін қосу

Windows PowerShell:

\$env:GEMINI_API_KEY="YOUR_KEY"

Windows CMD:

set GEMINI_API_KEY=YOUR_KEY

Linux / Mac:

export GEMINI_API_KEY=YOUR_KEY

## Серверді іске қосу

python app.py

Сайт:\
http://localhost:5000

AI чат:\
http://localhost:5000/chat

------------------------------------------------------------------------

# 2. Docker арқылы іске қосу

.env файл:

GEMINI_API_KEY=YOUR_KEY\
GEMINI_MODEL=gemini-1.5-flash\
SECRET_KEY=change-me

Сосын:

docker compose up --build

------------------------------------------------------------------------

# 3. Деректер қоры

Жоба **SQLite** қолданады.

База файлы:

app.db

Flask бірінші іске қосылғанда автоматты түрде таблицалар жасайды.

------------------------------------------------------------------------

# 4. Жоба құрылымы

project

app.py\
config.py\
models.py\
requirements.txt

templates/\
services/

app.db

------------------------------------------------------------------------

# 5. GitHub-қа шығару

git init\
git add .\
git commit -m "Kazpi Stock MVP + Gemini AI chatbot"

git branch -M main\
git remote add origin
https://github.com/`<username>`{=html}/kaspistore.git\
git push -u origin main

------------------------------------------------------------------------

# Технологиялар

-   Python
-   Flask
-   SQLAlchemy
-   SQLite
-   OpenPyXL
-   Google Gemini API
-   Docker
