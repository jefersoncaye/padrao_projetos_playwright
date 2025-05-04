import psycopg2
import fdb
import sys
import os
import datetime
from decimal import Decimal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_global

if config_global.in_jenkins:
    arquivo_conexao = open(fr'\\{config_global.servidor_global}\Tributario\Questor.Conexao.ini',
                           'r').read().strip()
else:
    arquivo_conexao = open(r'D:\workspace\Tributario\Questor.Conexao.ini',
                           'r').read().strip()

servidor_postgre = 'apus'
servidor_firebird = 'hydra'
porta_postgre = '5432'
usuario_postgre = 'xxxxxx'
usuario_firebird = 'xxxxxx'
senha = 'xxxxxxx'


def criar_conexao_banco_postgre(servidor, porta, usuario, senha, database):
    try:
        conexao = psycopg2.connect(
            database=database,
            user=usuario,
            password=senha,
            host=servidor,
            port=porta
        )
        return conexao
    except BaseException:
        exit('Erro ao Conectar no Servidor, verifique as credenciais!')


def criar_conexao_banco_firebird(servidor, usuario, senha, database):
    try:
        conexao = fdb.connect(
            dsn=f'{servidor}:{database}',
            user=usuario,
            password=senha
        )
        return conexao
    except BaseException:
        exit('Erro ao Conectar no Servidor, verifique as credenciais!')


def executar_comando_sql(
        comando_sql_postre, comando_sql_firebird='',
        banco_dados_postgre='',
        caminho_banco_dados_firebird=''):
    comando_sql = ''
    comando_sql_postre.replace(
        'select',
        'SELECT').replace(
        'update',
        'UPDATE').replace(
        'insert',
        'INSERT').replace(
        'delete',
        'DELETE').replace(
        'from',
        'FROM').replace(
        'where',
        'WHERE')
    comando_sql_firebird.replace(
        'select',
        'SELECT').replace(
        'update',
        'UPDATE').replace(
        'insert',
        'INSERT').replace(
        'delete',
        'DELETE').replace(
        'from',
        'FROM').replace(
        'where',
        'WHERE')
    conexao = ''
    comando_sql = comando_sql_postre
    conexao = criar_conexao_banco_postgre(
        servidor=servidor_postgre,
        porta=porta_postgre,
        usuario=usuario_postgre,
        senha=senha,
        database=banco_dados_postgre)

    cursor = conexao.cursor()
    cursor.execute(comando_sql)
    if 'SELECT' not in comando_sql:
        conexao.commit()
    return cursor

def normalizar_valores(valor):
    if isinstance(valor, Decimal):
        return float(valor)
    elif isinstance(valor, (datetime.date, datetime.datetime)):
        return valor.isoformat()
    else:
        return valor

def buscar_dados_com_colunas(cursor):
    nomes_colunas = [desc[0] for desc in cursor.description]

    resultados = cursor.fetchall()

    resultados_normalizados = [
        [normalizar_valores(valor) for valor in linha]
        for linha in resultados
    ]

    return [nomes_colunas] + resultados_normalizados

def salvar_tabela_em_arquivo_formatado(dados, caminho_arquivo):
    num_colunas = len(dados[0])

    larguras_colunas = [0] * num_colunas
    for linha in dados:
        for idx, celula in enumerate(linha):
            larguras_colunas[idx] = max(larguras_colunas[idx], len(str(celula)))

    def formatar_linha(linha):
        return " | ".join(str(celula).ljust(larguras_colunas[idx]) for idx, celula in enumerate(linha))

    linhas = []
    cabecalho = formatar_linha(dados[0])
    separador = "-+-".join("-" * larguras_colunas[idx] for idx in range(num_colunas))
    linhas.append(cabecalho)
    linhas.append(separador)
    for linha in dados[1:]:
        linhas.append(formatar_linha(linha))

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")

