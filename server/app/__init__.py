from flask import Flask, render_template
from 

WEB_FILES_PATH = "../web_files"

def create_app():
    app = Flask(
        __name__,
        template_folder=f"{WEB_FILES_PATH}/templates",
        static_folder=f"{WEB_FILES_PATH}/static"
    )
    
    return app

app = create_app()

# Init app
from api import register 
@app.route('/')
def root():
    return render_template('extends.html')