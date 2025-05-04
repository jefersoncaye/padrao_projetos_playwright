from asyncio import timeout

from page_objects.objetos_gerais import ObjetosGerais
from time import sleep
from playwright.sync_api import expect


class Dime(ObjetosGerais):

    def __init__(self, page):
        super().__init__(page)
        self.page = page

        self.combobox_tipo_periodo = page.locator("#ctrlPTIPODIME")
        self.campo_data_inicial = page.get_by_role(
            "textbox", name="Informe a data inicial de")
        self.combobox_gerar_arquivo = page.get_by_label("Gerar Arquivo *")
        self.campo_contador = page.get_by_label("Contador *")
        self.campo_empresa = page.get_by_role("textbox", name="Empresa")
        self.campo_filial = page.get_by_role("textbox", name="Filial")

    def acessar_tela_dime(self):
        self.page.goto(
            self.construir_link(
                base_url='/npmnFis/Processo?Scope={Class:"TnArqDPGerarArqDIME2006",pathName:"OBRIGACOES_FISCAL_ICMS_SC"}'))
        sleep(2)
        self.page.wait_for_load_state()

    def gerar_dime(
            self,
            tipo_periodo='',
            data_inicial='',
            gerar_arquivo='',
            contador='',
            empresa='',
            filial='',
            caminho_arquivo=''):
        if tipo_periodo:
            self.combobox_tipo_periodo.click()
            self.combobox_tipo_periodo.select_option(label=tipo_periodo)

        if data_inicial:
            self.campo_data_inicial.clear()
            self.campo_data_inicial.fill(data_inicial)

        if gerar_arquivo:
            self.combobox_gerar_arquivo.click()
            self.combobox_gerar_arquivo.select_option(label=gerar_arquivo)

        if contador:
            self.campo_contador.clear()
            self.campo_contador.fill(contador)

        if empresa:
            self.campo_empresa.clear()
            self.campo_empresa.fill(empresa)

        if filial:
            self.campo_filial.clear()
            self.campo_filial.fill(filial)

        self.botao_executar.click()

        expect(self.label_resultados).to_be_visible(timeout=60000)

        if caminho_arquivo:
            with self.page.expect_download() as download_info:
                self.botao_download.click()
            relatorio = download_info.value
            relatorio.save_as(caminho_arquivo)
