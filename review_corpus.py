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
- off_topic (incl. bad questions)
- bad_question (todo: merge with off_topic?)
- faq_get_started (incl. getting started with a project - where do I start?)
- faq_career
- faq_resource
- faq_tool (incl. laptop specs)
- faq_language (e.g. how much should I know before I am expert, which should I
pick)
- faq_other (including motivation etc.)

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
