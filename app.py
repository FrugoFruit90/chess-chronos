import itertools
import logging
import os

from flask import Flask, flash, request, redirect, render_template, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

from exceptions_ import MissingValueException
from forms import GameForm, MoveForm
from loaders import pgn_game_generator
from config import config
from constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

root = logging.getLogger()
logging.basicConfig(level=logging.INFO)
root.setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def pairwise_longest(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return itertools.zip_longest(a, a)


def create_app(app_environment=None):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'secret key'
    if app_environment is None:
        app.config.from_object(config[os.getenv('FLASK_ENV', 'dev')])
    else:
        app.config.from_object(config[app_environment])
    CORS(app)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods=['GET', 'POST'])
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
                return redirect(url_for('game_data', filename=filename, game_no=0))
        else:
            return render_template('base.html', title='Move Table')

    @app.route('/game_data/', methods=['GET', 'POST'])
    def game_data():
        if request.method == 'GET':
            with open(f'upload/{request.args.get("filename")}') as pgn_file:
                for i, game in enumerate(pgn_game_generator(pgn_file)):
                    if i != int(request.args.get("game_no")):
                        continue
                    else:
                        game_form = GameForm()
                        headers = game.headers
                        game_form.title.data = f'{headers["White"]} - {headers["Black"]}, {headers["Date"]}'
                        for move_no, (move_white, move_black) in enumerate(pairwise_longest(game.mainline())):
                            move_form = MoveForm()
                            move_form.move_number = move_no + 1
                            move_form.white_move = move_white.move
                            move_form.white_time = move_white.clock()
                            try:
                                move_form.black_move = move_black.move
                                move_form.black_time = move_black.clock()
                            except AttributeError:
                                move_form.black_move = '---'
                                move_form.black_time = '---'
                            game_form.moves.append_entry(move_form)
                        return render_template('table.html', game_form=game_form)
        elif request.method == 'POST':
            with open(f'upload/{request.args.get("filename")}') as pgn_file_input:
                for i, game in enumerate(pgn_game_generator(pgn_file_input)):
                    if i != int(request.args.get("game_no")):
                        continue
                    for move_no, (move_white, move_black) in enumerate(pairwise_longest(game.mainline())):
                        try:
                            move_white.set_clock(int(request.form[f'moves-{move_no}-white_time']))
                            move_black.set_clock(int(request.form[f'moves-{move_no}-black_time']))
                        except AttributeError:
                            move_white.set_clock(int(request.form[f'moves-{move_no}-white_time']))
                        except ValueError:
                            raise MissingValueException("Missing clock values!")
                            # TODO: this should be changed to just giving the same page without
                            # TODO: or actually have a validator on the website
                    print(game, file=open(f'download/{request.args.get("filename")}', "a"), end="\n\n")
            return redirect(
                url_for('game_data', filename=request.args.get("filename"),
                        game_no=int(request.args.get("game_no")) + 1))

    return app


if __name__ == "__main__":
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    app.run()
