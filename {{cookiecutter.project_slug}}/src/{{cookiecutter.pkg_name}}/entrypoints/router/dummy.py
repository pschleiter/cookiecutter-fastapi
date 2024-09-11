import secrets
from fastapi import APIRouter, HTTPException, Request, status

from {{ cookiecutter.pkg_name }}.entrypoints.deps import ServiceDep

router = APIRouter()


@router.get('/session')
def new_session(request: Request):
    request.session['id'] = secrets.token_urlsafe(64)
    return 'Success'


@router.get('/hello')
def hello(service: ServiceDep):
    if service is None:
        return 'No service.'
    return 'Hello World.'


@router.post('/test')
def test(request: Request, value: str):
    if 'id' in request.session:
        return f'Your value: {value}'
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized'
    )
