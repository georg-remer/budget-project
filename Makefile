install:
	poetry install
test:
	poetry run coverage run personal_budget/manage.py test monthly_budget
	poetry run coverage report -m
run:
	poetry run python personal_budget/manage.py runserver
migrate:
	poetry run python personal_budget/manage.py makemigrations
	poetry run python personal_budget/manage.py migrate
loaddata:
	poetry run python personal_budget/manage.py loaddata category.json --app monthly_budget 
check:
	poetry run python personal_budget/manage.py check
code:
	poetry run code .
shell:
	poetry run python personal_budget/manage.py shell
