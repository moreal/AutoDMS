class Router:
    @classmethod
    def init_app(cls, app):
        from app.api.extends import register
        from app.api.extends import apply
        app.register_blueprint(register.api.blueprint)
        app.register_blueprint(apply.api.blueprint)

        from app import extends
        app.register_blueprint(extends.api.blueprint)
