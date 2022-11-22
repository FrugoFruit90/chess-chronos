from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FieldList, FormField


class MoveForm(FlaskForm):
    move_number = StringField('Move', render_kw={'disabled': 'disabled', 'style': 'width: 1cm'})
    white_move = StringField('White', render_kw={'disabled': 'disabled', 'style': 'width: 3cm'})
    black_move = StringField('Black', render_kw={'disabled': 'disabled', 'style': 'width: 3cm'})
    white_time = IntegerField('Move time White')
    black_time = IntegerField('Move time Black')


class GameForm(FlaskForm):
    title = StringField('Game Title')
    moves = FieldList(FormField(MoveForm))
