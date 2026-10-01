from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[
        DataRequired(message='El usuario es obligatorio.'),
        Length(min=4, max=20, message='El usuario debe tener entre 4 y 20 caracteres.')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria.'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Confirma tu contraseña.'),
        EqualTo('password', message='Las contraseñas deben coincidir.')
    ])
    submit = SubmitField('Registrarse')

    def validate_username(self, field):
        if User.get_by_username(field.data):
            raise ValidationError('Este nombre de usuario ya está registrado.')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message='Ingresa tu usuario.')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Ingresa tu contraseña.')
    ])
    submit = SubmitField('Iniciar Sesión')
