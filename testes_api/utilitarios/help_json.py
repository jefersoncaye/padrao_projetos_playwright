import json

def salvar_json(resposta_json, caminho_arquivo_salvar):
    with open(caminho_arquivo_salvar, "w", encoding='utf-8') as arquivo:
        json.dump(resposta_json, arquivo, indent=4, ensure_ascii=False)

def abri_json(arquivo_json):
    with open(arquivo_json, "r", encoding='utf-8') as arquivo:
        return json.load(arquivo)

