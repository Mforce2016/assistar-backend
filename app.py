from flask import Flask
from flask_cors import CORS
from routes.license_routes import license_bp
from routes.auth_routes import auth_bp
from routes.ia_routes import ia_bp
from routes.payment_routes import payment_bp
from routes.emotional_routes import emotional_bp
from routes.payment_tokens_routes import tokens_bp

app = Flask(__name__)

CORS(app)

# ======================================
# BLUEPRINTS
# ======================================
app.register_blueprint(
    emotional_bp,
    url_prefix="/emocional"
)

app.register_blueprint(
    tokens_bp,
    url_prefix="/tokens"
)

app.register_blueprint(auth_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(license_bp)
# ======================================
# TEST ONLINE
# ======================================

@app.route("/")
def home():
    return {
        "status": "Backend online"
    }

# ======================================
# MAIN
# ======================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )