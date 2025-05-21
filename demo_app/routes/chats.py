# demo_app/routes/chats.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from thu_messaging.extensions.database import db
from thu_messaging.models.patient import Patient
from thu_messaging.models.message import Message

from sqlalchemy import or_, func

chats_bp = Blueprint("chats", __name__)

@chats_bp.route("/", methods=["GET"])
def chat_list():
    """
    List the most recent 10 chat threads, grouped by phone.
    Shows preview, timestamp, and patient name if linked.
    """
    subquery = (
        db.session.query(
            Message.phone,
            func.max(Message.timestamp).label("last_timestamp")
        )
        .group_by(Message.phone)
        .subquery()
    )

    messages = (
        db.session.query(Message)
        .join(subquery, (Message.phone == subquery.c.phone) & (Message.timestamp == subquery.c.last_timestamp))
        .order_by(Message.timestamp.desc())
        .limit(10)
        .all()
    )

    # Optional: map phone -> patient
    phones = [msg.phone for msg in messages]
    patients = Patient.query.filter(Patient.phone.in_(phones)).all()
    phone_to_name = {p.phone: f"{p.first_name} {p.last_name}" for p in patients}

    return render_template("chat_list.html", messages=messages, phone_to_name=phone_to_name)


@chats_bp.route("/search", methods=["GET"])
def chat_search():
    """
    Search chats by keyword, recipient name, phone, email, or date.
    """
    query = request.args.get("q", "")
    if not query:
        return redirect(url_for("chats.chat_list"))

    results = (
        db.session.query(Message)
        .join(Patient, Patient.id == Message.patient_id, isouter=True)
        .filter(
            or_(
                Message.phone.ilike(f"%{query}%"),
                Message.content.ilike(f"%{query}%"),
                Patient.first_name.ilike(f"%{query}%"),
                Patient.last_name.ilike(f"%{query}%"),
                Patient.email.ilike(f"%{query}%"),
                func.cast(Message.timestamp, db.String).ilike(f"%{query}%")
            )
        )
        .order_by(Message.timestamp.desc())
        .all()
    )

    return render_template("chat_search_results.html", messages=results, query=query)


@chats_bp.route("/<phone>", methods=["GET", "POST"])
def chat_detail(phone):
    """
    View messages for a conversation thread and send new messages.
    """
    if request.method == "POST":
        content = request.form["message"]
        sender = "admin"  # or get from auth system

        new_msg = Message(phone=phone, sender=sender, content=content)
        db.session.add(new_msg)
        db.session.commit()
        flash("Message sent", "success")
        return redirect(url_for("chats.chat_detail", phone=phone))

    messages = Message.query.filter_by(phone=phone).order_by(Message.timestamp.asc()).all()
    patient = Patient.query.filter_by(phone=phone).first()
    return render_template("chat.html", messages=messages, patient=patient)
