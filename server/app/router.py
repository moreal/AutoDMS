class Router:
    @classmethod
    def init_app(cls, app):
        from app.api.extends import register
        app.register_blueprint(register.api.blueprint)

        from app import extends
        app.register_blueprint(extends.api.blueprint)
