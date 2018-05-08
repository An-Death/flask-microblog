import factory
from factory import Sequence

from app import db
from app.models import User, Post


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = db.session

    id = Sequence(lambda x: x)
    body = factory.Faker('text', locale='ru_RU')


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = Sequence(lambda x: x)
    username = factory.Faker('name', locale='ru_RU')
    email = factory.Faker('email')
    # posts = factory.SubFactory(PostFactory, user_id=factory.SelfAttribute('..id'))
