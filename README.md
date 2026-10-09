# 🧁 Cupcake Gourmet — Projeto Integrador II

Sistema web responsivo de venda e gestão de cupcakes gourmet, desenvolvido como evolução do Projeto Integrador I.

## Stack
- Python + Flask
- Flask-SQLAlchemy + SQLAlchemy
- Flask-Login
- SQLite para desenvolvimento / PostgreSQL para hospedagem
- HTML5 + CSS3 + JavaScript
- Pytest
- Gunicorn para produção

## Funcionalidades
- catálogo, busca e categorias;
- cadastro/login;
- carrinho e checkout;
- pagamento simulado;
- pedidos e acompanhamento;
- controle de estoque;
- painel administrativo;
- cadastro, edição e ativação/desativação de produtos;
- gerenciamento de categorias;
- atualização de status dos pedidos.

## Executar localmente — Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```
Abra http://127.0.0.1:5000

## Testes
```powershell
pytest -q
```

## Administrador de demonstração
- E-mail: `admin@cupcakelocal.test`
- Senha: `Admin123!`

**Troque a senha antes de qualquer publicação pública.**

## Produção
O arquivo `render.yaml` já contém a configuração básica para um Web Service Flask no Render. Configure `SECRET_KEY` e `DATABASE_URL` no provedor.

## Documentação
Consulte `docs/` para backlog, UML, banco, testes, manual, roteiro do vídeo, relatório acadêmico e preparação para GitHub/hospedagem.

## Observação acadêmica
O pagamento é simulado. Resultados de testes com usuários devem ser preenchidos somente após execução real.

## Health check
A rota `/health` retorna JSON com status `ok` e pode ser usada pelo provedor para verificar a aplicação.

## Integração contínua
O GitHub Actions executa `pytest -q` a cada push e pull request.

## Licença
Projeto disponibilizado sob licença MIT para fins acadêmicos e de estudo.
