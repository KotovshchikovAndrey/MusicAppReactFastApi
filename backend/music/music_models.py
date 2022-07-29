from db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    music = relationship("Music", backref='author')

    def __str__(self) -> str:
        return self.name


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text())
    file_name = Column(String(255), nullable=True)
    author_id = Column(ForeignKey('authors.id', ondelete='CASCADE'), nullable=True)

    def __str__(self) -> str:
        return self.title