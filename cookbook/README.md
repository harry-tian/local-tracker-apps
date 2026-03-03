# Recipe Cookbook

A local Django + SQLite webapp for storing and browsing recipes. Filter by ingredients and tags.

## TODOs
1. version control for receipes

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

Open http://0.0.0.0:8000/ (or http://localhost:8000/). Access from other devices on your network via your machine's LAN IP (e.g. http://192.168.1.x:8000/).
