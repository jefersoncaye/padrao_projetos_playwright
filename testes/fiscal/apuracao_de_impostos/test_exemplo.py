from page_objects.fiscal.apuracao_de_impostos.apuracao_impostos_estaduais import TelaApuracaoDosImpostosEstaduais, \
    TelaLimpezaApuracaoDosImpostosEstaduais
from page_objects.fiscal.icms_sc.dime import Dime
from utilitarios.login_cloud import login_cloud, sair_cloud
from page_objects.fiscal.arquivos.sped_fiscal import TelaSpedFiscal
from utilitarios.comparador_arquivos import comparar_arquivos


def test_login_cloud(set_up_page):
    page = set_up_page
    login_cloud(
        page,
        usuario='administrador',
        conexao='test_exemplo',
        senha='xxxxxxx',
        empresa='9999',
        filial='1',
        periodo_calculo='',
        data_inicial='01/01/2023',
        data_final='31/01/2023',
        escritorio='9999 - Empresa Padrão New Informática - SC',
        modulo='nFis')


def test_limpar_apuracao_icms_limpeza_cenario(set_up_page):
    """
    Obrigações > Apurações de Impostos > Limpar apuração de Impostos Estaduais ou link: /npmnFis/Processo?Scope={Class:"TnFisDPLimparApuracaoICMS",pathName:"OBRIGACOES_FISCAL_APURACOESDEIMPOSTOS_APURACAO"}
    Preenche os seguintes campos para realizar a limpeza de apuração:
    - Data Inicial: '01/01/2023'
    - Data Final: '31/01/2023'
    - Código da Empresa: '9999'
    - Código da Filial: '1'
    Inicia o processo de limpeza e valida se o texto "Executando..." desaparece da tela dentro de 30 segundos
    Valida se a mensagem "Nenhum registro excluído Empresa:9999 Filial:1" está presente no log de resultado
    """
    print(test_limpar_apuracao_icms_limpeza_cenario.__name__)
    print(test_limpar_apuracao_icms_limpeza_cenario.__doc__)
    page = set_up_page
    limpar_apuracao = TelaLimpezaApuracaoDosImpostosEstaduais(page)
    limpar_apuracao.acessar_limpeza_apuracao_impostos_estaduais()
    limpar_apuracao.limpar_apuracao_impostos_estatuais(
        data_inicial='01/01/2023',
        data_final='31/01/2023',
        cod_empresa='9999',
        cod_filial='1',
        log_validar='Nenhum registro excluído Empresa:9999 Filial:1'
    )


def test_apurar_imp_estadual(set_up_page):
    """
    Acessar Obrigações > Apurações de Impostos > Apuração dos Impostos Estaduais ou link: npmnFis/Processo?Scope={Class:%22TnFisDPApurarImpEstadual%22,pathName:%22OBRIGACOES_FISCAL_APURACOESDEIMPOSTOS_APURACAO%22}
    Preenche os seguintes campos para realizar a apuração:
    - Data Inicial: '01/01/2023'
    - Data Final: '31/01/2023'
    - Tipo de Apuração: 'Normal'
    - Código da Empresa: '9999'
    - Código da Filial: '1'
    Inicia o processo de apuração e valida se o texto "Executando..." desaparece da tela dentro de 30 segundos
    Valida se a mensagem "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" está presente no log de resultado
    """
    print(test_apurar_imp_estadual.__name__)
    print(test_apurar_imp_estadual.__doc__)
    page = set_up_page
    apurar_impostos = TelaApuracaoDosImpostosEstaduais(page)
    apurar_impostos.acessar_apuracao_impostos_estaduais()
    apurar_impostos.apurar_impostos_estaduais(
        data_inicial='01/01/2023',
        data_final='31/01/2023',
        tipo_apuracao='Normal',
        cod_empresa='9999',
        cod_filial='1',
        log_validar='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    )


def test_gerar_dime(set_up_page):
    r"""
    Acessa Obrigações > ICMS > Dime ou link: npmnFis/Processo?Scope={Class:%22TnArqDPGerarArqDIME2006%22,pathName:%22OBRIGACOES_FISCAL_ICMS_SC%22}
    Preenche os seguintes campos:
    - Tipo de Período: "Mensal"
    - Data Inicial: "01/01/2023"
    - Gerar Arquivo: 'Um Arquivo por Estabelecimento'
    - Contador: '1'
    - Empresa: '9999'
    - Filial: '1'
    - Arquivo: dime.txt
    Gera o arquivo e compara com o arquivo base
    """
    print(test_gerar_dime.__name__)
    print(test_gerar_dime.__doc__)
    page = set_up_page
    apurar_icms = Dime(page)
    apurar_icms.acessar_tela_dime()
    apurar_icms.gerar_dime(
        tipo_periodo="Mensal",
        data_inicial="01/01/2023",
        gerar_arquivo='Um Arquivo por Estabelecimento',
        contador='1',
        empresa='9999',
        filial='1',
        caminho_arquivo=r'padrao_projetos_playwright\stores\fiscal\icms_sc\test_apuracao_credito_presumido_transportes_icms_sc\dime.txt'
    )
    comparar_arquivos(
        arquivo_base=r"padrao_projetos_playwright\stores\fiscal\icms_sc\test_apuracao_credito_presumido_transportes_icms_sc\base_dime.txt",
        arquivo_atual=r'padrao_projetos_playwright\stores\fiscal\icms_sc\test_apuracao_credito_presumido_transportes_icms_sc\dime.txt',
        linhas_ignorar=[1])


def test_gerar_sped(set_up_page):
    """
    Acessar Obrigações > Gerar Arquivos > SPED Fiscal ou link: npmnFis/Processo?Scope={Class:%22TnArqDPGerarArqSPEDFis%22,pathName:%22OBRIGACOES_FISCAL_GERARARQUIVOS%22}
    - Empresa: '9999'
    - Filial: '1'
    - Data Inicial: '01/01/2023'
    - Data Final: '31/01/2023'
    - Gerar Registro Duplicatas: 'Não'
    - Gerar Somente Registros de Apuração: 'Não'
    - Gerar Registros CIAP: 'Não'
    - Gerar Valores PIS/COFINS: 'Não'
    - Gerar C170 para Modelo 55 Emissão Própria: 'Não'
    - Gerar Bloco K: 'K200/K280'
    - Gerar Registro de Inventário: 'Não'
    - Tipo de Declaração: 'Original'
    - Relatório: 'sped.txt'
    Gera o arquivo SPED e compara com o arquivo base:
    - Arquivo Base: 'base_sped.txt'
    - Arquivo Atual: 'sped.txt'
    """
    print(test_gerar_sped.__name__)
    print(test_gerar_sped.__doc__)
    page = set_up_page
    gerar_sped = TelaSpedFiscal(page)
    gerar_sped.gerar_sped_fiscal(
        cod_empresa="9999",
        cod_filial="1",
        dt_inicial="01/01/2023",
        dt_final="31/01/2023",
        gerar_registro_duplicatas="Não",
        gerar_somente_registros_de_apuracao="Não",
        gerar_registros_ciap="Não",
        gerar_valores_pis_cofins="Não",
        gerar_c170_para_modelo_55_emissao_propria="Não",
        gerar_bloco_k="K200/K280",
        gerar_registro_de_inventario="Não",
        tipo_declaracao="Original",
        caminho_relatorio=r'padrao_projetos_playwright\stores\fiscal\icms_sc\test_apuracao_credito_presumido_transportes_icms_sc\sped.txt'
    )
    comparar_arquivos(
        arquivo_base=r"padrao_projetos_playwright\stores\fiscal\icms_sc\test_apuracao_credito_presumido_transportes_icms_sc\base_sped.txt",
        arquivo_atual=r"padrao_projetos_playwright\stores\fiscal\icms_sc\test_apuracao_credito_presumido_transportes_icms_sc\sped.txt")


def test_limpar_apuracao_icms(set_up_page):
    """
    Obrigações > Apurações de Impostos > Limpar apuração de Impostos Estaduais ou link: /npmnFis/Processo?Scope={Class:"TnFisDPLimparApuracaoICMS",pathName:"OBRIGACOES_FISCAL_APURACOESDEIMPOSTOS_APURACAO"}
    - Data Inicial: '01/01/2023'
    - Data Final: '31/01/2023'
    - Empresa: '9999'
    - Filial: '1'
    Executa a limpeza e realiza as seguintes validações:
    - Confirma que o processo não exibe a mensagem "Executando..." no tempo limite de 30 segundos
    - Verifica se o log de resultados contém a mensagem "Nenhum registro excluído Empresa:9999 Filial:1"
    Finaliza o teste saindo do sistema.
    """
    print(test_limpar_apuracao_icms.__name__)
    print(test_limpar_apuracao_icms.__doc__)
    page = set_up_page
    limpar_apuracao = TelaLimpezaApuracaoDosImpostosEstaduais(page)
    limpar_apuracao.acessar_limpeza_apuracao_impostos_estaduais()
    limpar_apuracao.limpar_apuracao_impostos_estatuais(
        data_inicial='01/01/2023',
        data_final='31/01/2023',
        cod_empresa='9999',
        cod_filial='1',
        log_validar="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
    sair_cloud(page)
