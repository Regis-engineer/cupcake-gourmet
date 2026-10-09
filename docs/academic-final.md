# Relatório acadêmico final — estrutura e conteúdo-base

## 1. Introdução
O projeto Cupcake Gourmet constitui a evolução do Projeto Integrador Transdisciplinar em Engenharia de Software I para uma aplicação web funcional. A proposta mantém o domínio de vendas de cupcakes gourmet e amplia o trabalho anterior para contemplar modelagem, IHC, frontend, backend, banco de dados, testes e validação.

## 2. Contextualização
O Projeto Integrador I concentrou-se no levantamento de requisitos, User Stories, Product Backlog, Scrum e definição do MVP. No Projeto Integrador II, esses artefatos são revisados e transformados em uma solução implementada.

## 3. Problema
Como desenvolver um sistema web simples, responsivo e de fácil utilização que permita apresentar cupcakes gourmet, receber pedidos, organizar informações dos clientes e auxiliar o estabelecimento no gerenciamento das vendas?

## 4. Justificativa
A solução permite aplicar conhecimentos de Engenharia de Software em um domínio pequeno e controlável, possibilitando demonstrar requisitos, modelagem, desenvolvimento, persistência, segurança básica, testes e validação.

## 5. Objetivo geral
Desenvolver um sistema web responsivo para comercialização de cupcakes gourmet, permitindo aos clientes consultar produtos, montar pedidos e acompanhar suas compras, enquanto disponibiliza ao administrador recursos de gestão.

## 6. Objetivos específicos
Consultar a especificação principal em `docs/product-backlog.md` e o documento-base do projeto.

## 7. Metodologia
O projeto utiliza a organização por backlog e User Stories herdada do PI I, com desenvolvimento incremental do MVP e validação posterior com usuários.

## 8. Requisitos
Os requisitos funcionais, não funcionais e regras de negócio estão documentados no projeto-base.

## 9. IHC
A interface prioriza clareza, consistência, feedback, responsividade e facilidade de navegação. Os protótipos e fluxos encontram-se em `docs/prototipos/`.

## 10. UML
Os diagramas de casos de uso e classes estão em `docs/uml/`.

## 11. Banco de dados
O modelo relacional contém usuários, categorias, produtos, endereços, pedidos, itens de pedido e pagamentos. O script está em `database/schema.sql`.

## 12. Arquitetura
A aplicação utiliza Flask com separação entre modelos, rotas/controllers e serviços, apoiada por SQLAlchemy e Flask-Login.

## 13. Desenvolvimento
A aplicação implementa catálogo, autenticação, carrinho, checkout, pagamento simulado, pedidos, estoque e administração.

## 14. Testes
A suíte automatizada cobre navegação, catálogo, validação de cadastro, estoque, checkout, criação de pagamento/pedido, edição administrativa e controle de acesso. Os resultados devem ser registrados após execução no ambiente do aluno.

## 15. Validação com cinco usuários
Os cinco participantes devem executar tarefas definidas em `docs/testes/feedback-5-usuarios.md`. Os resultados reais devem ser anexados ao relatório.

## 16. Melhorias
Após a validação, registrar cada problema encontrado, sua causa, correção e evidência de reteste.

## 17. Resultados
Esta seção deve ser preenchida com evidências reais: screenshots, resultados de testes automatizados, feedback dos cinco usuários e URL pública.

## 18. Conclusão
O projeto demonstra a evolução de uma especificação inicial para uma solução de software implementada, testável e passível de validação com usuários.

## 19. Referências
- Material didático do Projeto Integrador Transdisciplinar em Engenharia de Software II.
- Projeto Integrador Transdisciplinar em Engenharia de Software I — Reginaldo Oliveira da Silva.
- Documentação oficial do Flask, SQLAlchemy, GitHub e provedor de hospedagem utilizados.


> **Nota de implementação:** o ORM utiliza a entidade `User` e cria automaticamente o banco no desenvolvimento. O `database/schema.sql` representa o modelo físico de referência para PostgreSQL; nomes reservados são evitados no SQL manual (`app_user` e `orders`).
