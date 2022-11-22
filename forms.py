from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FieldList, FormField


class MoveForm(FlaskForm):
    move_number = StringField('Move number', render_kw={'disabled': 'disabled'})
    white_move = StringField('Move number', render_kw={'disabled': 'disabled'})
    black_move = StringField('Move number', render_kw={'disabled': 'disabled'})
    white_time = IntegerField('Move time')
    black_time = IntegerField('Move time')


class GameForm(FlaskForm):
    title = StringField('Game Title')
    moves = FieldList(FormField(MoveForm))
