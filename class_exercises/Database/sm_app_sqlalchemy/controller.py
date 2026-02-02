import sqlalchemy as sa
import sqlalchemy.orm as so

from class_exercises.Database.sm_app_sqlalchemy.models import User, Post, Comment


class Controller:
    def __init__(self, db_location = 'sqlite:///social_media.db'):
        self.current_user_id: int|None = None
        self.viewing_post_user_id: int|None = None
        self.engine = sa.create_engine(db_location)

    def set_current_user_from_name(self, name:str) -> User|None:
        with so.Session(bind=self.engine) as session:
            user = session.scalars(sa.select(User).where(User.name == name)).one_or_none()

            if user is None:
                # Fallback behaviour: clear current user and return None
                self.current_user_id = None
                return None

            self.current_user_id = user.id
        return user

    def get_user_names(self) -> list[str]:
        with so.Session(bind=self.engine) as session:
            user_names = session.scalars(sa.select(User.name).order_by(User.name)).all()
        return list(user_names)

    def create_user(self, name: str, age: int, gender: str, nationality: str) -> User:
        with so.Session(bind=self.engine) as session:
            user = User(name=name, age=age, gender=gender, nationality=nationality)
            session.add(user)
            session.commit()
            # Sets current user to the newly-created user
            self.set_current_user_from_name(user.name)
        return user

    def get_user_info(self, user_id: int|None = None) -> dict:
        if user_id is None:
            user_id = self.current_user_id

        with so.Session(bind=self.engine) as session:
            user = session.get(User, user_id)
            user_info = {'name': user.name,
                         'age': user.age,
                         'gender': user.gender,
                         'nationality': user.nationality,
                         }
            return user_info

    def get_user_posts(self, user_name: str) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            user = session.scalars(sa.select(User).where(User.name == user_name)).one_or_none()
            posts_info = [{'id': post.id,
                           'title' : post.title,
                           'description': post.description,
                           'number_likes': len(post.liked_by_users),
                           }
                          for post in user.posts]
            self.viewing_post_user_id = user.id
        return posts_info


    def get_comments(self, post_id) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            post = session.get(Post, post_id)
            comments_info = [{'comment': comment.comment,
                              'author': comment.user.name,}
                             for comment in post.comments]
        return comments_info

    def write_new_post(self, title, description, user_id = None) -> int:
        if user_id is None:
            user_id = self.current_user_id

        with so.Session(bind=self.engine) as session:
            # Quick method to SELECT one record via a primary key id
            user = session.get(User, user_id)
            post = Post(title=title, description=description)
            post_id = post.id
            user.posts.append(post)
            session.commit()
        return post_id

    def like_post_toggle(self, post_id, user_id = None):
        if user_id is None:
            user_id = self.current_user_id

        with so.Session(bind=self.engine) as session:
            user = session.get(User, user_id)
            post = session.get(Post, post_id)
            if user in post.liked_by_users:
                post.liked_by_users.remove(user)
            else:
                post.liked_by_users.append(user)
            session.commit()

    def comment_on_post(self, post_id, comment, user_id = None):
        if user_id is None:
            user_id = self.current_user_id

        with so.Session(bind=self.engine) as session:
            post = session.get(Post, post_id)
            new_comment = Comment(user_id=user_id, comment=comment)
            post.comments.append(new_comment)

if __name__ == '__main__':
    controller = Controller()
    controller.set_current_user_from_name('Alice')