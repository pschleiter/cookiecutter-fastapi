from {{ cookiecutter.pkg_name }}.entrypoints.main import create_api

app = create_api()
