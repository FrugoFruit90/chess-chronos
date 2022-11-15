from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FieldList, FormField


class MoveForm(FlaskForm):
    move_number = StringField('Move number')
    white_move = StringField('Move number')
    black_move = StringField('Move number')
    white_time = IntegerField('Move time')
    black_time = IntegerField('Move time')


class GameForm(FlaskForm):
    title = StringField('Game Title')
    moves = FieldList(FormField(MoveForm))
