from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, FieldList, FormField
from wtforms.validators import InputRequired, length


class MoveForm(FlaskForm):
    move_number = StringField('Move', render_kw={'disabled': 'disabled', 'style': 'width: 1cm'})
    white_move = StringField('White', render_kw={'disabled': 'disabled', 'style': 'width: 2cm'})
    white_time = IntegerField('Move time White', validators=[InputRequired(), length(max=3)],
                              render_kw={'style': 'width: 2cm'})
    black_move = StringField('Black', render_kw={'disabled': 'disabled', 'style': 'width: 2cm'})
    black_time = IntegerField('Move time Black', validators=[InputRequired(), length(max=3)],
                              render_kw={'style': 'width: 2cm'})


class GameForm(FlaskForm):
    title = StringField('Game Title')
    moves = FieldList(FormField(MoveForm))
