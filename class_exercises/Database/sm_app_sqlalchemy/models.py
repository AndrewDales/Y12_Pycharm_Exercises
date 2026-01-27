import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import Mapped

# Base is called an Abstract Base Class - our SQL Alchemy models will inherit from this class
class Base(so.DeclarativeBase):
    pass

# Define the likes table as a secondary table
likes_table = sa.Table(
    'likes',
    Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id'), nullable=False),
)

class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(unique=True)
    age: so.Mapped[int|None]
    gender: so.Mapped[str|None]
    nationality: so.Mapped[str|None]
    posts: so.Mapped[list['Post']] = so.relationship(back_populates='user')
    liked_posts: so.Mapped[list['Post']] = so.relationship(secondary=likes_table, back_populates='liked_by_users')
    comments_made: so.Mapped[list['Comment']] = so.relationship(back_populates='user')

    def __repr__(self):
        return f"User(name='{self.name}', age={self.age}, gender='{self.gender}', nationality='{self.nationality}')"

class Post(Base):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str]
    description: so.Mapped[str]
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    user: so.Mapped["User"] = so.relationship(back_populates='posts')
    liked_by_users: so.Mapped[list["User"]] = so.relationship(secondary=likes_table,
                                                              back_populates='liked_posts')
    comments: so.Mapped[list["Comment"]] = so.relationship(back_populates='post')

    @property
    def number_of_likes(self) -> int:
        return len(self.liked_by_users)

    def __repr__(self):
        return f"Post(title='{self.title}', description='{self.description}', user={self.user.name})"

class Comment(Base):
    __tablename__ = 'comments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('posts.id'))
    comment: so.Mapped[str]
    post: so.Mapped['Post'] = so.relationship(back_populates='comments')
    user: so.Mapped['User'] = so.relationship(back_populates='comments_made')

    def __repr__(self):
        return f"Comment(user_id={self.user_id}, post_id={self.post_id}, comment='{self.comment}')"