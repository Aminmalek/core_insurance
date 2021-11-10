@echo off
echo "creating python environment"
call python -m venv venv
call venv\scripts\activate.bat

echo "installing requirements"
call pip install -r requirements.txt

echo "delete cashe"
call del /f /s /q .\Health_Insurance\__pycache__\*

echo "delete old migrations"
call del /f /s /q .\authenticate\migrations\*
call del /f /s /q .\core\migrations\*
call del /f /s /q .\insurance\migrations\*
call del /f /s /q .\insured\migrations\*
call del /f /s /q .\payment\migrations\*
call del /f /s /q .\super_holder\migrations\*
call del /f /s /q .\ticket\migrations\*

echo "creating database"
call python manage.py makemigrations authenticate insurance insured payment super_holder ticket
call python manage.py migrate

echo "creating user"
call python manage.py createsuperuser

echo "seeding data"
call python manage.py seed

echo "done"