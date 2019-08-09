from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, 
                     BooleanField, SubmitField)
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    page_title = "Configure sua rede"
    ssid = StringField('SSID', validators=[DataRequired(message="Por favor, preencha o SSID")])
    password = PasswordField('Senha', validators=[DataRequired(message="Por favor, preencha a senha")])
    submit = SubmitField('Conecte-se')