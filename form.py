from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm

class Firebase_Input(FlaskForm):
    name = StringField('Experiment No/Name :')
    code = TextAreaField('Code :')
    submit = SubmitField('Submit')