## Local deploy instructions

1) Create and activate virtulalenv:
- `python3 -m venv .venv`  
- `source .venv/bin/activate`  

2) pip install -r requirements.txt

3) Create postgresql db

4) Create .env file in csmoney directory from template .env.template and add your local configuration to it.

5) python manage.py migrate

6) python manage.py runserver
