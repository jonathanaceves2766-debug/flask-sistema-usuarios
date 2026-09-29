from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import db, User
from forms.user_forms import RegisterForm, LoginForm, EditProfileForm

user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('El usuario o correo ya está registrado.', 'danger')
            return render_template('register.html', form=form)
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('¡Usuario registrado con éxito! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(url_for('user.user_list'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('user.login'))

@user_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('user.profile', id=user.id))
    return render_template('edit_profile.html', form=form, user=user)

@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    if session.get('user_id') == id:
        session.clear()
    flash('Usuario eliminado con éxito.', 'info')
    return redirect(url_for('user.user_list'))
