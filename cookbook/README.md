# Recipe Cookbook

A local Django + SQLite webapp for storing and browsing recipes. Filter by ingredients and tags.

Open [http://0.0.0.0:8000/](http://0.0.0.0:8000/) (or [http://localhost:8000/](http://localhost:8000/)).

## TODOs

1. version control for receipes

## Run in background

```bash
cd /Users/tianh/Desktop/local-tracker-apps/cookbook
source venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 &
```

## Setup

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

## Run

```bash
python manage.py runserver 0.0.0.0:8000
```

