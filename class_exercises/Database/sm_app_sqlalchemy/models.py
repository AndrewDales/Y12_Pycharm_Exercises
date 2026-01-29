# class_exercises/Database/sm_app_sqlalchemy/models.py

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

# Base is called an Abstract Base Class - our SQL Alchemy models will inherit from this class
class Base(so.DeclarativeBase):
    pass

# Define the likes table as a secondary table
# The primary key for the table is set to be the composite key from the two FKs
likes_table = sa.Table(
    'likes',
    Base.metadata,
    sa.Column('user_id', sa.Integer,
              sa.ForeignKey(column='users.id', ondelete='CASCADE'),
              primary_key=True),
    sa.Column('post_id', sa.Integer,
              sa.ForeignKey(column='posts.id', ondelete='CASCADE'),
              primary_key=True),
)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    age: Mapped[Optional[int]]
    gender: Mapped[Optional[str]]
    nationality: Mapped[Optional[str]]
    # One-to-many: posts authored by the user
    posts: Mapped[list['Post']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    # Many-to-many: posts that are liked by the user - defined by the likes table
    liked_posts: Mapped[list['Post']] = relationship(
        secondary=likes_table,
        back_populates='liked_by_users',
    )
    # One-to-many: Comments authored by the user
    comments_made: Mapped[list['Comment']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f"User(name='{self.name}', age={self.age}, gender='{self.gender}', nationality='{self.nationality}')"

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    # Many-to-many: which users liked this post
    liked_by_users: Mapped[List["User"]] = relationship(
        secondary=likes_table,
        back_populates='liked_posts',
    )

    # Author (many posts -> one user)
    user: Mapped["User"] = relationship(
        back_populates='posts',
    )

    # One-to-many: comments that are made about this post
    comments: Mapped[List["Comment"]] = relationship(
        back_populates='post',
        cascade='all, delete-orphan',
    )

    # For efficiency, it would be better to include this as a column_property with a subquery to count the users
    @property
    def number_of_likes(self) -> int:
        return len(self.liked_by_users)

    def __repr__(self):
        return f"Post(title='{self.title}', description='{self.description}', user={self.user.name})"

class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    comment: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    post_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False
    )

    # Many-to-one relationship defining the author of a comment
    user: Mapped['User'] = so.relationship(back_populates='comments_made')

    # Many-to-one relationship defining the post which is being commented about
    post: Mapped['Post'] = so.relationship(back_populates='comments')


    def __repr__(self):
        return f"Comment(user_id={self.user_id}, post_id={self.post_id}, comment='{self.comment}')"


