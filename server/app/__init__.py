from flask import Flask, render_template
from app.router import Router

WEB_FILES_PATH = "../web_files"

def create_app():
    app = Flask(
        __name__,
        template_folder=f"{WEB_FILES_PATH}/templates",
        static_folder=f"{WEB_FILES_PATH}/static"
    )
    
    Router.init_app(app)
    
    return app

app = create_app()

# Init app

@app.route('/')
def root():
    return render_template('extends.html')

@app.errorhandler(500)
def errorhandler(e):
    return render_template("error.html"), 500

@app.errorhandler(400)
def errorhandler(e):
    return render_template("error.html"), 400