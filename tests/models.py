import unittest

from app import db
from app.models import User
from tests.factories import UserFactory, PostFactory


class TestHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()


class TestUserModel(TestHelper):
    def setUp(self):
        self.post = PostFactory()
        self.user = UserFactory(posts=(self.post,))
        db.session.commit()

    def test_UserModel_password_hashing_must_return_True_for_equals_passwords(self):
        test_password = 'test'
        self.user.set_password(test_password)
        self.assertTrue(self.user.check_password(test_password))

    def test_UserModel_password_hashing_must_return_False_for_non_equals_passwords(self):
        self.user.set_password('test_password')
        self.assertFalse(self.user.check_password('other_pass'))

    def test_UserModel_must_have_post(self):
        posts = self.user.posts.all()
        self.assertListEqual([self.post], posts)

    def test_UserModel_must_return_empty_list_if_user_have_not_posts(self):
        self.user.posts.delete()
        self.assertListEqual([], self.user.posts.all())

    def test_UserModel_is_exist_classmethod_must_return_True_for_exist_user(self):
        self.assertTrue(User.is_exist(username=self.user.username))

    def test_UserModel_is_exist_classmethod_must_return_False_for_not_existed_user(self):
        self.assertFalse(User.is_exist(username='that username cannot be exist'))

    def test_UserModel_is_following_method_must_return_False_if_new_user_not_in_followed_list(self):
        new_user = UserFactory()
        self.assertFalse(self.user.is_following(new_user))

    def test_UserModel_is_following_method_must_return_True_if_new_user_in_followed_list(self):
        new_user = UserFactory()
        self.user.followed.append(new_user)
        self.assertTrue(self.user.is_following(new_user))

    def test_UserModel_follow_method_must_append_new_user_to_followed(self):
        new_user = UserFactory()
        self.user.follow(new_user)
        self.assertIn(new_user, self.user.followed.all())

    def test_UserModel_follow_method_must_append_user_to_followers_of_new_user(self):
        new_user = UserFactory()
        self.user.follow(new_user)
        self.assertIn(self.user, new_user.followers.all())

    def test_UserModel_unfollow_method_must_remove_new_user_from_followed_list_of_user(self):
        new_user = UserFactory()
        self.user.followed.append(new_user)
        self.user.unfollow(new_user)
        self.assertNotIn(new_user, self.user.followed.all())
        self.assertNotIn(self.user, new_user.followers.all())

    def test_UserModel_followed_post_must_returned_list_must_contain_post1_and_post2(self):
        new_user = UserFactory()
        post1 = PostFactory(author=new_user)
        post2 = PostFactory(author=new_user)
        self.user.followed.append(new_user)
        user_posts = self.user.followed_posts().all()
        self.assertIn(post1, user_posts)
        self.assertIn(post2, user_posts)

    def test_UserModel_followed_post_must_return_list_of_new_user_posts_with_own_user_posts(self):
        new_user = UserFactory()
        post1 = PostFactory(author=new_user)
        post2 = PostFactory(author=new_user)
        self.user.followed.append(new_user)
        expected = [post2, post1, *self.user.posts.all()]
        self.assertListEqual(expected, list(self.user.followed_posts()))
