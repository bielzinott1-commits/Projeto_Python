from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .extensions import db
from .models import Apprehension, Occurrence, AuditLog

bp = Blueprint("apprehensions", __name__)

@bp.get("/")
@login_required
def index():
    items = Apprehension.query.order_by(Apprehension.created_at.desc()).limit(100).all()
    return render_template("apprehensions/index.html", items=items)

@bp.route("/nova", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role not in {"administrador", "gestor", "operador"}: abort(403)
    occurrences = Occurrence.query.order_by(Occurrence.created_at.desc()).all()
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("storage_location", "").strip()
        try:
            quantity = int(request.form.get("quantity", "1"))
            occurrence_id = int(request.form.get("occurrence_id") or 0) or None
        except ValueError:
            quantity, occurrence_id = 0, None
        occurrence = db.session.get(Occurrence, occurrence_id) if occurrence_id else None
        if not description or not category or not location or quantity < 1 or (occurrence_id and not occurrence):
            flash("Confira os campos e a ocorrência vinculada.", "error")
            return render_template("apprehensions/form.html", occurrences=occurrences)
        item = Apprehension(identifier="BEM-" + __import__("secrets").token_hex(6).upper(),
                            description=description, category=category, quantity=quantity,
                            storage_location=location, occurrence_id=occurrence.id if occurrence else None,
                            created_by=current_user.id)
        db.session.add(item)
        db.session.flush()
        db.session.add(AuditLog(user_id=current_user.id, event="create", entity="apprehension", entity_id=str(item.id)))
        db.session.commit()
        flash("Registro demonstrativo de bem criado.", "success")
        return redirect(url_for("apprehensions.index"))
    return render_template("apprehensions/form.html", occurrences=occurrences)

@bp.get("/<int:item_id>")
@login_required
def detail(item_id):
    item = db.session.get(Apprehension, item_id)
    if not item: abort(404)
    return render_template("apprehensions/detail.html", item=item)
