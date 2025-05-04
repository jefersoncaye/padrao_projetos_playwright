from utilitarios.login_cloud import iniciar_nserver_config, converter_base, restaurar_backup_postgre, ler_arquivo_configuracao, atualizar_personalizacao
from utilitarios.backup_restore_postgre_jenkins import criar_backup_postgre
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_global

def login_api(api_request_context, base):
    arquivo_conexao = open(r'D:\workspace\Tributario\Questor.Conexao.ini',
                           'r').read().strip()
    fazer_bkp_global, restaurar_bkp_global = ler_arquivo_configuracao(modulo='api')
    storage_state = r'padrao_projetos_playwright\playwright\auth\state.json'
    restaurar_bkp_job = False
    token_api = None
    if os.path.isfile(r'padrao_projetos_playwright\restaurarBackupJob.txt'):
        restaurar_bkp_job = True
    if not token_api:
        if restaurar_bkp_job:
            if 'TipoBancoDados=PostgreSQL' in arquivo_conexao:
                restaurar_backup_postgre(
                    pasta='backupAtual',
                    base=f'db{base}')
        elif restaurar_bkp_global.lower() != 'nao':
            if 'TipoBancoDados=PostgreSQL' in arquivo_conexao:
                restaurar_backup_postgre(
                    pasta=restaurar_bkp_global,
                    base=f'db{base}')
        if not os.path.isfile(storage_state):
            if not config_global.in_jenkins:
                iniciar_nserver_config()
            converter_base(conexao=base)
            atualizar_personalizacao(conexao=base)
        print(f'\nPOST para url: home/LoginModulo?LogonName=administrador@{base}&PlainPassword=masterkey')
        request = api_request_context.post(
            f'home/LoginModulo?LogonName=administrador@{base}&PlainPassword=masterkey')
        print(f'O retorno foi:\n'
              f'code: {request.status}, \n\nbody: {request.json()}, \n\nheaders: {request.headers}')
        print('\n\n-----Fim do Login-----\n\n')
        token_api = request.json()['Token']
        assert request.status == 200
        assert token_api
        if fazer_bkp_global.lower() != 'nao':
            if 'TipoBancoDados=PostgreSQL' in arquivo_conexao:
                criar_backup_postgre(
                    base=f'db{base}',
                    pasta=fazer_bkp_global)
        return token_api
    else:
        return token_api
