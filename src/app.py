from flask import Flask , request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lar1ss0n@localhost:5432/zapatillas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Zapatilla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    año = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Zapatilla %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "año": self.año,
            "precio": self.precio,
            "imagen": self.imagen
        }   
    
with app.app_context():
 db.create_all()

@app.route('/publicacion', methods=['POST'])
def create_publicacion():
   
    marca = request.json.get('marca')
    modelo = request.json.get('modelo')
    año = request.json.get('año')
    precio = request.json.get('precio')
    imagen = request.json.get('imagen')

    new_publicacion = Zapatilla(marca=marca, modelo=modelo, año=año, precio=precio, imagen=imagen)
    db.session.add(new_publicacion)
    db.session.commit()
    return "Publicacion creada"

@app.route('/publicacion', methods=['GET'])
def get_publicaciones():
    try:
        publicaciones = Zapatilla.query.all()
        publicaciones = list(map(lambda publicacion: publicacion.serialize(), publicaciones))
        return {"publicaciones": publicaciones}
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/publicacion/<id>', methods=['GET'])
def get_publicacion(id):
    try:
        publicacion = Zapatilla.query.get(id)
        return publicacion.serialize()
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/publicacion/<id>', methods=['PUT'])
def update_publicacion(id):
    try:
        publicacion = Zapatilla.query.get(id)
        marca = request.json.get('marca')
        modelo = request.json.get('modelo')
        año = request.json.get('año')
        precio = request.json.get('precio')
        imagen = request.json.get('imagen')

        publicacion.marca = marca
        publicacion.modelo = modelo
        publicacion.año = año
        publicacion.precio = precio
        publicacion.imagen = imagen

        db.session.commit()
        return publicacion.serialize()
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/publicacion/<id>', methods=['DELETE'])
def delete_publicacion(id):
    try:
        publicacion = Zapatilla.query.get(id)
        db.session.delete(publicacion)
        db.session.commit()
        return "Publicacion eliminada"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)






