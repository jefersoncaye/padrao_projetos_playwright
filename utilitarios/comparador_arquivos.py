import re
from openpyxl import load_workbook
import pandas as pd


def comparar_arquivos(arquivo_base, arquivo_atual, linhas_ignorar=None, padrao_ignorar='', bytes_ignorar=0):
    """
    Faz a comparação linha por linha de dois arquivos
    Caso algum arquivo tenha linhas a mais, será apresentado a mensagem "Os arquivos têm tamanhos diferentes, podem existir mais diferenças!"
    Caso seja necessario uma ou mais linhas especificas do arquivo, passar linhas em forma de lista no parametro "linhas_ignorar"
    Caso queira ignorar tag ou algum padrão, passar na variavel 'padrao_ignorar' (precisa ser um padrão ReGex)
    Caso queira ignorar uma quantidade de bytes especifica, passar o parametro bytes_ignorar, lembrar de alterar no arquivo base para sempre ser um caracter diferente
    """
    if linhas_ignorar is None:
        linhas_ignorar = []
    with open(arquivo_base, 'r', encoding='latin-1') as f1, open(arquivo_atual, 'r', encoding='latin-1') as f2:
        linhas_arquivo1 = f1.readlines()
        linhas_arquivo2 = f2.readlines()
    tem_diferenca = False
    bytes_diferenca = 0
    for i, (linha1, linha2) in enumerate(zip(linhas_arquivo1, linhas_arquivo2)):
        if (i + 1) in linhas_ignorar:
            continue
        if padrao_ignorar:
            linha1 = re.sub(padrao_ignorar, '', linha1, flags=re.DOTALL)
            linha2 = re.sub(padrao_ignorar, '', linha2, flags=re.DOTALL)
        if linha1 != linha2:
            print(f'Diferença na linha {i + 1}:')
            print(f'Arquivo Base:  {linha1.strip()}')
            print(f'Arquivo Atual: {linha2.strip()}')
            bytes_linha1 = linha1.encode()
            bytes_linha2 = linha2.encode()
            max_len = max(len(bytes_linha1), len(bytes_linha2))
            for j in range(max_len):
                try:
                    if bytes_linha1[j] != bytes_linha2[j]:
                        bytes_diferenca += 1
                except IndexError:
                    bytes_diferenca += 1
            if bytes_diferenca > bytes_ignorar or bytes_ignorar == 0:
                tem_diferenca = True

    assert len(linhas_arquivo2) > 0, 'Arquivo atual está em branco, Verifique!'

    assert len(linhas_arquivo1) == len(
        linhas_arquivo2), 'Os arquivos têm tamanhos diferentes, podem existir mais diferenças!'

    if not tem_diferenca:
        print(f'\nArquivos {arquivo_base} e {arquivo_atual} são iguais!, estão sendo ignorados {bytes_ignorar} Bytes')

    assert not tem_diferenca, f'\nArquivos com diferenças' \
                              f'\n{bytes_diferenca} Bytes de diferença!, foi configurado para ignorar {bytes_ignorar} Bytes' \
                              f'\nPara mais informações compare os arquivos Base: {arquivo_base} e Atual: {arquivo_atual} ' \
                              f'com algum utilitario de sua preferencia'
    assert bytes_ignorar == bytes_diferenca, (
        f'A quantidade de bytes a ingorar não é a mesma que a diferença de bytes entre os arquivos, verifique!\n'
        f'Bytes ignorar: {bytes_ignorar}\n'
        f'Bytes diferença: {bytes_diferenca}')


def comparar_arquivos_excel(arquivo_base, arquivo_atual, bytes_ignorar=0):
    # Detectar extensão e escolher engine
    engine_base = 'xlrd' if arquivo_base.endswith('.xls') else 'openpyxl'
    engine_atual = 'xlrd' if arquivo_atual.endswith('.xls') else 'openpyxl'

    df_base = pd.read_excel(arquivo_base, engine=engine_base).fillna('')
    df_atual = pd.read_excel(arquivo_atual, engine=engine_atual).fillna('')

    tem_diferenca = False
    bytes_diferenca = 0

    if df_base.shape != df_atual.shape:
        raise AssertionError("As planilhas não têm o mesmo tamanho, podem existir mais diferenças")

    for row_idx in range(df_base.shape[0]):
        for col_idx in range(df_base.shape[1]):
            cell1 = str(df_base.iat[row_idx, col_idx])
            cell2 = str(df_atual.iat[row_idx, col_idx])
            if cell1 != cell2:
                print(f'Diferença na linha {row_idx + 1}, coluna {col_idx + 1}:')
                print(f'Arquivo Base:  {cell1}')
                print(f'Arquivo Atual: {cell2}')
                max_len = max(len(cell1.encode()), len(cell2.encode()))
                for j in range(max_len):
                    try:
                        if cell1.encode()[j] != cell2.encode()[j]:
                            bytes_diferenca += 1
                    except IndexError:
                        bytes_diferenca += 1
                if bytes_diferenca > bytes_ignorar or bytes_ignorar == 0:
                    tem_diferenca = True

    if not tem_diferenca:
        print(f'\nArquivos {arquivo_base} e {arquivo_atual} são iguais!, estão sendo ignorados {bytes_ignorar} Bytes')

    assert not tem_diferenca, (
        f'\nArquivos com diferenças'
        f'\n{bytes_diferenca} Bytes de diferença!, foi configurado para ignorar {bytes_ignorar} Bytes'
        f'\nPara mais informações compare os arquivos Base: {arquivo_base} e Atual: {arquivo_atual} '
        f'com algum utilitário de sua preferência'
    )

    assert bytes_ignorar == bytes_diferenca, (
        f'A quantidade de bytes a ignorar não é a mesma que a diferença de bytes entre os arquivos, verifique!\n'
        f'Bytes ignorar: {bytes_ignorar}\n'
        f'Bytes diferença: {bytes_diferenca}'
    )