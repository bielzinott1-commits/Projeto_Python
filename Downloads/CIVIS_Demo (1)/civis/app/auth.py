from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import db
from .models import User, AuditLog

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username, active=True).first()
        if user and user.check_password(password):
            login_user(user)
            db.session.add(AuditLog(user_id=user.id, event="login", entity="user", entity_id=str(user.id)))
            db.session.commit()
            return redirect(url_for("main.dashboard"))
        flash("Usuário ou senha inválidos.", "error")
    return render_template("auth/login.html")

@bp.post("/logout")
@login_required
def logout():
    db.session.add(AuditLog(user_id=current_user.id, event="logout", entity="user", entity_id=str(current_user.id)))
    db.session.commit()
    logout_user()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("auth.login"))
