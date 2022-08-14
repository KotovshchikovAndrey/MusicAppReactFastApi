from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete='CASCADE'), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete='CASCADE'), primary_key=True),
)


user_favorite_music = Table(
    "user_favorite_music",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete='CASCADE'), primary_key=True),
    Column("music_id", ForeignKey("music.id", ondelete='CASCADE'), primary_key=True),
)


user_last_music = Table(
    "user_last_music",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete='CASCADE'), primary_key=True),
    Column("music_id", ForeignKey("music.id", ondelete='CASCADE'), primary_key=True),
)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    role_name = Column(String(255), nullable=False, unique=True)
    users = relationship("User", secondary=user_role, back_populates='roles')

    def __str__(self) -> str:
        return self.role_name


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    last_music = relationship("Music", secondary=user_last_music)
    favorite_music = relationship("Music", secondary=user_favorite_music)
    roles = relationship("Role", secondary=user_role, back_populates='users')
    tokens = relationship("JwtToken", backref='user')
    
    def __str__(self) -> str:
        return self.username


class JwtToken(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    refresh_token = Column(String, nullable=False, unique=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    def __str__(self) -> str:
        return self.refresh_token
