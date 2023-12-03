from flask import Blueprint, request, jsonify
from database import db

usuario_blueprint = Blueprint("usuario", __name__)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "username": self.username,
        }

@usuario_blueprint.route('/usuario', methods=['POST'])
def registrar_usuario():
    try:
        data = request.get_json()

        if not all(key in data for key in ['email', 'password', 'username']):
            raise ValueError("Campos 'email', 'password' y 'username' son requeridos")

        nuevo_usuario = Usuario(
            email=data['email'],
            password=data['password'],
            username=data['username'],
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Nuevo usuario registrado correctamente"}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar el usuario: {str(e)}"}), 500
    finally:
        db.session.close()

@usuario_blueprint.route('/usuario/login', methods=['POST'])
def iniciar_sesion():
    try:
        data = request.get_json()

        if not all(key in data for key in ['email', 'password']):
            raise ValueError("Campos 'email' y 'password' son requeridos")

        usuario = Usuario.query.filter_by(email=data['email'], password=data['password']).first()

        if usuario:
            return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
        else:
            return jsonify({"error": "Correo o contraseña incorrectos"}), 401

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al iniciar sesión: {str(e)}"}), 500
    finally:
        db.session.close()

@usuario_blueprint.route('/usuario', methods=['GET'])
def obtener_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify([usuario.serialize() for usuario in usuarios]), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los usuarios: {str(e)}"}), 500
    finally:
        db.session.close()



@usuario_blueprint.route('/usuario/<int:id>', methods=['GET'])
def obtener_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        return jsonify(usuario.serialize()), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el usuario: {str(e)}"}), 500
    finally:
        db.session.close()



