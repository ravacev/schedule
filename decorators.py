from functools import wraps
from flask import redirect, flash, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'isadmin', True)
        if not is_admin:
            message = 'You are not admin to view this page!'
            flash(message)
            return redirect(url_for('home'))
        else:
            pass
        return f(*args, **kws)
    return decorated_function