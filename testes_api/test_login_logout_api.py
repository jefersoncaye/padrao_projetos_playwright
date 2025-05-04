import pytest
from utilitarios.login_cloud import fechar_nHttp
from testes_api.utilitarios.login_api import login_api

base = 'test_login_logout_api'


@pytest.fixture(scope="session")
def api_login(api_request_context):
    token_api = login_api(api_request_context, base)
    assert token_api
    yield token_api


def test_api_logout(api_request_context, api_login):
    token_api = api_login
    print(f'\nPOST para url: home/logout?token={token_api}')
    request = api_request_context.post(f'home/logout?token={token_api}')
    print(f'O retorno foi:\n'
          f'code: {request.status}, \n\nheaders: {request.headers}\n\n')
    assert request.status == 200
    fechar_nHttp()
