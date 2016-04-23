#!/usr/bin/python2

from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
import logging
import webbrowser
import argparse
import sys

from settings import LOGFILE_URI, DATABASE_URI, LOG_LEVEL, CLIENT_ID, CLIENT_SECRET, CLIENT_ACCESSCODE, SUBREDDIT
import model
import praw

# This allows for Python 3 compatibility by replacing input() on Python 2
if sys.version_info[:2] <= (2, 7):
    input = raw_input

responses = {
    'bad': '''
Hi! Your post doesn't seem very suitable for /r/learnprogramming. This may be because you didn't include a code sample, provided very little detail or linked content that doesn't seem relevant. You can improve your post by:

- [Asking Questions The Smart Way](http://catb.org/~esr/faqs/smart-questions.html)
- Avoiding posting links without any explanation, discussion or question
- Using code pastebins (images don't count!)
- Reviewing the post guidelines on the sidebar

Don't worry about this message if you think your post **is** relevant - it may just be an error in my classifier - but please check the resources above anyway to make sure that your post is good.

*I am a bot for /r/learnprogramming using supervised learning to detect common questions. If this message is irrelevant or unhelpful, please report an issue so I can improve my classifier!*
    ''',
    'faq': '''
Hello! Your post seems similar to one of the common questions answered in the [/r/learnprogramming FAQ](https://www.reddit.com/r/learnprogramming/wiki/faq), and you might find an answer to your question there.

Links that may be useful to you:

- [Programming Resources](https://www.reddit.com/r/learnprogramming/wiki/online)
- [/r/cscareerquestions](https://www.reddit.com/r/cscareerquestions)
- [Getting Started with Programming](https://www.reddit.com/r/learnprogramming/wiki/gettingstarted)

*I am a bot for /r/learnprogramming using supervised learning to detect common questions. Your post was recognised as an faq question. If this seems irrelevant or unhelpful, please report an issue on GitHub!*
    '''
}

class Classifier(object):
    def __init__(self, training_values, training_targets):
        self.vectorizer = TfidfVectorizer()
        self.classifier = OneVsRestClassifier(svm.LinearSVC(class_weight='balanced'))
        training_values = self.vectorizer.fit_transform(training_values).toarray()
        self.classifier.fit(training_values, training_targets)

    def classify(self, text):
        transformed_text = self.vectorizer.transform([text]).toarray()
        return self.classifier.predict(transformed_text)

def connect_to_database(uri):
    engine = create_engine(uri)
    return sessionmaker(bind=engine)

def get_reddit_client():
    reddit = praw.Reddit(user_agent='test')
    reddit.set_oauth_app_info(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://127.0.0.1/callback')
    return reddit

def run_bot(args):
    logging.basicConfig(filename=LOGFILE_URI, level=LOG_LEVEL)

    logging.info('Connecting to database {}'.format(DATABASE_URI))
    Session = connect_to_database(DATABASE_URI)
    logging.info('Database connection OK')

    session = Session()
    data = session.query(model.Corpus).all()

    data_values = [col.title + ' ' + col.text for col in data]
    data_targets = [col.category for col in data]

    logging.info('Training classifier with {} values'.format(len(data_values)))
    classifier = Classifier(data_values, data_targets)
    logging.info('Classifier trained')

    logging.info('Connecting to reddit...')
    reddit = get_reddit_client()

    logging.info('Authorizing...')
    access_information = reddit.get_access_information(CLIENT_ACCESSCODE)
    reddit.set_access_credentials(**access_information)
    logging.info('Logged in successfully.')

    for message in praw.helpers.submission_stream(reddit, SUBREDDIT, limit=5, verbosity=0):
        message_text = message.title + ' ' + message.selftext
        pred = classifier.classify(message_text)[0]
        if pred != 'good':
            try:
                message.add_comment(responses[pred])
            except praw.errors.RateLimitExceeded:
                logging.error('Rate limit exceeded, cannot post to thread {}'.format(message.title))

def train_bot(args):
    reddit = get_reddit_client()
    message = reddit.get_submission(submission_id=args.id)
    print(message.title)
    print('----------')
    print(message.selftext)
    print('')
    message_type = input('Enter category: ')
    Session = connect_to_database(DATABASE_URI)
    session = Session()
    session.add(model.Corpus(title=message.title, text=message.selftext, category=message_type))
    session.commit()

def create_token(args):
    url = reddit.get_authorize_url('uniqueKey', 'identity,submit,read', True)
    webbrowser.open(url)
    print('Please copy the access code that you are redirected to:')
    print('Like this: http://praw.readthedocs.org/en/latest/_images/CodeUrl.png')
    print('Put it in settings.py as CLIENT_ACCESSCODE')

def initialise_database(args):
    engine = create_engine(DATABASE_URI)
    model.Corpus.metadata.create_all(engine)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_run = subparsers.add_parser('run', help='runs the bot')
    parser_run.set_defaults(func=run_bot)
    parser_train = subparsers.add_parser('train', help='adds training data to the bot')
    parser_train.add_argument('--id', type=str, required=True, help='the submission id of the post to review')
    parser_train.set_defaults(func=train_bot)
    parser_token = subparsers.add_parser('create-token', help='gets an access token with your client id/secret')
    parser_token.set_defaults(func=create_token)
    parser_init = subparsers.add_parser('init', help='initialises the database, ready to insert training data')
    parser_init.set_defaults(func=initialise_database)
    args = parser.parse_args(sys.argv[1:])
    args.func(args)
