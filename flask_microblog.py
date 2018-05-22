from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    context = {
        'db': db,
        'User': User,
        'Post': Post
    }
    return context


if __name__ == '__main__':
    app.run()
