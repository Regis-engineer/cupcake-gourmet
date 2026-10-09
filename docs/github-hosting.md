# GitHub e hospedagem

## 1. GitHub
Crie um repositório vazio, sem README, .gitignore ou licença pré-criados, e depois execute na pasta do projeto:

```bash
git init
git add .
git commit -m "feat: projeto integrador cupcake gourmet"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/cupcake-gourmet.git
git push -u origin main
```

O GitHub recomenda criar o repositório remoto vazio ao importar um projeto existente para evitar conflitos e depois fazer `git push -u origin main`.

## 2. Render
O Render permite Web Services Python gratuitos e integração direta com GitHub. O comando de build é `pip install -r requirements.txt` e o serviço pode ser iniciado com Gunicorn.

Para este projeto, use:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn wsgi:app`
- Environment: `SECRET_KEY` gerada pelo provedor
- `DATABASE_URL`: URL do PostgreSQL

**Atenção:** o PostgreSQL gratuito do Render expira após 30 dias e tem limite de 1 GB; portanto, para um projeto acadêmico que precise permanecer disponível, prefira um PostgreSQL externo no plano gratuito.

## 3. Neon + Render
Uma opção atual é manter o Web Service no Render e o PostgreSQL no Neon. Em outubro de 2026, o Neon informa 1 GB de armazenamento PostgreSQL por projeto no Free Plan.

Depois de criar o banco no Neon, copie a connection string para a variável `DATABASE_URL` no Render.

## 4. Segurança
Nunca publique senha de administrador, API keys, `SECRET_KEY` real ou connection strings no GitHub. Use variáveis de ambiente.

## 5. Checklist de publicação
- [ ] testes locais executados;
- [ ] senha administrativa alterada;
- [ ] `SECRET_KEY` de produção configurada;
- [ ] PostgreSQL configurado;
- [ ] `DATABASE_URL` configurada;
- [ ] repositório público criado;
- [ ] primeiro push realizado;
- [ ] serviço conectado ao GitHub;
- [ ] deploy concluído;
- [ ] URL pública testada;
- [ ] cinco usuários realizaram validação;
- [ ] evidências e screenshots arquivados.


## 6. Verificação pós-deploy
Acesse `/health` e confirme resposta JSON semelhante a `{"status":"ok","service":"cupcake-gourmet"}`. Depois execute manualmente os fluxos de cadastro, login, catálogo, carrinho, checkout e administração.

## 7. Integração contínua
O arquivo `.github/workflows/tests.yml` executa a suíte automatizada em cada push e pull request.
