# dbt-accelerator
DBT Cli to accelerate your work


# init dev inviroment
```
rm -rf venv
pyenv shell 3.9.7
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install tox

# Install Git hooks
pip install pre-commit
pre-commit install
pre-commit autoupdate
```

# run tests
```
tox -e tests
tox -e integration
```
