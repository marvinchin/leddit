from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ThreadForm(FlaskForm):
    topic = StringField('Topic', validators = [DataRequired()])
    submit = SubmitField('Submit')
