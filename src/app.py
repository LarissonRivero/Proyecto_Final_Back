from flask import Flask
from flask_cors import CORS
from publicacion_routes import publicacion_blueprint
from database import db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lar1ss0n@localhost:5432/snicky'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

app.register_blueprint(publicacion_blueprint)

if __name__ == '__main__':
    app.run(debug=True)





