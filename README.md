# Padrão de Projetos com Playwright

Este repositório apresenta um modelo estruturado para projetos de automação de testes utilizando Playwright com Python. A proposta é fornecer uma base organizada e escalável, com separação clara entre testes, objetos de página, utilitários e configurações.

## Estrutura do Projeto

```bash
padrao_projetos_playwright/
├── page_objects/                  # Objetos de página reutilizáveis
│   └── exemplo_objeto.py
├── stores/
│   └── fiscal/
│       └── apuracao_de_impostos/
│           └── test_exemplo/     # Arquivos Utilizados nos testes (para importação ou validações)
├── testes/
│   └── fiscal/
│       └── apuracao_de_impostos/ # Pastas para organização dos testes conforme sistemas
│           └── test_exemplo.py   # Testes de funcionalidades específicas
├── testes_api/                   # Testes automatizados de APIs
│   └── test_exemplo_api.py
├── utilitarios/                  # Funções auxiliares para os testes
│   └── banco.py
│   └── login.py
├── conftest.py                   # Fixtures e configurações do Pytest
├── pytest.ini                    # Configurações globais do Pytest
├── requirements.txt              # Dependências do projeto
```

## Como usar este modelo

1. Clone o repositório:
   ```bash
   git clone https://github.com/jefersoncaye/padrao_projetos_playwright.git
   cd padrao_projetos_playwright
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   cd venv/bin/activate 
   pip install -r requirements.txt
   ```
3. Instale os navegadores do Playwright:
   ```bash
   playwright install
   ```
4. Faça os ajustes necessarios para seu sistema
5. Execute os testes:
   ```bash
   pytest ...
   ```
