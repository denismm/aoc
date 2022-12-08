mypy --strict $@
flake8 --extend-ignore=E203,E128 $@
