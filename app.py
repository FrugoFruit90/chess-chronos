import logging
import os

from flask import Flask, flash, request, redirect, render_template, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

from constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from config import config

root = logging.getLogger()
logging.basicConfig(level=logging.INFO)
root.setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def create_app(app_environment=None):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if app_environment is None:
        app.config.from_object(config[os.getenv('FLASK_ENV', 'dev')])
    else:
        app.config.from_object(config[app_environment])
    CORS(app)

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def index():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('download_file', name=filename))
        return render_template('base.html', title='Move Table')

    return app


if __name__ == "__main__":
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    app.run()
