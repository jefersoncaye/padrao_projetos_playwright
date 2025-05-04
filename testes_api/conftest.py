from playwright.sync_api import Playwright
import pytest
import os
import shutil
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_global

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    pasta_arquivos_magicos = r'padrao_projetos_playwright\ArquivosComuns\ArquivosMagicos\ArquivosServidor\LOCALHOST'
    pasta_tributario = r'D:\workspace\Tributario'
    storage_state = r'padrao_projetos_playwright\playwright\auth\state.json'
    if config_global.in_jenkins:
        url_base = f'http://{config_global.servidor_global}:8080/'
    else:
        for arquivo in os.listdir(pasta_arquivos_magicos):
            caminho_origem = os.path.join(pasta_arquivos_magicos, arquivo)
            caminho_destino = os.path.join(pasta_tributario, arquivo)

            if os.path.isfile(caminho_origem):
                shutil.copy2(caminho_origem, caminho_destino)
        url_base = f'http://{config_global.servidor_global}:8080/'


    request_context = playwright.request.new_context(
        base_url=url_base,
    )
    yield request_context
    if not os.path.isfile(storage_state):
        request_context.storage_state(path=storage_state)
    request_context.dispose()


@pytest.fixture(scope="session")
def api_request_context_geral(playwright: Playwright):
    storage_state = r'padrao_projetos_playwright\playwright\auth\state.json'
    request_context = playwright.request.new_context(
        ignore_https_errors=True,
    )
    yield request_context
    if not os.path.isfile(storage_state):
        request_context.storage_state(path=storage_state)
    request_context.dispose()
