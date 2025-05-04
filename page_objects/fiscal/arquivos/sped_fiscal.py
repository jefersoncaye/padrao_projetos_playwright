from page_objects.objetos_gerais import ObjetosGerais
from playwright.sync_api import expect
from utilitarios.exportar_relatorios import exportar_relatorios
import os


class TelaSpedFiscal(ObjetosGerais):

    def __init__(self, page):
        super().__init__(page)
        self.page = page

        self.campo_empresa = page.get_by_role("textbox", name="Empresa *")
        self.campo_filial = page.get_by_role("textbox", name="Filial *")
        self.campo_data_inicial = page.locator(
            "#formFieldPDATAINICIALTnArqDPGerarArqSPEDFis").get_by_role("textbox", name="Data")
        self.campo_data_final = page.locator(
            "#formFieldPDATAFINALTnArqDPGerarArqSPEDFis").get_by_role("textbox", name="Data")
        self.combobox_gerar_registro_duplicatas = page.get_by_role(
            "combobox", name="Gerar Registros Duplicatas *")
        self.combobox_gerar_somente_registros_de_apuracao = page.get_by_role(
            "combobox", name="Gerar Somente Registros de Apuração *")
        self.combobox_gerar_registros_ciap = page.get_by_role(
            "combobox", name="Gerar Registros CIAP *")
        self.combobox_gerar_valores_pis_cofins = page.get_by_role(
            "combobox", name="Gerar Valores PIS e COFINS *")
        self.combobox_gerar_c170_para_modelo_55_emissao_propria = page.get_by_role(
            "combobox", name="Gerar C170 para Modelo 55 Emissão Própria *")
        self.combobox_gerar_bloco_k = page.get_by_role(
            "combobox", name="Gerar Bloco K *")
        self.combobox_gerar_registro_de_inventario = page.get_by_role(
            "combobox", name="Gerar Registros de Inventário *")
        self.campo_periodo_registro_inventario = page.locator(
            "#formFieldPPERIODOH005TnArqDPGerarArqSPEDFis")
        self.combobox_tipo_declaracao = page.get_by_role(
            "combobox", name="Tipo de declaraçäo *")
        self.combobox_gerar_registro_0210 = page.get_by_role(
            "combobox", name="Gerar Registro 0210 *")
        self.combobox_gerar_registro_0221 = page.get_by_label(
            "Gerar Registro 0221 *")
        self.campo_pessoa_juridica_do_contador = page.get_by_label(
            "Código Pessoa Jurídica do Contador  *")

    def acessar_sped_fiscal(self):
        self.page.goto(
            self.construir_link(
                base_url='npmnFis/Processo?Scope={Class:%22TnArqDPGerarArqSPEDFis%22,pathName:%22OBRIGACOES_FISCAL_GERARARQUIVOS%22}'))
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(2000)

    def gerar_sped_fiscal(
            self,
            cod_empresa='',
            cod_filial='',
            dt_inicial='',
            dt_final='',
            gerar_registro_duplicatas='',
            gerar_somente_registros_de_apuracao='',
            gerar_registros_ciap='',
            gerar_valores_pis_cofins='',
            gerar_c170_para_modelo_55_emissao_propria='',
            gerar_bloco_k='',
            gerar_registro_de_inventario='',
            periodo_registro_inventario='',
            tipo_declaracao='',
            pessoa_juridica_do_contador='',
            gerar_registro_0210='',
            gerar_registro_0221='',
            caminho_relatorio=''

    ):
        if 'TnArqDPGerarArqSPEDFis' not in self.page.url:
            self.acessar_sped_fiscal()

        if cod_empresa:
            self.campo_empresa.clear()
            self.campo_empresa.fill(cod_empresa)
        if cod_filial:
            self.campo_filial.clear()
            self.campo_filial.fill(cod_filial)
        if dt_inicial:
            self.campo_data_inicial.fill(dt_inicial)
        if dt_final:
            self.campo_data_final.fill(dt_final)
        if gerar_registro_duplicatas:
            self.combobox_gerar_registro_duplicatas.select_option(
                label=gerar_registro_duplicatas)
        if gerar_somente_registros_de_apuracao:
            self.combobox_gerar_somente_registros_de_apuracao.select_option(
                label=gerar_somente_registros_de_apuracao)
        if gerar_registros_ciap:
            self.combobox_gerar_registros_ciap.select_option(
                label=gerar_registros_ciap)
        if gerar_valores_pis_cofins:
            self.combobox_gerar_valores_pis_cofins.select_option(
                label=gerar_valores_pis_cofins)
        if gerar_c170_para_modelo_55_emissao_propria:
            self.combobox_gerar_c170_para_modelo_55_emissao_propria.select_option(
                label=gerar_c170_para_modelo_55_emissao_propria)
        if gerar_bloco_k:
            self.combobox_gerar_bloco_k.select_option(label=gerar_bloco_k)
        if gerar_registro_de_inventario:
            self.combobox_gerar_registro_de_inventario.select_option(
                label=gerar_registro_de_inventario)
            if gerar_registro_de_inventario.lower() == 'sim' and periodo_registro_inventario:
                self.campo_periodo_registro_inventario.fill(
                    periodo_registro_inventario)
        if gerar_registro_0210:
            self.combobox_gerar_registro_0210.select_option(
                label=gerar_registro_0210)
        if gerar_registro_0221:
            self.combobox_gerar_registro_0221.select_option(
                label=gerar_registro_0221)
        if tipo_declaracao:
            self.combobox_tipo_declaracao.select_option(label=tipo_declaracao)
        if pessoa_juridica_do_contador:
            self.campo_pessoa_juridica_do_contador.fill(
                pessoa_juridica_do_contador)
        self.botao_executar.click()
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)
        expect(
            self.page.get_by_role(
                "heading",
                name="Resultados")).to_be_visible(
            timeout=240000)
        expect(self.label_log_resultado).to_contain_text('.SPED')
        self.page.wait_for_timeout(2000)
        if caminho_relatorio:
            with self.page.expect_download() as download_info:
                self.botao_download.click()
            relatorio = download_info.value
            relatorio.save_as(caminho_relatorio)
