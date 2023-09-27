from .connect import db_supporters
# def get_admins():
#     users = db_admins.find({},{"_id":1})
#     return users

def supporters_list():
    admins = db_supporters.find({},{"_id":1})
    admins_id = []
    for admin in admins:
        admin = admin['_id']
        admins_id.append(admin)
    return admins_id