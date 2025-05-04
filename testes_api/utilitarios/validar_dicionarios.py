def validar_schema_dicionario(
        dicionario_base,
        dicionario_atual,
        chave_atual='',
        diferencas=None):
    if diferencas is None:
        diferencas = []

    if isinstance(dicionario_base, dict) and isinstance(dicionario_atual, dict):
        # Verifica as chaves que estão no dicionário base, mas não no
        # dicionário atual
        for chave_base in dicionario_base.keys():
            if chave_base not in dicionario_atual:
                diferencas.append(
                    f"Chave '{chave_base}' não encontrada no dicionário atual.")

        # Verifica as chaves que estão no dicionário atual, mas não no
        # dicionário base
        for chave_atual in dicionario_atual.keys():
            if chave_atual not in dicionario_base:
                diferencas.append(
                    f"Chave '{chave_atual}' não encontrada no dicionário base.")

        # Verifica os valores para as chaves que estão presentes em ambos os
        # dicionários
        for chave_base, elemento_base in dicionario_base.items():
            if chave_base in dicionario_atual:
                elemento_atual = dicionario_atual[chave_base]
                if not isinstance(elemento_base, type(elemento_atual)):
                    diferencas.append(
                        f"Tipo de dado diferente para a chave '{chave_base}': "
                        f"Esperado {type(elemento_base)}, encontrado {type(elemento_atual)}")
                elif isinstance(elemento_base, dict) or isinstance(elemento_base, list):
                    validar_schema_dicionario(
                        elemento_base, elemento_atual, chave_base, diferencas)

    elif isinstance(dicionario_base, list) and isinstance(dicionario_atual, list):
        if len(dicionario_base) != len(dicionario_atual):
            diferencas.append(
                f"Existe uma diferença de tamanho na lista da chave '{chave_atual}': "
                f"Esperado {len(dicionario_base)}, encontrado {len(dicionario_atual)}")
        else:
            for (item_base, item_atual) in (
                    zip(dicionario_base, dicionario_atual)):
                validar_schema_dicionario(
                    item_base, item_atual, chave_atual, diferencas)

    elif not isinstance(dicionario_base, list) and not isinstance(dicionario_base, dict):
        if not isinstance(dicionario_base, type(dicionario_atual)):
            diferencas.append(
                f"Foi encontrado um tipo de dado diferente "
                f"esperado tipo: {type(dicionario_base)}, valor: {dicionario_base}, "
                f"encontrado tipo: {type(dicionario_atual)}, valor: {dicionario_atual}, "
                f"necessario verificar!")

    else:
        assert False, f'Ocorreu algum erro, necessario verificar a validação!"'

    return diferencas


def validar_headers_padrao(dicionario):
    assert 'charset=UTF-8' in dicionario['content-type']
    assert dicionario['accept-encoding'] == 'synlz,gzip'
