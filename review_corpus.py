from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys

import main
import model
import settings

"""
Valid categories:
- resource (incl. self post blogs)
- discussion (generally non-code questions)
- good
- off_topic
- bad_question
- faq_get_started (incl. getting started with a project - where do I start?)
- faq_career
- faq_resource
- faq_tool
- faq_language
- faq_other

"""

# This allows for Python 3 compatibility by replacing input() on Python 2
if sys.version_info[:2] <= (2, 7):
    input = raw_input

if __name__ == '__main__':
    engine = create_engine(settings.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(model.Corpus).all()
    for message in data:
        print(message.title)
        print('----')
        print(message.text)
        print('')
        category = input('Enter category for post: ')
        message.category = category
        session.commit()
