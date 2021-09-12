@echo off
echo "creating python environment"
call python -m venv venv
call venv\scripts\activate.bat

echo "installing requirements"
call pip install -r requirements.txt

echo "creating database"
call python manage.py makemigrations authenticate insurance insured payment ticket vendor
call python manage.py migrate

echo "creating user"
call python manage.py createsuperuser

echo "done"