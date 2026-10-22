import getpass
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    username = input("Usuário administrador: ").strip()
    password = getpass.getpass("Senha (mínimo 12 caracteres): ")
    if len(password) < 12:
        raise SystemExit("A senha precisa ter pelo menos 12 caracteres.")
    if not username or User.query.filter_by(username=username).first():
        raise SystemExit("Usuário vazio ou já existente.")
    user = User(username=username, role="administrador")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print("Administrador local criado.")
