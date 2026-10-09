# Matriz de rastreabilidade

| Requisito | Implementação | Teste |
|---|---|---|
| RF01 Cadastro | /cadastro | cadastro válido/inválido |
| RF02 Login | /login | credenciais |
| RF03 Catálogo | /catalogo | produtos ativos |
| RF07 Carrinho | /carrinho | adicionar/alterar/remover |
| RF11 Endereço | /checkout | campos obrigatórios |
| RF12 Pagamento | Payment | criação de transação simulada |
| RF13 Pedido | Order/OrderItem | checkout completo |
| RF15 Status | admin_order | atualização de status |
| RF17 Produtos | admin_product/admin_edit_product | CRUD parcial + ativação |
| RNF01 Responsividade | CSS media queries | teste em telas |
| RNF03 Segurança | Flask-Login + controle admin | acesso não autorizado |
