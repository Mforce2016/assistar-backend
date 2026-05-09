from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.ia_routes import ia_bp
from routes.payment_routes import payment_bp

app = Flask(__name__)

CORS(app)

# ======================================
# BLUEPRINTS
# ======================================

app.register_blueprint(auth_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(payment_bp)

# ======================================
# TEST ONLINE
# ======================================

@app.route("/")
def home():
    return {
        "status": "Backend AssistAR online"
    }

# ======================================
# MAIN
# ======================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )