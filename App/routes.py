from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, current_user, logout_user, login_required
from App import app, db_users, bcrypt
from App.models import User
from App.forms import RegistrationForm, LoginForm

@app.route("/")
@login_required
def home():
    session['username'] = current_user.username
    return render_template(
        # template_name_or_list="home.html"
        template_name_or_list="groundwater.html"
    )


@app.route('/groundwater')
@login_required
def groundwater():
    return render_template(
        template_name_or_list="groundwater.html"
    )


@app.route('/groundwater/datacleansing')
@login_required
def groundwater_dataCleansing():
    return render_template(
        template_name_or_list="groundwater_dataCleansing.html"
    )


@app.route('/groundwater/datavisualization')
@login_required
def groundwater_dataVisualization():
    return render_template(
        template_name_or_list="groundwater_dataVisualization.html"
    )


@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            password=form.password.data).decode(encoding='utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db_users.session.add(user)
        db_users.session.commit()
        flash(message="ثبت نام شما با موفقیت انجام شد!", category='success')
        return redirect(location=url_for(endpoint='home'))

    return render_template(template_name_or_list='register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        session['username'] = current_user.username
        return redirect(location=url_for(endpoint='home'))
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(pw_hash=user.password, password=form.password.data):
            login_user(user=user)
            # login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(message="ورود شما با موفقیت انجام شد!", category='success')
            return redirect(location=url_for(endpoint='home'))
            # return redirect(location=next_page if next_page else url_for(endpoint='home'))
        else:
            flash(message="نام کاربری یا رمز عبور وارد شده صحیح نمیباشد!",
                  category='danger')
    return render_template(template_name_or_list='login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(message="شما با موفقیت از حساب کاربری خود خارج شده اید!",
                  category='success')
    return redirect(location=url_for(endpoint='login'))