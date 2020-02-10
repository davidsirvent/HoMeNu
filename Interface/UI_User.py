""" User Interface for User management """

import functools
import secrets

from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session, g)
from werkzeug.security import check_password_hash, generate_password_hash

from Modeling.user import M_User
from Modeling import error
from Logical import (L_User, L_Mail, utils)


ui = Blueprint('UI_User', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('UI_User.login'))

        elif g.user.activate_url != '':
            return redirect(url_for('UI_User.activation'))

        return view(**kwargs)

    return wrapped_view


def generate_token():
    return secrets.token_urlsafe(24)


@ui.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        if 'save_button' in request.form:
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']

            try:
                request.form['terms']
                terms = 1
            except:
                terms = 0

            try:
                request.form['pub']
                pub = 1
            except:
                pub = 0

            try:
                try:
                    user_list = L_User.select(email)
                except:
                    user_list = None

                error_tmp = False
                if user_list is not None:
                    flash(error.Email_exist)
                    error_tmp = True

                if utils.check_password_requirements(password) == False:
                    flash(error.Bad_password)
                    error_tmp = True

                if error_tmp == False:
                    try:
                        activation_token = generate_token()                        
                        L_Mail.send('activation', activation_token, email.lower())
                        L_User.save(M_User(email.lower(), username, generate_password_hash(password), activation_token, '', terms, pub))
                        flash(error.Saved_Successfully)
                        return redirect(url_for('UI_User.login'))

                    except RuntimeError as err:
                        flash(err.args[0])

            except RuntimeError as err:
                flash(err.args[0])

    return render_template('UI_User/register.html')


@ui.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        if 'login_button' in request.form:
            email = request.form['email']
            password = request.form['password']

            try:
                user = L_User.select(email)

                error_temp = False
                if len(user) == 0:
                    flash(error.Bad_user)
                    error_temp = True

                if error_temp == False and check_password_hash(user[0].password, password) == False:
                    flash(error.Bad_Credentials)
                    error_temp = True

                if error_temp == False:
                    try:
                        session.clear()
                        session['user_email'] = user[0].email

                        return redirect(url_for('calendar'))

                    except RuntimeError as err:
                        flash(error.Insert_Failed)

            except RuntimeError as err:
                flash(err.args[0])

    return render_template('UI_User/login.html')


@ui.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    if request.method == 'POST':
        if 'save_button' in request.form:
            username = request.form['username']
            try:
                request.form['pub']
                pub = 1
            except:
                pub = 0

            try:
                L_User.save(M_User(g.user.email, username, g.user.password, g.user.activate_url, g.user.reset_url, g.user.accept_terms, pub))
                g.user = L_User.select(g.user.email)[0]
                flash(error.Saved_Successfully)
            except:
                flash(error.Insert_Failed)

        elif 'reset_button' in request.form:
            reset_token = generate_token()
            L_User.save(M_User(g.user.email, g.user.name, g.user.password, g.user.activate_url, reset_token, g.user.accept_terms, g.user.accept_pub))
            L_Mail.send('reset', reset_token, g.user.email)
            flash(error.Mail_Sent)

    return render_template('UI_User/profile.html')


@ui.before_app_request
def load_logged_user():
    user_email = session.get('user_email')

    if user_email is None:
        g.user = None
    else:
        user = L_User.select(user_email)
        g.user = user[0]


@ui.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('UI_User.login'))


@ui.route('/activation', methods=('GET', 'POST'))
def activation():
    if request.method == 'POST':
        if 'resend_button' in request.form:
            try:
                email = request.form['email']
                user = L_User.select(email)[0]
                L_Mail.send('activation', user.activate_url, email.lower())
            except:
                pass

        flash(error.Mail_Sent)

    return render_template('UI_User/activation.html')


@ui.route('/activation/<value>')
def set_active(value: str):
    try:
        user_list = L_User.select()
    except:
        user_list = None

    found = False
    for user in user_list:
        if user.activate_url == value:
            found = True
            email = user.email

    if found:
        L_User.activate(email)
        return render_template('UI_User/set_active.html')
    else:
        return redirect(url_for('UI_User.login'))


@ui.route('/reset/<value>', methods=('GET', 'POST'))
def reset_password(value: str):
    if request.method == 'POST':
        if 'reset_button' in request.form:
            email = request.form['email']
            new_password = request.form['password']
            if utils.check_password_requirements(new_password) == False:
                flash(error.Bad_password)
                return render_template('UI_User/reset_password.html')

            try:
                user = L_User.select(email)[0]
                if user.reset_url == value:
                    L_User.save(M_User(user.email, user.name, generate_password_hash(
                        new_password), '', '', user.accept_terms, user.accept_pub))
                    flash(error.Saved_Successfully)
                else:
                    flash(error.Insert_Failed)

            except:
                flash(error.Insert_Failed)

    return render_template('UI_User/reset_password.html')


@ui.route('/request-new-password', methods=('GET', 'POST'))
def request_new_password():
    if request.method == 'POST':
        if 'request_button' in request.form:
            email = request.form['email']
            try:
                user = L_User.select(email)[0]
                reset_token = generate_token()
                L_User.save(M_User(user.email, user.name, user.password, user.activate_url, reset_token, user.accept_terms, user.accept_pub))
                L_Mail.send('reset', reset_token, user.email)
                flash(error.Mail_Sent)

            except:
                flash(error.Mail_Sent)

    return render_template('UI_User/reset_password_request.html')


@ui.route('/privacidad')
def privacy():
    return render_template('UI_User/privacy.html')


@ui.route('/terminos-de-uso')
def terms():
    return render_template('UI_User/terms.html')


@ui.route('/politica-cookies')
def cookies():
    return render_template('UI_User/cookies.html')
