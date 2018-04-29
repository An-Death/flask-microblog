from app import login
from .blog import *


@login.user_loader
def load_user(id):
    return User.query.get(id)
