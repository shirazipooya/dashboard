from App import db_users, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db_users.Model, UserMixin):
    id = db_users.Column(db_users.Integer, primary_key=True)
    username = db_users.Column(db_users.String(30), unique=True, nullable=False)
    password = db_users.Column(db_users.String(60), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.username})"
