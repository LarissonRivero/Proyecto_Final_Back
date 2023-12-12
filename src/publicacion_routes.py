from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db

publicacion_blueprint = Blueprint("publicacion", __name__)

class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    año = db.Column(db.String(4), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Publicacion {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "año": self.año,
            "precio": self.precio,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
        }
    
@publicacion_blueprint.route('/publicacion', methods=['POST'])
def agregar_publicacion():
    try:
        data = request.get_json()

        if not all(key in data for key in ['marca', 'modelo', 'año', 'precio', 'descripcion', 'imagen']):
            raise ValueError("Campos 'marca', 'modelo', 'año', 'precio', 'descripcion' e 'imagen'  son requeridos")

        nueva_publicacion = Publicacion(
            marca=data['marca'],
            modelo=data['modelo'],
            año=str(data['año']),
            precio=data['precio'],
            descripcion=data['descripcion'],
            imagen=data['imagen'],
        )

        db.session.add(nueva_publicacion)
        db.session.commit()

        return jsonify({"mensaje": "Nueva publicación agregada correctamente"}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar el producto: {str(e)}"}), 500
    finally:
        db.session.close()

@publicacion_blueprint.route('/publicacion', methods=['GET'])
def obtener_publicaciones():
    try:
        publicaciones = Publicacion.query.all()
        return jsonify([publicacion.serialize() for publicacion in publicaciones]), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las publicaciones: {str(e)}"}), 500
    finally:
        db.session.close()

@publicacion_blueprint.route('/publicacion/<int:id>', methods=['GET'])
def obtener_publicacion(id):
    try:
        publicacion = Publicacion.query.get(id)
        return jsonify(publicacion.serialize()), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener la publicación: {str(e)}"}), 500
    finally:
        db.session.close()

@publicacion_blueprint.route('/publicacion/<int:id>', methods=['PUT'])
def actualizar_publicacion(id):
    try:
        data = request.get_json()

        if not all(key in data for key in ['marca', 'modelo', 'año', 'precio', 'descripcion', 'imagen']):
            raise ValueError("Campos 'marca', 'modelo', 'año', 'precio', 'descripcion' e 'imagen'  son requeridos")

        publicacion = Publicacion.query.get(id)

        if not publicacion:
            raise ValueError("La publicación no existe")

        publicacion.marca = data['marca']
        publicacion.modelo = data['modelo']
        publicacion.año = data['año']
        publicacion.precio = data['precio']
        publicacion.descripcion = data['descripcion']
        publicacion.imagen = data['imagen']

        db.session.commit()

        return jsonify({"mensaje": "Publicación actualizada correctamente"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar la publicación: {str(e)}"}), 500
    finally:
        db.session.close()

@publicacion_blueprint.route('/publicacion/<int:id>', methods=['DELETE'])
def eliminar_publicacion(id):
    try:
        publicacion = Publicacion.query.get(id)

        if not publicacion:
            raise ValueError("La publicación no existe")

        db.session.delete(publicacion)
        db.session.commit()

        return jsonify({"mensaje": "Publicación eliminada correctamente"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la publicación: {str(e)}"}), 500
    finally:
        db.session.close()


