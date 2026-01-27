
# models.py
from __future__ import annotations

import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

# ---------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------
class Base(so.DeclarativeBase):
    pass


# ---------------------------------------------------------------------
# Association table (many-to-many) for likes
# Composite PK prevents duplicate likes; no surrogate id needed
# ---------------------------------------------------------------------
likes_table = sa.Table(
    "likes",
    Base.metadata,
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    sa.Column(
        "post_id",
        sa.Integer,
        sa.ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    sa.Index("ix_likes_user", "user_id"),
    sa.Index("ix_likes_post", "post_id"),
)


# ---------------------------------------------------------------------
# User
# ---------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(80), unique=True, nullable=False, index=True)

    # Make profile fields nullable (if you allow blanks in CLI), else set nullable=False
    age: Mapped[int | None] = mapped_column(nullable=True)
    gender: Mapped[str | None] = mapped_column(sa.String(30), nullable=True)
    nationality: Mapped[str | None] = mapped_column(sa.String(60), nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
    )

    # One-to-many: posts authored by the user
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",   # delete posts when user is deleted
        passive_deletes=True,
        lazy="selectin",
        order_by="Post.id",
    )

    # Many-to-many: posts liked by the user
    liked_posts: Mapped[list["Post"]] = relationship(
        secondary=likes_table,
        back_populates="liked_by_users",
        lazy="selectin",
    )

    # One-to-many: comments authored by the user
    comments_made: Mapped[list["Comment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
        order_by="Comment.id",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"


# ---------------------------------------------------------------------
# Post
# ---------------------------------------------------------------------
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(120), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
    )

    # Author (many posts -> one user)
    user: Mapped["User"] = relationship(
        back_populates="posts",
        lazy="joined",  # Often you show author with post; joined keeps it efficient
    )

    # Many-to-many: users who liked this post
    liked_by_users: Mapped[list["User"]] = relationship(
        secondary=likes_table,
        back_populates="liked_posts",
        lazy="selectin",
    )

    # One-to-many: comments under this post
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
        order_by="Comment.id",
    )

    # --- Like counts ---
    @hybrid_property
    def number_of_likes(self) -> int:
        # Works on loaded instances (Python-side)
        return len(self.liked_by_users)

    @number_of_likes.expression  # type: ignore[misc]
    def number_of_likes(cls) -> sa.ColumnElement[int]:
        # Works in SQL (e.g., ORDER BY Post.number_of_likes)
        return (
            sa.select(sa.func.count(likes_table.c.user_id))
            .where(likes_table.c.post_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r}, user_id={self.user_id})"


# ---------------------------------------------------------------------
# Comment
# ---------------------------------------------------------------------
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,  # allow keeping comments even if user is deleted
        index=True,
    )
    post_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    comment: Mapped[str] = mapped_column(sa.Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
    )

    # Relationships
    post: Mapped["Post"] = relationship(
        back_populates="comments",
        lazy="joined",  # often show comment with its post id already known; joined is okay
    )

    user: Mapped["User"] = relationship(
        back_populates="comments_made",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, post_id={self.post_id}, user_id={self.user_id})"
