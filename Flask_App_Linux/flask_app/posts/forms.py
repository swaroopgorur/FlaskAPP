from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


######################################################################################
################################# Post Form ##########################################
######################################################################################

class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=30, max=10000)])
    submit = SubmitField("Post")
