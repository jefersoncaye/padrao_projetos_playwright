import json
import config_global


class ObjetosGerais:

    def __init__(self, page):
        self.page = page
        self.botao_salvar_cadastro = page.get_by_role("button", name="SALVAR")
        self.botao_novo_registro = page.get_by_role("button", name="add")
        self.mensagem_avisos = page.locator('.toast-message')
        self.mensagem_avisos_framemodal = page.frame_locator(
            "#framemodal").locator('.toast-message')
        self.botao_sim = page.get_by_role("button", name="Sim")
        self.botao_nao = page.get_by_role("button", name="Não")
        self.botao_ok = page.get_by_role("button", name="OK")
        self.botao_sair = page.get_by_role("button", name="Close")
        self.botao_anterior = page.get_by_role('button', name='ANTERIOR')
        self.botao_proximo = page.get_by_role('button', name='PRÓXIMO')
        self.botao_executar = page.get_by_role("button", name="EXECUTAR")
        self.botao_cancelar = page.get_by_role("button", name="CANCELAR")
        self.botao_executar_framemodal = page.frame_locator("#framemodal").get_by_role("button", name="EXECUTAR")
        self.botao_acoes = page.get_by_role("button", name="AÇÕES")
        self.opcao_exportar_botao_acoes_relatorios =page.get_by_role("button", name="Exportar")
        self.opcao_acoes_consultar = page.locator("a").locator(
            '.navi-text:visible').get_by_text('Consultar', exact=True)
        self.opcao_acoes_novo = page.get_by_role("button", name=" Novo").first
        self.opcao_acoes_atualizar = page.locator("a").filter(
            has=page.get_by_text('Atualizar', exact=True))
        self.opcao_acoes_excluir = page.locator(
            ".dropdown-menu").get_by_role(
            "button", name="Excluir")
        self.opcao_acoes_atualizar_valores = page.locator(
            "a").filter(has_text="Atualizar os valores")
        self.botao_avancar = page.get_by_role('button', name='AVANÇAR')
        self.botao_confirmar = page.get_by_role('button', name='CONFIRMAR')
        self.botao_concluir = page.get_by_role('button', name='Concluir')
        self.label_resultados = page.get_by_role("heading", name="Resultados")
        self.label_avisos = page.get_by_role("heading", name="Avisos")
        self.label_log_resultado = page.locator('#widget_tree_TreeView')
        self.label_log_resultado_framemodal = page.frame_locator(
            "#framemodal").locator('#widget_tree_TreeView')
        self.linhas_grid = page.get_by_label('Grelha de dados').locator(
            '.dx-datagrid-rowsview tr.dx-row:visible')
        self.botao_selecionar = page.get_by_role('button', name='SELECIONAR')
        self.botao_gerar_evento_esocial = page.get_by_role(
            "button", name="GERAR EVENTO ESOCIAL")
        self.botao_download = page.locator('.la-cloud-download')
        self.botao_editar_registro_grid = page.get_by_role(
            "button", name="las la-pen")
        self.botao_excluir_registro_grid = page.get_by_role(
            "button", name="la-trash")
        self.botao_inserir_registro_grid = page.get_by_role("button", name="Base64")
        self.desmarcar_todos = page.locator(
            '.context-menu-item:visible').get_by_text("Desmarcar Todos", exact=True)
        self.marcar_todos = page.locator(
            '.context-menu-item:visible').get_by_text("Marcar Todos", exact=True)
        self.desmarcar_todos_iframe = page.frame_locator("#framemodal").locator(
            '.context-menu-item:visible').get_by_text("Desmarcar Todos", exact=True)
        self.marcar_todos_iframe = page.frame_locator("#framemodal").locator(
            '.context-menu-item:visible').get_by_text("Marcar Todos", exact=True)
        self.botao_salvar_cadastro_framemodal = page.frame_locator(
            "#framemodal").get_by_role("button", name=" SALVAR")
        self.opcao_acoes_excluir_framemodal =  page.locator("#framemodal").content_frame.get_by_role("button", name="Base64")

        self.botao_sim_framemodal = page.frame_locator(
            "#framemodal").get_by_role("button", name="Sim")
        self.mensagem_motivo_erro = page.locator(
            '.bootbox-body .justify-content-center .example-compact .example-code-on .example-highlight')
        self.linhas_grid_iframe = page.frame_locator("#framemodal").get_by_label(
            'Grelha de dados').locator('.dx-datagrid-rowsview tr.dx-row:visible')
        self.menu_selecao = page.locator(
            '.dx-item:visible').or_(page.locator('.navi-item:visible'))
        self.botao_voltar = page.get_by_role("button", name="Voltar")
        self.botao_50_itens_grid = page.get_by_role(
            "button", name="Display 50 items on page")
        self.botao_10_itens_grid = page.get_by_role(
            "button", name="Display 10 items on page")
        self.botao_500_itens_grid = page.get_by_role(
            "button", name="Display 500 items on page")
        self.botao_100_itens_grid = page.get_by_role(
            "button", name="Display 100 items on page")
        self.botao_opcoes_do_grid = page.get_by_label("las la-th")
        self.botao_pesquisa = page.locator("#kt_quick_search_toggle i").first
        self.campo_pesquisa = page.get_by_role("textbox", name="Pesquisar...")
        self.botao_home_cloud = page.locator('a.header-logo')
        self.botao_visualizar_exec_agendamento = page.get_by_label("Base64").nth(2)
        self.label_element = page.locator(".dx-calendar-caption-button .dx-button-text")
        self.botao_avancar_direita_calendario = page.get_by_label("chevronright")
        self.botao_avancar_esquerda_calendario = page.get_by_label("chevronleft")

    def abrir_logs_resultados(self):
        while self.page.locator(
                '.jstree-closed').first.is_visible(timeout=5000):
            self.page.locator(
                '.jstree-closed').first.locator('.jstree-icon').first.click()

    def abrir_logs_resultados_iframe(self):
        while self.page.frame_locator("#framemodal").locator(
                '.jstree-closed').first.is_visible(timeout=5000):
            self.page.frame_locator("#framemodal").locator(
                '.jstree-closed').first.locator('.jstree-icon').first.click()

    def pesquisar_valor_grid(
            self,
            texto_linha_buscar,
            indice_linha=0,
            coluna_buscar=1):
        if coluna_buscar:
            return self.page.get_by_role('row').filter(
                has_text=texto_linha_buscar).nth(indice_linha).locator(
                f'[aria-colindex="{coluna_buscar}"]')
        else:
            return self.page.get_by_role('row').filter(
                has_text=texto_linha_buscar).nth(indice_linha)

    def pesquisar_valor_grid_iframe(
            self,
            texto_linha_buscar,
            indice_linha=0,
            coluna_buscar=1):
        if coluna_buscar:
            return self.page.frame_locator("#framemodal").get_by_role('row').filter(
                has_text=texto_linha_buscar).nth(indice_linha).locator(
                f'[aria-colindex="{coluna_buscar}"]')
        else:
            return self.page.get_by_role('row').filter(
                has_text=texto_linha_buscar).nth(indice_linha)

    @staticmethod
    def acessar_home(page):
        page.goto(
            ObjetosGerais.construir_link(base_url=f"http://{config_global.servidor_global}:8080/npmnGem/Default?"))

    def selecionar_data_calendario(self, ano='', mes='', dia=''):
        lista_meses = [
            'janeiro',
            'fevereiro',
            'março',
            'abril',
            'maio',
            'junho',
            'julho',
            'agosto',
            'setembro',
            'outubro',
            'novembro',
            'dezembro']
        nome_mes = lista_meses[int(mes) - 1]
        periodo = self.page.locator(
            f'.dx-calendar-body td[data-value="{ano}/{mes}/{dia}"]:visible').first
        self.page.locator(
            '#widget_Agenda .tw-agenda-left .btn-text-dark').click()
        self.page.locator(
            '.dx-calendar-navigator .dx-calendar-caption-button').click()
        self.page.locator(
            '.dx-calendar-navigator .dx-calendar-caption-button').click()

        intervalo_texto = self.label_element.inner_text()
        ano_inicio, ano_fim = map(int, intervalo_texto.split('-'))

        if int(ano) > ano_fim:
            self.botao_avancar_direita_calendario.click()
        elif int(ano) < ano_inicio:
            self.botao_avancar_esquerda_calendario.click()
        if self.page.get_by_label(ano, exact=True).first.is_visible():
            self.page.get_by_label(ano, exact=True).first.click()
        else:
            print('não encontrei o ano')
        if self.page.get_by_label(
                f'{nome_mes} de {ano}',
                exact=True).is_visible():
            self.page.get_by_label(f'{nome_mes} de {ano}', exact=True).click()
        else:
            print('não encontrei o mes')
        if periodo.is_visible():
            periodo.click()
        else:
            print('não encontrei o dia')
        self.botao_confirmar.click()

    def clicar_menu_selecao(self, texto):
        self.menu_selecao.get_by_text(texto).click()

    def restaurar_colunas_grid(self):
        self.botao_opcoes_do_grid.click()
        self.page.get_by_text("Restaurar colunas").click()
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state()

    @staticmethod
    def construir_link(base_url, arquivo_json="D:\workspace\TestesWeb\Cloud\parametros_sessao.json"):
        try:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                parametros = json.load(arquivo)

            empresa = parametros.get("empresa", None) or None
            filial = parametros.get("filial", None) or None
            periodo_calculo = parametros.get("periodo_calculo", None) or None
            data_inicial = parametros.get("data_inicial", None) or None
            data_final = parametros.get("data_final", None) or None

            selecao = {
                "CODIGOEMPRESA": empresa,
                "CODIGOESTAB": filial,
                "CODIGOPERCALCULO": periodo_calculo,
                "DATALCTOFIS_MAIORIGUAL": data_inicial,
                "DATALCTOFIS_MENORIGUAL": data_final
            }

            selecao_str = json.dumps(selecao)  # Transforma em JSON string e já está no formato correto

            # Verifica se já existe '?' na URL base
            separador = '?' if '?' not in base_url else '&'

            full_url = f"{base_url}{separador}selecao={selecao_str}"

            return full_url
        except FileNotFoundError:
            print(f"Erro: Arquivo {arquivo_json} não encontrado.")
        except json.JSONDecodeError:
            print("Erro: O arquivo JSON está mal formatado.")

    def expandir_itens_grid(self):
        while self.page.locator(".dx-datagrid-group-closed").first.is_visible():
            self.page.locator(".dx-datagrid-group-closed").first.click(force=True)
            self.page.wait_for_timeout(500)

    def acessar_rotina_por_pesquisa(self, rotina, timeout=120000):
        self.botao_pesquisa.click()
        self.campo_pesquisa.fill(rotina)
        self.campo_pesquisa.press('Enter')
        self.page.get_by_role("link", name=rotina).click(timeout=timeout)
        self.page.wait_for_timeout(4000)
        self.page.wait_for_load_state()
