from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[FileRequired(), FileAllowed(['xlsx', 'xls', 'csv', 'json', 'xml'], 'Invalid file format.')])
    submit = SubmitField('Submit')
