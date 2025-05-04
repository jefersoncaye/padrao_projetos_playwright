from page_objects.objetos_gerais import ObjetosGerais
from playwright.sync_api import expect


class TelaApuracaoDosImpostosEstaduais(ObjetosGerais):

    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.campo_data_inicial = page.get_by_role(
            "textbox", name="Informe a data inicial para apuração do imposto estadual")
        self.campo_data_final = page.get_by_role(
            "textbox", name="Informe a data final para apuração do imposto estadual")
        self.combobox_tipo_apuracao = page.get_by_role(
            "combobox", name="Tipo Apuração *")
        self.campo_empresa = page.get_by_role("textbox", name="Empresa *")
        self.label_resultado_busca_empresa = page.locator(
            "#ctrlPCODIGOEMPRESARESULTTEXT")
        self.campo_filial = page.get_by_role("textbox", name="Filial *")
        self.label_resultado_busca_filial = page.locator(
            "#ctrlPCODIGOESTABRESULTTEXT")

    def acessar_apuracao_impostos_estaduais(self):
        self.page.goto(
            self.construir_link(
                base_url='npmnFis/Processo?Scope={Class:%22TnFisDPApurarImpEstadual%22,pathName:%22OBRIGACOES_FISCAL_APURACOESDEIMPOSTOS_APURACAO%22}'))
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(2000)

    def apurar_impostos_estaduais(
            self,
            data_inicial,
            data_final,
            tipo_apuracao,
            cod_empresa,
            cod_filial,
            descicao_filial='',
            descricao_empresa='',
            log_validar='Operação Concluída!'):
        if data_inicial:
            self.campo_data_inicial.fill(data_inicial)
        if data_final:
            self.campo_data_final.fill(data_final)
        if tipo_apuracao:
            self.combobox_tipo_apuracao.select_option(label=tipo_apuracao)
        if cod_empresa:
            self.campo_empresa.fill(cod_empresa)
        if descricao_empresa:
            expect(self.label_resultado_busca_empresa).to_have_text(
                descricao_empresa)
        if cod_filial:
            self.campo_filial.fill(cod_filial)
        if descicao_filial:
            expect(self.label_resultado_busca_filial).to_have_text(
                descicao_filial)
        self.botao_executar.click()
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)
        expect(
            self.page.get_by_role(
                "heading",
                name="Resultados")).to_be_visible(
            timeout=120000)
        self.page.wait_for_timeout(2000)
        if log_validar:
            self.abrir_logs_resultados()
            expect(
                self.label_log_resultado).to_contain_text(
                log_validar, timeout=15000)


class TelaLimpezaApuracaoDosImpostosEstaduais(ObjetosGerais):

    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.campo_data_inicial = page.get_by_role(
            "textbox", name="Informe a data inicial da apuração do ICMS")
        self.campo_data_final = page.get_by_role(
            "textbox", name="Informe a data final da apuração do ICMS")
        self.combobox_tipo_apuracao = page.get_by_role(
            "combobox", name="Tipo da Apuração *")
        self.campo_empresa = page.get_by_role("textbox", name="Empresa *")
        self.label_resultado_busca_empresa = page.locator(
            "#ctrlPCODIGOEMPRESARESULTTEXT")
        self.campo_filial = page.get_by_role("textbox", name="Filial *")
        self.label_resultado_busca_filial = page.locator(
            "#ctrlPCODIGOESTABRESULTTEXT")

    def acessar_limpeza_apuracao_impostos_estaduais(self):
        self.page.goto(
            self.construir_link(
                base_url='/npmnFis/Processo?Scope={Class:"TnFisDPLimparApuracaoICMS",pathName:"OBRIGACOES_FISCAL_APURACOESDEIMPOSTOS_APURACAO"}'))
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(2000)

    def limpar_apuracao_impostos_estatuais(
            self,
            data_inicial,
            data_final,
            cod_empresa,
            cod_filial,
            descicao_filial='',
            descricao_empresa='',
            log_validar='Operação Concluída!'):
        if data_inicial:
            self.campo_data_inicial.fill(data_inicial)
        if data_final:
            self.campo_data_final.fill(data_final)
        if cod_empresa:
            self.campo_empresa.fill(cod_empresa)
            self.campo_empresa.press('Enter')
            self.page.wait_for_load_state()
            self.page.wait_for_timeout(2000)
        if descricao_empresa:
            expect(self.label_resultado_busca_empresa).to_have_text(
                descricao_empresa)
        if cod_filial:
            self.campo_filial.fill(cod_filial)
        if descicao_filial:
            expect(self.label_resultado_busca_filial).to_have_text(
                descicao_filial)
        self.botao_executar.click()
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(2000)
        expect(
            self.page.get_by_role(
                "heading",
                name="Resultados")).to_be_visible(
            timeout=120000)
        self.page.wait_for_timeout(2000)
        if log_validar:
            self.abrir_logs_resultados()
            expect(
                self.label_log_resultado).to_contain_text(
                log_validar, timeout=15000)
