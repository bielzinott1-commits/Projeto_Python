from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db, login_manager

def utcnow():
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="operador")
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.active

class Occurrence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(30), unique=True, nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="Registrada")
    description = db.Column(db.Text, nullable=False, default="")
    unit_name = db.Column(db.String(120), nullable=False, default="Unidade Demonstrativa")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

class Apprehension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(32), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    storage_location = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="Registrado")
    occurrence_id = db.Column(db.Integer, db.ForeignKey("occurrence.id"), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    occurrence = db.relationship("Occurrence", backref="apprehensions")

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    event = db.Column(db.String(80), nullable=False)
    entity = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.String(40), nullable=True)
    result = db.Column(db.String(30), nullable=False, default="success")
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
