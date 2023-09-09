from flask import Flask
from models.database import db
from routes.user_routes import user_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skills.db'

db.init_app(app)

app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)