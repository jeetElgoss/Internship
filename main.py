from flask import Flask
from routes.qr_routes import qr_bp
from routes.intern_routes import intern_bp

# Initialize Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(qr_bp)
app.register_blueprint(intern_bp)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
