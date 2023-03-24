from models import User
import query

class user_create():
    test = query.test.account
    users = []
    
    for value in range(len(test)):
        users.append(User(id = test[value]['idusers'], username = test[value]['username'], password = test[value]['password'], email = test[value]['email'], isadmin = bool(test[value]['isadmin'])))
        # users.insert(value, test[value]['idusers'], test[value]['username'], test[value]['password'], test[value]['email'], test[value]['isadmin'])