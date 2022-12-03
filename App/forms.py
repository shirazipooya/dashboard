import itertools
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, SelectField, SubmitField, FormField, FieldList, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from App.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(message="وارد کردن نام کاربری ضروری میباشد."), Length(min=4, max=30, message="طول نام کاربری باید بین 4 تا 30 کارکتر باشد.")])
    password = PasswordField(label='Password',
                             validators=[DataRequired(message="وارد کردن رمز عبور ضروری میباشد.")])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(message="این نام کاربری موجود میباشد.")


class LoginForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(message="وارد کردن نام کاربری ضروری میباشد."), Length(min=4, max=30, message="طول نام کاربری باید بین 4 تا 30 کارکتر باشد.")])
    password = PasswordField(label='Password',
                             validators=[DataRequired(message="وارد کردن رمز عبور ضروری میباشد.")])