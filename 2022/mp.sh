mypy --strict $@
flake8 --extend-ignore=E203,E128,E501,E741 $@
