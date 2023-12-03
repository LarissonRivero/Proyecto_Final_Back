# app.py
from flask import Flask
from flask_cors import CORS
from publicacion_routes import publicacion_blueprint, db
from usuario_routes import usuario_blueprint, db
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lar1ss0n@localhost:5432/snicky'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

app.register_blueprint(publicacion_blueprint)
app.register_blueprint(usuario_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



