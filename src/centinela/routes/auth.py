from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import bcrypt
from config import Config
from src.centinela.extensions import db
from src.centinela.models.user import User

auth_bp = Blueprint("auth", __name__)


def init_admin():
    if User.query.filter_by(username="admin").first():
        return
    admin = User(
        username="admin",
        email="admin@centinela.local",
        password_hash=bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(),
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username y password requeridos"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Usuario ya existe"}), 409

    user = User(
        username=data["username"],
        email=data.get("email", f"{data['username']}@centinela.local"),
        password_hash=bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode(),
        role=data.get("role", "analyst")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario creado", "user": user.to_dict()}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username y password requeridos"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not bcrypt.checkpw(data["password"].encode(), user.password_hash.encode()):
        return jsonify({"error": "Credenciales invalidas"}), 401
    if not user.is_active:
        return jsonify({"error": "Usuario desactivado"}), 403

    token = create_access_token(
        identity=user.username,
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    )
    return jsonify({"token": token, "user": user.to_dict()})


@auth_bp.route("/api/auth/me")
@jwt_required()
def me():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_dict())
