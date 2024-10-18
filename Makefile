VENV_ACTIVATE = . venv/bin/activate
ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = venv\Scripts\activate
endif

runserver:
	$(VENV_ACTIVATE) && python manage.py runserver

makemigrations:
	$(VENV_ACTIVATE) && python manage.py makemigrations

migrate:
	$(VENV_ACTIVATE) && python manage.py migrate

createsuperuser:
	$(VENV_ACTIVATE) && python manage.py createsuperuser