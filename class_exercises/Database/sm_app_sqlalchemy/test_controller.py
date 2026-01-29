import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError

from .models import User, Comment, Post, Base
from .write_to_db import write_initial_data
from .controller import Controller

# test_db_location = 'sqlite:///:memory:'
test_db_location = 'sqlite:///test_sm.db'


class TestDataBase:
    @pytest.fixture(scope="class")
    def db_session(self):
        engine = sa.create_engine(test_db_location, echo=False)
        Base.metadata.create_all(engine)
        session = so.Session(bind=engine)
        yield session
        session.close()
        Base.metadata.drop_all(engine)

    def test_valid_user(self, db_session):
        """ Checks that a User can be added and retrieved from the database"""
        user = User(name = "Bob Dylan", age=81, gender="male")
        db_session.add(user)
        db_session.commit()
        qry = sa.select(User).where(User.name=="Bob Dylan")
        bob = db_session.scalar(qry)
        assert bob.name == "Bob Dylan"
        assert bob.age == 81
        assert bob.gender == "male"
        assert bob.nationality is None


    def test_invalid_user(self, db_session):
        """ Checks that a User missing a name can not be added"""
        user = User(age=7, nationality='British')
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_add_post(self, db_session):
        """ Test creating a user and adding a post to that user
        - check that the post is including in user.posts and the user
        is included in post.user"""
        user = User(name="Eleonore", age=20, gender="female")
        post = Post(title="Hello", description="Hello World")
        user.posts.append(post)
        db_session.add(user)
        db_session.commit()
        eleonore = db_session.scalar(sa.select(User).where(User.name == "Eleonore"))
        assert eleonore.posts == [post,]
        e_post = eleonore.posts[0]
        assert e_post.title == "Hello"
        assert e_post.description == "Hello World"
        assert e_post.user == user

class TestController:
    # Set up a test database fixture by creating the database and writing in initial data
    @pytest.fixture(scope="class", autouse=True)
    def test_db(self):
        engine = sa.create_engine(test_db_location, echo=False)
        Base.metadata.create_all(engine)
        write_initial_data(engine)
        yield
        # After the fixture is used drop the data from database in memory
        Base.metadata.drop_all(engine)

    @pytest.fixture(scope="class")
    def controller(self):
        control = Controller(db_location=test_db_location)
        return control

    def test_set_current_user_from_name(self, controller):
        controller.set_current_user_from_name('Alice')
        assert controller.current_user.name == 'Alice'
        assert controller.current_user.age == 30

    def test_get_user_names(self, controller):
        names = controller.get_user_names()
        assert names == ['Alice', 'Bob', 'Charlie', 'Diana']

    def test_create_user(self, controller):
        user = controller.create_user("Mary", 30, "Female", "Dutch")
        assert controller.current_user.name == "Mary"
        assert controller.current_user == user

    def test_get_posts(self, controller):
        alice_posts = controller.get_posts('Alice')
        assert alice_posts[0] == {'id': 1,
                                  'title': 'Exploring the Rocky Mountains',
                                  'description': 'Just returned from an amazing trip to the Rockies! The views were breathtaking and the hikes were exhilarating.',
                                  'number_likes': 2,
                                }
        # print(controller.current_posts)
        assert(len(controller.current_posts) == 1)

    def test_delete_user(self, controller):
        controller.delete_user('Alice')
        alice_posts = controller.get_posts('Alice')
        assert alice_posts is None

    def test_get_comments(self):
        assert False

    def test_add_comment(self, controller):
        assert False

    def test_add_post(self):
        assert False

    def test_like_post(self):
        assert False
