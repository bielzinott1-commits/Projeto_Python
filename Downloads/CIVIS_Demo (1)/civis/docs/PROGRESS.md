# Progresso CIVIS

## Fase atual
Fase C — fundação e interface inicial.

## Implementado
- [x] Estrutura Flask e configuração por ambiente.
- [x] Modelos iniciais de usuários, ocorrências, bens e auditoria.
- [x] Login/logout, hash de senha e CSRF.
- [x] Dashboard com contagens do banco.
- [x] Cadastro e consulta de ocorrências com busca, filtro e paginação.
- [x] Cadastro e consulta de bens demonstrativos.
- [x] Layout responsivo inicial.
- [x] Folha de estilos `app/static/css/app.css` criada para corresponder aos templates.
- [x] JavaScript `app/static/js/app.js` criado para menu móvel com suporte a teclado.
- [x] Estrutura e README reorganizados.
- [x] Testes básicos automatizados escritos.

## Pendente
- [ ] Migrações versionadas Flask-Migrate/Alembic.
- [ ] Procedimentos, pessoas fictícias e unidades.
- [ ] RBAC granular e escopo por unidade.
- [ ] Movimentações imutáveis do inventário.
- [ ] Relatórios e exportação CSV segura.
- [ ] Notificações persistentes.
- [ ] Limite de tentativas de login.
- [ ] Testes de integração adicionais e Playwright.

## Verificação desta organização
- [x] Arquivos CSS e JavaScript referenciados pelo template criados.
- [x] Sintaxe Python compilada sem erros.
- [ ] `pytest -q` bloqueado neste ambiente porque Flask não está instalado (`ModuleNotFoundError: No module named 'flask'`).

## Estados
Implementado não significa testado. Atualizar este documento após cada execução real dos testes.

## Limitações conhecidas
- O inicializador usa `db.create_all()` para a primeira versão, não substituindo migrações em um produto evolutivo.
- Auditoria cobre login/logout e criação de registros; não é ainda um histórico completo à prova de alteração.
- A aplicação é demonstrativa e não deve conter dados pessoais reais.
