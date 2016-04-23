from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Corpus(Base):
    __tablename__ = 'corpora'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
