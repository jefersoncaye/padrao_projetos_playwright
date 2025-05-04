import os
import sys
import subprocess
import psutil as ps
import time
import pytest
from playwright.sync_api import expect
from utilitarios.backup_restore_postgre_jenkins import restaurar_backup_postgre, criar_backup_postgre
import xml.etree.ElementTree as et
import re
import requests
from utilitarios.banco_dados import executar_comando_sql
import json
from page_objects.objetos_gerais import ObjetosGerais

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_global

host_postgre = 'Apus'
database_postgre = 'postgres'
user_postgre = 'postgres'
password_postgre = 'masterkey'
porta_postgre = '5432'
psql = r'C:\Program Files\PostgreSQL\15\bin\psql.exe'
os.putenv('PGPASSWORD', password_postgre)


def encerrar_processo_e_subprocessos(pai_pid):
    processo_pai = ps.Process(pai_pid)
    processos_filhos = processo_pai.children(recursive=True)

    for processo in processos_filhos + [processo_pai]:
        try:
            processo.terminate()
        except ps.NoSuchProcess:
            pass


def iniciar_nHttp(caminho_exe=r'D:\workspace\Tributario\nHttp.exe'):
    for proc in ps.process_iter():
        info = proc.as_dict(attrs=['pid', 'name'])
        if 'nhttp' in info['name'].lower():
            print("\nnHttp.exe aberto, Fechando..")
            encerrar_processo_e_subprocessos(info['pid'])
            time.sleep(2)
    print(f"Abrindo {caminho_exe}")
    subprocess.Popen(
        [caminho_exe, '/log'], cwd=r'D:\workspace\Tributario',
        creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(20)


def fechar_nHttp():
    print('Fechando nHttp.Exe')
    for proc in ps.process_iter(['pid', 'name']):
        info = proc.as_dict(attrs=['pid', 'name'])
        if 'nhttp' in info['name'].lower():
            encerrar_processo_e_subprocessos(info['pid'])
            time.sleep(2)


def iniciar_nserver_config(caminho_exe=r'D:\workspace\Tributario\nServerConfig.exe'):
    for proc in ps.process_iter():
        info = proc.as_dict(attrs=['pid', 'name'])
        if 'nserverconfig' in info['name'].lower():
            print("\nnServerConfig.exe aberto, Fechando..")
            encerrar_processo_e_subprocessos(info['pid'])
            time.sleep(2)
    print(f"Abrindo {caminho_exe}")
    subprocess.Popen(
        [caminho_exe, '/log'], cwd=r'D:\workspace\Tributario',
        creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(20)


def fechar_nserver_config():
    print('Fechando nServerConfig.Exe')
    for proc in ps.process_iter(['pid', 'name']):
        info = proc.as_dict(attrs=['pid', 'name'])
        if 'nserverconfig' in info['name'].lower():
            encerrar_processo_e_subprocessos(info['pid'])
            time.sleep(2)


def converter_base(conexao, caminho_exe=r'D:\workspace\Tributario\nfpa.exe'):
    if config_global.in_jenkins:
        url = f"http://{config_global.servidor_global}:8000/converter_base"

        payload = {
            "caminho_exe": caminho_exe,
            "conexao": conexao
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print("Erro:", response.json())

    else:
        print('\nAtualizando Base, aguarde...')
        print(
            f'{caminho_exe}',
            '/Auto',
            f'/Con:{conexao}',
            '/Usu:Administrador',
            '/Sen:masterkey',
            '/Converter:conv',
            '/ignoraperso',
            '/x')
        resultado_converter_base = subprocess.call(
            [f'{caminho_exe}', '/Auto', f'/Con:{conexao}', '/Usu:Administrador', '/Sen:masterkey',
             '/Converter:conv', '/ignoraperso', '/x'], timeout=1200)
        if resultado_converter_base == 0:
            print('\nAtualização Realizada com sucesso!')
        else:
            exit(
                f'\nOcorreu algum erro na atualização, Verifique!\n{resultado_converter_base}')


def atualizar_personalizacao(conexao, caminho_exe=r'D:\workspace\Tributario\nGem.exe'):
    if config_global.in_jenkins:
        url = f"http://{config_global.servidor_global}:8000/atualizar_perso"

        payload = {
            "caminho_exe": caminho_exe,
            "conexao": conexao
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print("Erro:", response.json())

    else:
        executar_comando_sql(banco_dados_postgre=f'db{conexao}', comando_sql_postre='delete from personalizacao')
        print('\nAtualizando Perso, aguarde...')
        print(
            caminho_exe,
            f'/con:{conexao}',
            '/auto',
            '/Usu:administrador',
            '/Sen:masterkey',
            '/xx',
            '/PersoCod:7800',
            f'/PersoSeq:1',
            '/PersoInscr:00.000.000/0000-00')
        for i in range(1, 4):
            try:
                resultado_atualizar_perso = subprocess.call(
                    [f'{caminho_exe}',
                     f'/con:{conexao}',
                     '/auto',
                     '/Usu:administrador',
                     '/Sen:masterkey',
                     '/xx',
                     '/PersoCod:7800',
                     f'/PersoSeq:{i}',
                     '/PersoInscr:00.000.000/0000-00'], timeout=200)
            except:
                pass


def sair_cloud(page, fechar_nhttp=True, _fechar_nserver_config=True):
    page.locator('div.header-logo')
    page.locator(".symbol-label").first.click(timeout=40000)
    page.get_by_role("link", name="Sair").click()
    if _fechar_nserver_config:
        fechar_nserver_config()
    if fechar_nhttp:
        fechar_nHttp()


def ler_arquivo_configuracao(modulo):
    dicionario = {}
    arquivo_xml = ''
    modulos_arquivo_fiscal = ['nfis', 'nctb', 'ngem', 'quiu']
    modulos_arquivo_folha = ['nfpa', 'nhttp', 'geral']
    modulos_arquivo_abre_fecha = ['abrefecha']
    modulos_arquivo_api = ['api']

    if modulo.lower() in modulos_arquivo_fiscal:
        arquivo_xml = r'D:\workspace\testesweb\Cloud\ArquivosConfiguracaoInstalacao\ConfiguracaoFiscalPostgre.xml'
    if modulo.lower() in modulos_arquivo_folha:
        arquivo_xml = r'D:\workspace\testesweb\Cloud\ArquivosConfiguracaoInstalacao\ConfiguracaoFolhaPostgre.xml'
    if modulo.lower() in modulos_arquivo_abre_fecha:
        arquivo_xml = r'D:\workspace\testesweb\Cloud\ArquivosConfiguracaoInstalacao\ConfiguracaoAbreFecha.xml'
    if modulo.lower() in modulos_arquivo_api:
        arquivo_xml = r'D:\workspace\testesweb\Cloud\ArquivosConfiguracaoInstalacao\ConfiguracaoApiPostgre.xml'

    tree = et.parse(arquivo_xml)
    root = tree.getroot()
    for elem in root.iter('property'):
        nome = elem.attrib.get('name')
        valor = elem.attrib.get('value')
        if nome == 'fazerBackup':
            dicionario['fazer_bkp_global'] = valor
        if nome == 'restaurarBackup':
            dicionario['restaurar_bkp_global'] = valor
    return dicionario.values()


def ler_arquivo_cfg_nia(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    versao = None
    projeto = None
    build = None

    for i, linha in enumerate(linhas):
        linha = linha.strip()

        if linha == "[Versao]":
            for j in range(i + 1, len(linhas)):
                if "Versao=" in linhas[j]:
                    versao = linhas[j].split('=')[1].strip()
                    break

        if linha == "[Construcao]":
            for j in range(i + 1, len(linhas)):
                if "Projeto=" in linhas[j]:
                    projeto = linhas[j].split('=')[1].strip()
                elif "Build=" in linhas[j]:
                    build = linhas[j].split('=')[1].strip()
                if projeto and build:
                    break

    if versao and projeto and build:
        return f"{versao} - {projeto} : {build} - "
    else:
        raise ValueError("Não foi possível encontrar todas as informações necessárias no arquivo.")


def login_cloud(
        page,
        usuario,
        conexao,
        senha,
        empresa,
        filial,
        periodo_calculo,
        data_inicial,
        data_final,
        escritorio='',
        modulo='',
        restaurar_bkp: bool = True,
        fazer_bkp: bool = True,
        atualizar_base: bool = True,
        iniciar_nserverconfig: bool = True,
        atualizar_perso: bool = False,
        excluir_cookies: bool = False,
        restaurar_bkp_padrao: bool = False):
    dia_inicial, mes_inicial, ano_inicial = data_inicial.split("/")
    dia_final, mes_final, ano_final = data_final.split("/")
    parametros = {
        "empresa": empresa,
        "filial": filial,
        "periodo_calculo": periodo_calculo,
        "data_inicial": f"{ano_inicial}-{mes_inicial}-{dia_inicial}",
        "data_final": f"{ano_final}-{mes_final}-{dia_final}",
    }
    with open(r'D:\workspace\TestesWeb\Cloud\parametros_sessao.json', "w", encoding="utf-8") as arquivo:
        json.dump(parametros, arquivo, ensure_ascii=False, indent=4)
    if excluir_cookies:
        page.context.clear_cookies()
        try:
            if os.path.exists(r"D:\Workspace\testesweb\Cloud\playwright\auth\state.json"):
                os.remove(r"D:\Workspace\testesweb\Cloud\playwright\auth\state.json")
                print("Json excluído com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar excluir o Json: {e}")
    if config_global.in_jenkins:
        with open(r'D:\workspace\numeroBuildTC.txt', 'w') as arquivo:
            arquivo.write(
                ler_arquivo_cfg_nia(caminho_arquivo=fr'\\{config_global.servidor_global}\Tributario\_cfg.nia'))
    restaurar_bkp_job = False
    if config_global.in_jenkins:
        arquivo_conexao = open(fr'\\{config_global.servidor_global}\Tributario\Questor.Conexao.ini',
                               'r').read().strip()
    else:
        arquivo_conexao = open(r'D:\workspace\Tributario\Questor.Conexao.ini',
                               'r').read().strip()
    if config_global.in_jenkins:
        build_data = open(fr'\\{config_global.servidor_global}\Tributario\Build.data', 'r').read().strip()
    else:
        build_data = open(r'D:\workspace\Tributario\Build.data', 'r').read().strip()
    if os.path.isfile(r'D:\workspace\testesweb\Cloud\restaurarBackupJob.txt'):
        restaurar_bkp_job = True
    fazer_bkp_global, restaurar_bkp_global = ler_arquivo_configuracao(modulo=modulo)
    print(f'\nFaz login com os seguintes parametros:'
          f'\n- Usuario: {usuario}@{conexao}'
          f'\n- Senha: {senha}'
          f'\n- Empresa: {empresa}'
          f'\n- Filial: {filial}'
          f'\n- Periodo Calculo: {periodo_calculo}'
          f'\n- Data Inicial: {data_inicial}'
          f'\n- Data Final: {data_final}')
    print(f"\nOpção 'restaurar_bkp' = {restaurar_bkp}")
    print(f"Opção 'fazer_bkp' = {fazer_bkp}")
    print(f"Opção 'restaurar_bkp_global' = {restaurar_bkp_global}")
    print(f"Opção 'restaurar_bkp_job' = {restaurar_bkp_job}")
    print(f"Opção 'fazer_bkp_global' = {fazer_bkp_global}")
    if restaurar_bkp_padrao:
        print('\nTeste Configurado para voltar backup padrão!')
        restaurar_backup_postgre(
            pasta='backupPadrao',
            base=f'db{conexao}')
    elif restaurar_bkp and restaurar_bkp_job:
        if 'TipoBancoDados=PostgreSQL' in arquivo_conexao:
            restaurar_backup_postgre(
                pasta='backupAtual',
                base=f'db{conexao}')
    elif restaurar_bkp and modulo and (restaurar_bkp_global.lower() != 'nao'):
        if 'TipoBancoDados=PostgreSQL' in arquivo_conexao:
            restaurar_backup_postgre(
                pasta=restaurar_bkp_global,
                base=f'db{conexao}')
    if 'TipoBancoDados=PostgreSQL' in arquivo_conexao:
        try:
            command = (
                f'"{psql}" -h apus -p {porta_postgre} -U {user_postgre} -d {database_postgre} -c "ALTER DATABASE db{conexao} SET datestyle TO ISO, DMY"')
            subprocess.call(command, shell=True)
            print("Ajustado datestyle para ISO, DMY")
        except BaseException:
            pytest.exit(f"Erro ao ajustar datestyle, Verifique!")
        try:
            command = (
                f'"{psql}" -h apus -p {porta_postgre} -U {user_postgre} -d {database_postgre} -c "ALTER DATABASE db{conexao}_cache SET datestyle TO ISO, DMY"')
            subprocess.call(command, shell=True)
            print("Ajustado datestyle para ISO, DMY base CACHE")
        except BaseException:
            print(f"Erro ao ajustar datestyle base Cache, Verifique!")
    try:
        if iniciar_nserverconfig:
            if not config_global.in_jenkins:
                iniciar_nserver_config()
        time.sleep(5)
        if not os.path.isfile(
                'd:\\workspace\\testesWeb\\Cloud\\playwright\\auth\\state.json'):
            if atualizar_base:
                converter_base(conexao)
            if atualizar_perso:
                atualizar_personalizacao(conexao)
            page.goto('home/Inicio')
            if page.get_by_role(
                    "button",
                    name="PERMITIR").is_visible(
                timeout=2500):
                page.get_by_role("button", name="PERMITIR").click()
            page.get_by_placeholder(
                "Usuário@Conexão").fill(f'{usuario}@{conexao}')
            page.get_by_placeholder("Senha").fill(senha)
            page.get_by_role("button", name="ENTRAR").click(timeout=180000)
            page.get_by_label("Empresa  *").clear()
            page.get_by_label("Empresa  *").fill(empresa)
            page.wait_for_timeout(2000)
            page.get_by_label("Filial  *").clear()
            page.get_by_label("Filial  *").fill(filial)
            page.wait_for_timeout(2000)
            page.get_by_label("Período de Cálculo  *").clear()
            page.get_by_label("Período de Cálculo  *").fill(periodo_calculo)
            page.wait_for_timeout(2000)
            page.get_by_role(
                "textbox",
                name="Informe a data inicial para o filtro do período fiscal").clear()
            page.get_by_role(
                "textbox",
                name="Informe a data inicial para o filtro do período fiscal").fill(data_inicial)
            page.wait_for_timeout(2000)
            page.get_by_role(
                "textbox",
                name="Informe a data final para o filtro do período fiscal").clear()
            page.get_by_role(
                "textbox",
                name="Informe a data final para o filtro do período fiscal").fill(data_final)
            page.locator('#btnDefaultSubmit').click(timeout=120000)
            page.wait_for_timeout(2000)

        else:
            page.goto('home/Inicio')
        expect(page.locator(
            'xpath=//*[@id="SelecaoEmpresaList"]/span[1]')).to_be_visible(timeout=20000)
        if escritorio:
            expect(
                page.locator('xpath=//*[@id="SelecaoEmpresaList"]/span[1]')).to_contain_text(
                escritorio, timeout=20000)
        page.wait_for_load_state('networkidle')
        if restaurar_bkp_padrao:
            criar_backup_postgre(
                base=f'db{conexao}',
                pasta=f'backupPadrao',
                build_data=build_data)
        elif fazer_bkp_global.lower() != 'nao' and fazer_bkp:
            criar_backup_postgre(
                base=f'db{conexao}',
                pasta=fazer_bkp_global,
                build_data=build_data)

        print('-----Fim do Login-----')
    except BaseException as erro:
        print('-----Fim do Login-----')
        pytest.exit(f'Falha no login. Verifique!\n{erro}')


def alterar_selecao_empresa(
        page,
        empresa,
        filial,
        periodo_calculo,
        data_inicial,
        data_final,
        escritorio):
    dia_inicial, mes_inicial, ano_inicial = data_inicial.split("/")
    dia_final, mes_final, ano_final = data_final.split("/")
    parametros = {
        "empresa": empresa,
        "filial": filial,
        "periodo_calculo": periodo_calculo,
        "data_inicial": f"{ano_inicial}-{mes_inicial}-{dia_inicial}",
        "data_final": f"{ano_final}-{mes_final}-{dia_final}",
    }
    with open(r'D:\workspace\TestesWeb\Cloud\parametros_sessao.json', "w", encoding="utf-8") as arquivo:
        json.dump(parametros, arquivo, ensure_ascii=False, indent=4)
    ObjetosGerais.acessar_home(page)
    page.wait_for_timeout(2000)
    page.wait_for_load_state('networkidle')
    page.locator("#SelecaoEmpresaList").click()
    page.get_by_label("Empresa  *").clear()
    page.get_by_label("Empresa  *").fill(empresa)
    page.get_by_label("Empresa  *").press('Tab')
    page.wait_for_load_state('networkidle')
    page.get_by_label("Filial  *").clear()
    page.get_by_label("Filial  *").fill(filial)
    page.get_by_label("Filial  *").press('Tab')
    page.wait_for_timeout(1000)
    page.wait_for_load_state('networkidle')
    page.locator('#ctrlCODIGOPERCALCULO').clear()
    expect(page.locator('#ctrlCODIGOPERCALCULO')).not_to_have_class(re.compile(r"lookup-spinner-inside"), timeout=30000)
    page.locator('#ctrlCODIGOPERCALCULO').fill(periodo_calculo)
    page.locator('#ctrlCODIGOPERCALCULO').press('Tab')
    page.wait_for_load_state('networkidle')
    page.get_by_role(
        "textbox",
        name="Informe a data inicial para o filtro do período fiscal").clear()
    page.get_by_role(
        "textbox",
        name="Informe a data inicial para o filtro do período fiscal").fill(data_inicial)
    page.wait_for_load_state('networkidle')
    page.get_by_role(
        "textbox",
        name="Informe a data final para o filtro do período fiscal").clear()
    page.get_by_role(
        "textbox",
        name="Informe a data final para o filtro do período fiscal").fill(data_final)
    page.wait_for_timeout(2000)
    page.wait_for_load_state('networkidle')
    page.locator('#btnDefaultSubmit').click(timeout=120000)
    page.wait_for_timeout(2000)
    page.wait_for_load_state('networkidle')
    expect(page.locator('xpath=//*[@id="SelecaoEmpresaList"]/span[1]')
           ).to_contain_text(escritorio, timeout=20000)
    page.wait_for_timeout(2000)
    page.wait_for_load_state('networkidle')
