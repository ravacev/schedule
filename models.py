from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

def create_password(password):
    return generate_password_hash(password)

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


class User(UserMixin):
    def __init__(self, id, username, password, email, isadmin, active):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.isadmin = isadmin
        self.active = active
        
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
    
    def is_admin(self):
        return True
        
    def __repr__(self):
        return f'<User {self.username}>'
    
    # def verify_password(self, password):
    #     return check_password(password, self.password)