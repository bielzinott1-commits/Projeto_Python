from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Occurrence, Apprehension, User, AuditLog

bp = Blueprint("main", __name__)

@bp.get("/")
def home():
    from flask import redirect, url_for
    return redirect(url_for("main.dashboard") if current_user.is_authenticated else url_for("auth.login"))

@bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html",
        occurrence_count=Occurrence.query.count(),
        active_count=Occurrence.query.filter(Occurrence.status.in_(["Registrada", "Em análise", "Em andamento", "Aguardando providências"])).count(),
        apprehension_count=Apprehension.query.count(),
        user_count=User.query.count(),
        recent=Occurrence.query.order_by(Occurrence.created_at.desc()).limit(6).all(),
        audit_count=AuditLog.query.count())
