from flask import Flask
def register_blueprints(app: Flask):
    from app.routes.health import bp as health_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
