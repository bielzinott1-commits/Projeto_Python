from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import Occurrence, AuditLog

bp = Blueprint("occurrences", __name__)
STATUSES = ["Registrada", "Em análise", "Em andamento", "Aguardando providências", "Concluída", "Arquivada"]

def can_write():
    return current_user.role in {"administrador", "gestor", "operador"}

@bp.get("/")
@login_required
def index():
    q = Occurrence.query
    term = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    if term:
        q = q.filter((Occurrence.protocol.contains(term)) | (Occurrence.title.contains(term)))
    if status in STATUSES:
        q = q.filter_by(status=status)
    page = q.order_by(Occurrence.created_at.desc()).paginate(page=request.args.get("page", 1, type=int), per_page=10, error_out=False)
    return render_template("occurrences/index.html", page=page, statuses=STATUSES, term=term, selected_status=status)

@bp.route("/nova", methods=["GET", "POST"])
@login_required
def create():
    if not can_write(): abort(403)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        if not title or not category:
            flash("Preencha o título e a categoria.", "error")
            return render_template("occurrences/form.html", occurrence=None)
        protocol = "DEMO-" + datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        item = Occurrence(protocol=protocol, title=title, category=category, description=description,
                          status="Registrada", unit_name="Unidade Demonstrativa", created_by=current_user.id)
        db.session.add(item)
        db.session.flush()
        db.session.add(AuditLog(user_id=current_user.id, event="create", entity="occurrence", entity_id=str(item.id)))
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Não foi possível gerar o protocolo. Tente novamente.", "error")
            return render_template("occurrences/form.html", occurrence=None)
        flash("Ocorrência demonstrativa cadastrada.", "success")
        return redirect(url_for("occurrences.index"))
    return render_template("occurrences/form.html", occurrence=None)

@bp.get("/<int:item_id>")
@login_required
def detail(item_id):
    item = db.session.get(Occurrence, item_id)
    if not item: abort(404)
    return render_template("occurrences/detail.html", item=item)
