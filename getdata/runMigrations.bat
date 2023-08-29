@echo off
cd C:\Users\CHRIS\web\coda\app
call venv\Scripts\activate
py manage.py makemigrations accounts
py manage.py makemigrations main
py manage.py makemigrations management
py manage.py makemigrations finance
py manage.py makemigrations data
py manage.py makemigrations application
py manage.py makemigrations getdata
py manage.py makemigrations investing
pause







