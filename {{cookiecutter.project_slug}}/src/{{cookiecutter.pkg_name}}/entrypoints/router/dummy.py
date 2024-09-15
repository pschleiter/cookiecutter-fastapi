import secrets
from fastapi import APIRouter, HTTPException, Request, status

from {{ cookiecutter.pkg_name }}.domain import model
from {{ cookiecutter.pkg_name }}.entrypoints.deps import ServiceDep

router = APIRouter()

SESSION_MAPPING = {}


@router.post('/add_user')
async def new_session(request: Request, service: ServiceDep, dummy: model.Dummy):
    await service.create_dummy(dummy=dummy)
    session_id = secrets.token_urlsafe(64)
    request.session['id'] = session_id
    SESSION_MAPPING[session_id] = dummy.name

    return 'Success'


@router.get('/hello')
def hello():
    return 'Hello World.'


@router.post('/response')
async def test(request: Request, service: ServiceDep, value: str):
    session_id = request.session.get('id')
    if session_id is not None:
        return (
            f'{await service.get_nickname(name=SESSION_MAPPING[session_id])}: {value}'
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized'
    )
