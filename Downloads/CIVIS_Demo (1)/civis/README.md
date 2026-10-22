# CIVIS — Sistema Integrado de Gestão Policial Demonstrativo

Aplicação educacional local para aprender Flask, SQLAlchemy, HTML, CSS e MySQL. Todos os dados devem ser fictícios. **Não é um sistema oficial nem deve ser usado para operações policiais reais.**

## Implementado nesta primeira versão
- Login com hash de senha, sessão Flask-Login e proteção CSRF.
- Inicialização de administrador sem senha padrão.
- Dashboard com indicadores calculados no banco.
- Cadastro, consulta, busca, filtro e paginação de ocorrências.
- Cadastro e consulta de bens demonstrativos vinculáveis a ocorrências.
- Registros básicos de auditoria.
- Interface responsiva com folha CSS organizada e JavaScript acessível para o menu móvel.
- Estrutura de arquivos separada por responsabilidade e documentação do progresso.
- Testes iniciais com SQLite isolado.

## Requisitos
Python 3.11+ recomendado. MySQL 8+ para uso configurado com MySQL; SQLite é usado por padrão para facilitar a execução local inicial.

## Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edite `.env` e substitua `SECRET_KEY` por um valor aleatório longo. Para MySQL, crie o banco e usuário de privilégio limitado e ajuste `DATABASE_URL`, por exemplo `mysql+pymysql://usuario:senha@localhost:3306/civis_demo?charset=utf8mb4`. Não use credenciais reais em arquivos versionados.

## Criar banco e administrador
```powershell
python scripts/init_db.py
```
O script cria as tabelas da versão atual e solicita usuário e senha de administrador. A senha deve ter pelo menos 12 caracteres. Para mudanças futuras, adicione migrações versionadas com Flask-Migrate/Alembic; esta versão inicial ainda não configura migrações.

## Iniciar
```powershell
python run.py
```
Abra `http://127.0.0.1:5000`. Não exponha o servidor de desenvolvimento à internet.

## Testes
```powershell
pytest -q
```
Os testes usam um banco SQLite em memória separado; não apagam seu banco de desenvolvimento.

## Estrutura do projeto
```text
civis/
├── app/
│   ├── __init__.py          # criação e configuração da aplicação
│   ├── config.py            # configuração por variáveis de ambiente
│   ├── extensions.py        # extensões Flask compartilhadas
│   ├── models.py            # modelos SQLAlchemy
│   ├── auth.py              # autenticação e sessão
│   ├── main.py              # dashboard e página inicial
│   ├── occurrences.py       # módulo de ocorrências
│   ├── apprehensions.py     # módulo de bens demonstrativos
│   ├── templates/           # templates Jinja2/HTML
│   └── static/
│       ├── css/app.css      # design system e layout responsivo
│       ├── js/app.js        # interações acessíveis
│       └── images/          # imagens locais do projeto
├── docs/PROGRESS.md         # progresso, pendências e limitações
├── scripts/init_db.py       # criação inicial do banco e administrador
├── sql/README.md            # notas de configuração SQL
├── tests/                   # testes automatizados
├── instance/                # dados locais, ignorados pelo Git
├── .env.example             # modelo de configuração sem segredos
├── requirements.txt         # dependências Python
├── run.py                   # ponto de entrada
└── README.md                # guia principal
```

## Limitações conhecidas
Esta entrega é uma base funcional inicial, não a totalidade do escopo V3.0. Procedimentos, pessoas fictícias, unidades, notificações, relatórios/CSV, matriz granular de permissões, movimentações de bens, limitação de tentativas de login e migrações versionadas ainda não estão implementados. Faça revisão de segurança antes de qualquer uso além de demonstração local.
