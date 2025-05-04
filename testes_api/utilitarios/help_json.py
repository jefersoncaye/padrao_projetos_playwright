import json

def salvar_json(resposta_json, caminho_arquivo_salvar, encoding=None):
    if encoding:
        with open(caminho_arquivo_salvar, "w", encoding=encoding) as arquivo:
            json.dump(resposta_json, arquivo, indent=4, ensure_ascii=False)
    else:
        with open(caminho_arquivo_salvar, "w") as arquivo:
            json.dump(resposta_json, arquivo, indent=4, ensure_ascii=False)

def abri_json(arquivo_json, encoding=None):
    if encoding:
        with open(arquivo_json, "r", encoding=encoding) as arquivo:
            return json.load(arquivo)
    else:
        with open(arquivo_json, "r") as arquivo:
            return json.load(arquivo)

