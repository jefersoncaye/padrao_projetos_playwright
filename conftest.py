import pytest
import pytest_html
from slugify import slugify
import os
import shutil
import sys
import psycopg2

urls_por_teste = {}

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_global

jenkins_url = os.getenv('BUILD_URL')


def pytest_addoption(parser):
    parser.addoption("--salvar_video", action="store", default="off", help="Turn video recording on/off")


@pytest.fixture(scope="session")
def set_up_context(browser, request):
    pasta_arquivos_magicos = r'padrao_projetos_playwright\ArquivosComuns\ArquivosMagicos\ArquivosServidor\LOCALHOST'
    pasta_tributario = r'D:\workspace\Tributario'
    video_option = request.config.getoption("--salvar_video")
    record_video = video_option.lower() == "on"
    if config_global.in_jenkins:
        url_base = f'http://{config_global.servidor_global}:8080/'
    else:
        for arquivo in os.listdir(pasta_arquivos_magicos):
            caminho_origem = os.path.join(pasta_arquivos_magicos, arquivo)
            caminho_destino = os.path.join(pasta_tributario, arquivo)

            if os.path.isfile(caminho_origem):
                shutil.copy2(caminho_origem, caminho_destino)
        url_base = f'http://{config_global.servidor_global}:8080/'

    if os.path.isfile(
            r'padrao_projetos_playwright\playwright\auth\state.json'):
        context = browser.new_context(
            storage_state=r'padrao_projetos_playwright\playwright\auth\state.json',
            base_url=url_base,
            record_video_dir="test-results/" if record_video else None,
            viewport={"width": 1366, "height": 768})
    else:
        context = browser.new_context(base_url=url_base,
                                      record_video_dir="test-results/" if record_video else None,
                                      viewport={"width": 1366, "height": 768})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context
    nome_arquivo_teste = next((arg for arg in sys.argv if arg.endswith(".py")), "teste_desconhecido")
    nome_trace = f"{slugify(nome_arquivo_teste)}.zip"
    trace_path = os.path.join(r"padrao_projetos_playwright\test-results\traces", nome_trace)
    context.tracing.stop(path=trace_path)
    if not os.path.isfile(
            r'padrao_projetos_playwright\playwright\auth\state.json'):
        context.storage_state(
            path=r'padrao_projetos_playwright\playwright\auth\state.json')
    context.close()


@pytest.fixture(scope="session")
def set_up_page(set_up_context):
    page = set_up_context.new_page()
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(120000)

    nome_arquivo_teste = next((arg for arg in sys.argv if arg.endswith(".py")), "desconhecido")

    urls_por_teste[nome_arquivo_teste] = []

    def log_request(req):
        urls_por_teste[nome_arquivo_teste].append(req.url)

    page.on("request", log_request)

    yield page

    page.remove_listener("request", log_request)
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if 'set_up_page' in item.fixturenames:
        page = item.funcargs['set_up_page']
        extras.append(pytest_html.extras.url("https://trace.playwright.dev/"))

        if report.when == 'call':
            xfail = hasattr(report, 'wasxfail')
            try:
                if (report.skipped and xfail) or (report.failed and not xfail):
                    screen_file = f'imagens\\{slugify(item.nodeid)}.png'
                    page.screenshot(path=screen_file, full_page=True)
                    extras.append(pytest_html.extras.png(screen_file))
            except:
                print('Ocorreu um erro ao salvar a imagem do teste!')
            report.extra = extras

    if 'set_up_page_abre_fecha' in item.fixturenames:
        page = item.funcargs['set_up_page_abre_fecha']
        extras.append(
            pytest_html.extras.url(page.url,
                                   name='URL Testada'))
        if report.when == 'call':
            xfail = hasattr(report, 'wasxfail')
            path_video = page.video.path()
            try:
                if (report.skipped and xfail) or (report.failed and not xfail):
                    screen_file = f'imagens\\{slugify(item.nodeid)}.png'
                    page.screenshot(path=screen_file, full_page=True)
                    extras.append(pytest_html.extras.png(screen_file))
                    new_video_path = f"videos\\{slugify(item.nodeid)}.webm"
                    page.context.close()
                    if os.path.isfile(new_video_path):
                        os.remove(new_video_path)
                    os.rename(path_video, new_video_path)
                    if jenkins_url:
                        extras.append(
                            pytest_html.extras.url(f'{jenkins_url}artifact/videos/{slugify(item.nodeid)}.webm',
                                                   name='Video do Erro'))
                else:
                    page.context.close()
                    if os.path.isfile(path_video):
                        os.remove(path_video)
            except Exception as erro:
                print(f'Ocorreu um erro ao salvar a imagem do teste!:\n{erro}')
            report.extra = extras


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 5 and session.config.getoption("lf"):
        session.exitstatus = 0
    try:
        conn = psycopg2.connect(
            dbname="informacoes_testes",
            user='xxxxxx',
            password='xxxxxx',
            host='apus',
            port='5432'
        )
        cur = conn.cursor()

        for nome_teste, urls in urls_por_teste.items():
            nome_inserir = os.path.splitext(os.path.basename(nome_teste))[0]
            if nome_inserir != '_jb_pytest_runner':
                cur.execute(
                    "DELETE FROM urls_acessadas_por_teste WHERE nome_teste = %s",
                    (nome_inserir,)
                )
                for url in urls:
                    if 'Class:' in url:
                        cur.execute("""
                            INSERT INTO urls_acessadas_por_teste (nome_teste, url)
                            VALUES (%s, %s)
                            """, (nome_inserir, url))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao salvar informações das urls acessadas no banco:", e)
