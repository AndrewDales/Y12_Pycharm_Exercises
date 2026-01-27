import sqlalchemy as sa
import sqlalchemy.orm as so

from Database.sm_app_sqlalchemy.models import User, Post, Comment


class Controller:
    def __init__(self, db_location = 'sqlite:///social_media.db'):
        self.current_user = None
        self.current_posts = None
        self.engine = sa.create_engine(db_location)

    def set_current_user_from_name(self, name):
        with so.Session(bind=self.engine) as session:
            self.current_user = session.scalars(sa.select(User).where(User.name == name)).one_or_none()

    def get_user_names(self) -> list[str]:
        with so.Session(bind=self.engine) as session:
            user_names = session.scalars(sa.select(User.name).order_by(User.name)).all()
        return list(user_names)

    def create_user(self, name: str, age: int, gender: str, nationality: str) -> User:
        with so.Session(bind=self.engine) as session:
            user = User(name=name, age=age, gender=gender, nationality=nationality)
            session.add(user)
            session.commit()
            self.set_current_user_from_name(user.name)
        return self.current_user

    def get_posts(self, user_name: str) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            user = session.scalars(sa.select(User).where(User.name == user_name)).one_or_none()
            posts_info = [{'id': post.id,
                           'title' : post.title,
                           'description': post.description,
                           'number_likes': len(post.liked_by_users),
                           }
                          for post in user.posts]
            self.current_posts = user.posts
        return posts_info


    def get_comments(self, post_id) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            post = session.get(Post, post_id)
            comments_info = [{'comment': comment.comment,
                              'author': comment.user.name,}
                             for comment in post.comments]
        return comments_info

    def add_post(self, title, description):
        with so.Session(bind=self.engine) as session:
            user = session.merge(self.current_user)
            post = Post(title=title, description=description)
            user.posts.append(post)
            session.commit()

    def like_post(self, post_id):
        with so.Session(bind=self.engine) as session:
            user = session.merge(self.current_user)
            post = session.get(Post, post_id)
            if user in post.liked_by_users:
                post.liked_by_users.remove(user)
            else:
                post.liked_by_users.append(user)
            session.commit()

    def comment_on_post(self, post_id, comment):
        with so.Session(bind=self.engine) as session:
            user_id = self.current_user.id
            post = session.get(Post, post_id)
            new_comment = Comment(user_id=user_id, comment=comment)
            post.comments.append(new_comment)

if __name__ == '__main__':
    controller = Controller()