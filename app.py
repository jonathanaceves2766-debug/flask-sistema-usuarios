from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(form.username.data, form.password.data)
        flash('Registro exitoso. ¡Ya puedes iniciar sesión!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(f'¡Bienvenido, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile'))
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@app.errorhandler(401)
def unauthorized_error(error):
    flash('Acceso no autorizado. Inicia sesión primero.', 'danger')
    return render_template('base.html'), 401

@app.errorhandler(403)
def forbidden_error(error):
    flash('Acceso prohibido. No tienes permisos para ver este recurso.', 'danger')
    return render_template('base.html'), 403

if __name__ == '__main__':
    app.run(debug=True, port=8000)
