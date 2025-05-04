import pytest
from utilitarios.login_cloud import fechar_nHttp
from testes_api.utilitarios.login_api import login_api
from testes_api.utilitarios.help_json import abri_json, salvar_json
from testes_api.utilitarios.validar_dicionarios import validar_schema_dicionario, validar_headers_padrao
import re

base = 'test_endpoints_api'


@pytest.fixture(scope="session")
def api_login(api_request_context):
    token_api = login_api(api_request_context, base)
    assert token_api
    yield token_api


def test_get_info(api_request_context, api_login):
    """
    Enviar GET para url: api/TnInfo/Info?tokenapi=token_api
    Obs: Atualizar token_api para o token do seu login

    Compara schema do json de retorno com json base

    Arquivo Base: get_info.json
    Arquivo Atual: get_info_atual.json
    """
    print(test_get_info.__name__)
    print(test_get_info.__doc__)
    token_api = api_login
    request = api_request_context.get(
        f'api/TnInfo/Info?tokenapi={token_api}', data={}, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_info_atual.json')
    lista_chaves_validar = ['Versao',
                            'InfoBancoDados',
                            'InfoServicos',
                            'ServerInfo',
                            'Processos', ]
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    validacao_chaves = [chave for chave in lista_chaves_validar if
                        chave not in resposta_json or not resposta_json[chave]]
    [print(f'A chave {diferenca} não foi encontrada no dicionario atual ou está vazia') for diferenca in
     validacao_chaves]
    assert request.status == 200
    assert not validacao_chaves
    validar_headers_padrao(request.headers)


def test_get_pegar_versao_questor(api_request_context, api_login):
    """
    Enviar GET para url: api/TnWebDMDadosGerais/PegarVersaoQuestor?tokenapi=token_api
    Obs: Atualizar token_api para o token do seu login

    Validar se versão retornada é igual a versão atual do sistema
    Compara schema do json de retorno com json base

    Arquivo Base: get_pegar_versao_questor.json
    Arquivo Atual: get_pegar_versao_questor_atual.json
    """
    print(test_get_pegar_versao_questor.__name__)
    print(test_get_pegar_versao_questor.__doc__)
    regex_versao = r'^\d+\.\d+\.\d+\.\d+$'
    token_api = api_login
    request = api_request_context.get(
        f'api/TnWebDMDadosGerais/PegarVersaoQuestor?tokenapi={token_api}', data={}, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_pegar_versao_questor_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_pegar_versao_questor.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)
    assert re.match(
        regex_versao, resposta_json['Versao']), "A versão não está no formato correto"


def test_get_pegar_menus_questor(api_request_context, api_login):
    """
    Enviar GET para url: api/TnWebDMMenus/Pegar?token=token_api&_ATipo=1
    Obs: Atualizar token_api para o token do seu login

    Validar se existem os menus abaixo no retorno:
        'Gerenciador de Empresas', 'Contabilidade', 'Folha de Pagamento', 'Inventário', 'Fiscal',
        'Controle Organizacional', 'Controle de Tributos', 'Financeiro', 'Tribunal de Contas do Estado',
        'Arquivos Magnéticos', 'Web', 'Serviço Trabalho Temporário', 'Controle Patrimonial',
        'Protocolo', 'Cloud', 'Lean', 'Quiu', 'Quiu - Automatizações'

    Validar a quantidade de "Childs" de cada menu é maior que 0

    Arquivo Base: get_pegar_menus_questor.json
    Arquivo Atual: get_pegar_menus_questor_atual.json
    """
    print(test_get_pegar_menus_questor.__name__)
    print(test_get_pegar_menus_questor.__doc__)
    token_api = api_login
    request = api_request_context.get(
        f'api/TnWebDMMenus/Pegar?token={token_api}&_ATipo=1', timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_pegar_menus_questor_atual.json')
    lista_modulos = ['Gerenciador de Empresas', 'Contabilidade', 'Folha de Pagamento', 'Inventário', 'Fiscal',
                     'Controle Organizacional', 'Controle de Tributos', 'Financeiro', 'Tribunal de Contas do Estado',
                     'Arquivos Magnéticos', 'Web', 'Serviço Trabalho Temporário', 'Controle Patrimonial',
                     'Protocolo', 'Cloud', 'Lean', 'Quiu', 'Quiu - Automatizações']
    for indice, modulo in enumerate(lista_modulos):
        assert resposta_json[indice]['Text'] == modulo, 'Apresentou diferença nos mudulos listados'
    lista_erros = []
    for modulo in resposta_json:
        count = 0
        count += len(modulo['Childs'])
        if count < 0:
            lista_erros.append(f'Modulo {modulo["Text"]} não apresentou nenhum menu em "Childs"')
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in lista_erros]
    assert not lista_erros
    assert request.status == 200
    validar_headers_padrao(request.headers)


def test_get_pegar_consulta_cadastro(api_request_context, api_login):
    """
    Enviar GET para url: api/TnWebDMConsulta/Pegar?token=token_api&_AActionName=TnFisDMLctoFisEnt&_AiDisplayStart=0&_AiDisplayLength=200&_AOrderBy=2&_AsEcho=asc
    Necessario enviar o body na requisição: get_pegar_consulta_cadastro_body.json
    Obs: Atualizar token_api para o token do seu login

    Compara schema do json de retorno com json base

    Arquivo Base: get_pegar_consulta_cadastro.json
    Arquivo Atual: get_pegar_consulta_cadastro_atual.json
    """
    print(test_get_pegar_consulta_cadastro.__name__)
    print(test_get_pegar_consulta_cadastro.__doc__)
    token_api = api_login
    body_get = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\data\get_pegar_consulta_cadastro_body.json')
    request = api_request_context.get(
        f'api/TnWebDMConsulta/Pegar?token={token_api}&_AActionName=TnFisDMLctoFisEnt&_AiDisplayStart=0&_AiDisplayLength=200&_AOrderBy=2&_AsEcho=asc',
        data=body_get, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_pegar_consulta_cadastro_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_pegar_consulta_cadastro.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)


def test_get_dados_gerais(api_request_context, api_login):
    """
    Enviar GET para url: api/TnWebDMDadosObjetos/Pegar?token=token_api&_AActionName=TnFisDMLctoFisEnt
    Obs: Atualizar token_api para o token do seu login

    Compara schema do json de retorno com json base

    Arquivo Base: get_dados_gerais.json
    Arquivo Atual: get_dados_gerais_atual.json
    """
    print(test_get_dados_gerais.__name__)
    print(test_get_dados_gerais.__doc__)
    token_api = api_login
    request = api_request_context.get(
        f'api/TnWebDMDadosObjetos/Pegar?token={token_api}&_AActionName=TnFisDMLctoFisEnt', timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_dados_gerais_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_dados_gerais.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)


def test_get_relatorio_executar(api_request_context, api_login):
    """
    Enviar GET para url: api/TnWebDMDadosObjetos/Pegar?token=token_api&_AActionName=TnFisDMLctoFisEnt
    Necessario enviar o body na requisição: get_relatorio_executar_body.json
    Obs: Atualizar token_api para o token do seu login

    Compara schema do json de retorno com json base

    Arquivo Base: get_relatorio_executar.json
    Arquivo Atual: get_relatorio_executar_atual.json
    """
    print(test_get_relatorio_executar.__name__)
    print(test_get_relatorio_executar.__doc__)
    token_api = api_login
    body_get = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\data\get_relatorio_executar_body.json')
    request = api_request_context.get(
        f'api/TnWebDMRelatorio/Executar?token={token_api}&_AActionName=nFisRRResumoConfLctoFisEnt&_ABase64=False&_ATipoRetorno=nrwexTxt',
        data=body_get, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_relatorio_executar_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\get_relatorio_executar.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)


def test_post_processo_executar_imp_cte(api_request_context, api_login):
    """
    Enviar POST para url: api/TnWebDMProcesso/ProcessoExecutar?token=token_api&_AActionName=TnArqDPImportarArqCTe
    Necessario enviar o body na requisição: post_processo_executar_imp_cte_body.json
    Obs: Atualizar token_api para o token do seu login

    Validar Total de Registros para Gravação e Total de Registros Gravados para:
        DuplicataSai
        LctoFisSai
        LctoFisSaiCFOP
        LctoFisSaiConFrete
        LctoFisSaiDIFAL
    Compara schema do json de retorno com json base

    Arquivo Base: post_processo_executar_imp_cte.json
    Arquivo Atual: post_processo_executar_imp_cte_atual.json
    """
    print(test_post_processo_executar_imp_cte.__name__)
    print(test_post_processo_executar_imp_cte.__doc__)
    token_api = api_login
    body_get = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\data\post_processo_executar_imp_cte_body.json')
    request = api_request_context.post(
        f'api/TnWebDMProcesso/ProcessoExecutar?token={token_api}&_AActionName=TnArqDPImportarArqCTe',
        data=body_get, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\post_processo_executar_imp_cte_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\post_processo_executar_imp_cte.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)
    # Registros para DuplicataSai
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1]['nodes'][0][
               'text'] == 'Registros para DuplicataSai'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][0]['nodes'][0]['text'] == 'Total de Registros para Gravação: 26'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][0]['nodes'][1]['text'] == 'Total de Registros Gravados: 26'
    # Registros para LctoFisSai
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1]['nodes'][1][
               'text'] == 'Registros para LctoFisSai'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][1]['nodes'][0]['text'] == 'Total de Registros para Gravação: 26'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][1]['nodes'][1]['text'] == 'Total de Registros Gravados: 26'
    # Registros para LctoFisSaiCFOP
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1]['nodes'][2][
               'text'] == 'Registros para LctoFisSaiCFOP'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][2]['nodes'][0]['text'] == 'Total de Registros para Gravação: 26'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][2]['nodes'][1]['text'] == 'Total de Registros Gravados: 26'
    # Registros para LctoFisSaiConFrete
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][
               1]['nodes'][3]['text'] == 'Registros para LctoFisSaiConFrete'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][3]['nodes'][0]['text'] == 'Total de Registros para Gravação: 27'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][3]['nodes'][1]['text'] == 'Total de Registros Gravados: 27'
    # Registros para LctoFisSaiDIFAL
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1]['nodes'][4][
               'text'] == 'Registros para LctoFisSaiDIFAL'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][4]['nodes'][0]['text'] == 'Total de Registros para Gravação: 26'
    assert resposta_json['Widgets']['bottom'][0]['Itens'][0]['nTreeView'][1][
               'nodes'][4]['nodes'][1]['text'] == 'Total de Registros Gravados: 26'
    assert resposta_json['Message'] == 'Concluído com sucesso!'


def test_post_processo_executar_cons_lcto_fis_ent(
        api_request_context, api_login):
    """
    Enviar POST para url: api/TnWebDMProcesso/ProcessoExecutar?Token=token_api&_AActionName=TnFisDPConsultaLctoSai
    Necessario enviar o body na requisição: post_processo_executar_cons_lcto_fis_ent_body.json
    Obs: Atualizar token_api para o token do seu login

    Compara schema do json de retorno com json base

    Arquivo Base: post_processo_executar_cons_lcto_fis_ent.json
    Arquivo Atual: post_processo_executar_cons_lcto_fis_ent_atual.json
    """
    print(test_post_processo_executar_cons_lcto_fis_ent.__name__)
    print(test_post_processo_executar_cons_lcto_fis_ent.__doc__)
    token_api = api_login
    body_get = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\data\post_processo_executar_cons_lcto_fis_ent_body.json')
    request = api_request_context.post(
        f'api/TnWebDMProcesso/ProcessoExecutar?Token={token_api}&_AActionName=TnFisDPConsultaLctoSai',
        data=body_get, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\post_processo_executar_cons_lcto_fis_ent_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\post_processo_executar_cons_lcto_fis_ent.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)


def test_post_processo_executar_cons_per_apurado(
        api_request_context, api_login):
    """
    Enviar POST para url: api/TnWebDMProcesso/ProcessoExecutar?token=token_api&_AActionName=TnFisDPConsultaPeriodoApurado
    Necessario enviar o body na requisição: post_processo_executar_cons_per_apurado_body.json
    Obs: Atualizar token_api para o token do seu login

    Compara schema do json de retorno com json base

    Arquivo Base: post_processo_executar_cons_per_apurado.json
    Arquivo Atual: post_processo_executar_cons_per_apurado_atual.json
    """
    print(test_post_processo_executar_cons_per_apurado.__name__)
    print(test_post_processo_executar_cons_per_apurado.__doc__)
    token_api = api_login
    body_get = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\data\post_processo_executar_cons_per_apurado_body.json')
    request = api_request_context.post(
        f'api/TnWebDMProcesso/ProcessoExecutar?token={token_api}&_AActionName=TnFisDPConsultaPeriodoApurado',
        data=body_get, timeout=60000)
    resposta_json = request.json()
    salvar_json(
        resposta_json=resposta_json,
        caminho_arquivo_salvar=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\post_processo_executar_cons_per_apurado_atual.json')
    json_base = abri_json(
        arquivo_json=r'padrao_projetos_playwright\testes_api\stores\test_endpoints_api\schemas\post_processo_executar_cons_per_apurado.json')
    resultado_schema_body = validar_schema_dicionario(
        dicionario_base=json_base, dicionario_atual=resposta_json)
    print(
        f'\n\nO retorno foi:\n'
        f'code: {request.status}')
    [print(diferenca) for diferenca in resultado_schema_body]
    assert request.status == 200
    assert not resultado_schema_body
    validar_headers_padrao(request.headers)
    fechar_nHttp()
