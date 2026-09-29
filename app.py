from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from models.user import db
from routes.user_routes import user_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
csrf = CSRFProtect(app)

app.register_blueprint(user_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
