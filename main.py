#!/usr/bin/python2

from __future__ import print_function

from sklearn.pipeline import make_union
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
import numpy as np
import logging
import webbrowser
import argparse
import sys

from settings import LOGFILE_URI, DATABASE_URI, LOG_LEVEL, CLIENT_ID, CLIENT_SECRET, CLIENT_ACCESSCODE, SUBREDDIT, REDIRECT_URI, LOG_FORMAT
import model
import praw

# This allows for Python 3 compatibility by replacing input() on Python 2
if sys.version_info[:2] <= (2, 7):
    input = raw_input

responses = {
    'bad': '''
Hi! Your post might not attract good responses on /r/learnprogramming.
This may be because you didn't include a code sample, provided very little
detail or linked content that doesn't seem relevant. You can improve your post
by:

- [Asking Questions The Smart Way](http://catb.org/~esr/faqs/smart-questions.html)
- Avoiding posting links without any explanation, discussion or question (links
might get a better response on /r/programming)
- Using code pastebins (images don't count!)
- Reviewing the post guidelines on the sidebar

Don't worry about this message if you think it's a mistake - it may just be an
error in my classifier - but please check the resources above anyway to make
sure that your post gets the best responses.

---
I am a bot for /r/learnprogramming using supervised learning to provide helpful
responses to common posts.

[[Learn More]](https://github.com/Aurora0001/LearnProgrammingBot)
[[Report an Issue]](https://github.com/Aurora0001/LearnProgrammingBot/issues)
    ''',
    'faq': '''
Hello! Your post seems similar to one of the common questions answered in the
[/r/learnprogramming FAQ](https://www.reddit.com/r/learnprogramming/wiki/faq),
and you might find an answer to your question there.

Links that may be useful to you:

- [Programming Resources](https://www.reddit.com/r/learnprogramming/wiki/online)
- [/r/cscareerquestions](https://www.reddit.com/r/cscareerquestions)
- [Getting Started with Programming](https://www.reddit.com/r/learnprogramming/wiki/gettingstarted)

---
I am a bot for /r/learnprogramming using supervised learning to provide helpful
responses to common posts.

[[Learn More]](https://github.com/Aurora0001/LearnProgrammingBot)
[[Report an Issue]](https://github.com/Aurora0001/LearnProgrammingBot/issues)
    '''
}

class PostTransformer(TransformerMixin):
    """
    Transforms posts on four characteristics:
    - Amount of links
    - Length of post
    - Contains block code
    - Contains inline code
    """
    def __init__(self):
        pass

    def fit(self, *args):
        return self

    def transform(self, X, *args, **kwargs):
        ret = []
        for item in X:
            ret.append(float(len(item)) / 10000)
            ret.append(item.count('http'))
            ret.append('    ' in item)
            ret.append('`' in item)

        y = np.array(ret).reshape(-1, 4)
        return y

    fit_transform = transform

class Classifier(object):
    """
    Wrapper for the vectorizer and classifier that handles training of both.
    """
    def __init__(self, training_values=None, training_targets=None):
        self.vectorizer = make_union(TfidfVectorizer(), PostTransformer())
        # Set using parameter_search. TODO: review after updating
        # corpus.
        self.classifier = svm.LinearSVC(C=5, loss='squared_hinge', multi_class='crammer_singer', class_weight='balanced', tol=0.1)
        if training_values is not None and training_targets is not None:
            self.fit(training_values, training_targets)

    def fit(self, training_values, training_targets):
        training_values = self.vectorizer.fit_transform(training_values).toarray()
        self.classifier.fit(training_values, training_targets)

    def classify(self, text):
        transformed_text = self.vectorizer.transform([text]).toarray()
        return self.classifier.predict(transformed_text)

    def get_probability(self, text):
        transformed_text = self.vectorizer.transform([text]).toarray()
        return self.classifier.decision_function(transformed_text)

def connect_to_database(uri):
    engine = create_engine(uri)
    return sessionmaker(bind=engine)

def get_reddit_client():
    reddit = praw.Reddit(user_agent='all platforms:Learn Programming Bot:v0.2.0-pre (by /u/Aurora0001, contact at github.com/Aurora0001/LearnProgrammingBot/issues)')
    reddit.set_oauth_app_info(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    return reddit

def run_bot(args):
    logging.basicConfig(filename=LOGFILE_URI, level=LOG_LEVEL, format=LOG_FORMAT)

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
                # TODO:
                # Ideally, errors should actually be handled properly. Perhaps a dequeue could be used
                # to store all the posts which failed, which could be retried every minute (or so)
                logging.error('Rate limit exceeded, cannot post to thread {}'.format(message.title))

def train_id(args):
    train_bot(args, True)

def train_batch(args):
    train_bot(args, False)

def train_bot(args, by_id):
    reddit = get_reddit_client()
    if by_id:
        messages = [reddit.get_submission(submission_id=args.id)]
    else:
        messages = reddit.get_subreddit(SUBREDDIT).get_new(limit=args.limit)
    for message in messages:
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
    reddit = get_reddit_client()
    url = reddit.get_authorize_url('uniqueKey', 'identity,submit,read', True)
    webbrowser.open(url)
    print('                   !!!                    ')
    print('Please copy the access code that you are redirected to ')
    print('like this: http://praw.readthedocs.org/en/latest/_images/CodeUrl.png')
    print('You need to put it in settings.py as CLIENT_ACCESSCODE')
    print('                   !!!                    ')

def classify_item(args):
    reddit = get_reddit_client()
    post = reddit.get_submission(submission_id=args.id)

    Session = connect_to_database(DATABASE_URI)
    session = Session()

    data = session.query(model.Corpus).all()
    data_values = [col.title + ' ' + col.text for col in data]
    data_targets = [col.category for col in data]

    classifier = Classifier(data_values, data_targets)
    post_text = post.title + ' ' + post.selftext
    classification = classifier.classify(post_text)[0]
    probability = classifier.get_probability(post_text)[0]
    print('p({}) = {}'.format(classification, max(probability)))
    print('All probabilities: {}'.format(probability))
    print('p(event) = -1 means that the classifier is certain that the post is not in this category.')
    print('p(event) = 1 means that the classifier is certain that the post is in this category.')

def initialise_database(args):
    engine = create_engine(DATABASE_URI)
    model.Corpus.metadata.create_all(engine)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_run = subparsers.add_parser('run', help='runs the bot')
    parser_run.set_defaults(func=run_bot)
    parser_train = subparsers.add_parser('train', help='adds training data to the bot (using a specific id)')
    parser_train.add_argument('--id', type=str, required=True, help='the submission id of the post to review')
    parser_train.set_defaults(func=train_id)
    parser_batch = subparsers.add_parser('train-batch', help='adds training data to the bot in batches')
    parser_batch.add_argument('--limit', type=int, required=True, help='the maximum number of posts to fetch')
    parser_batch.set_defaults(func=train_batch)
    parser_token = subparsers.add_parser('create-token', help='gets an access token with your client id/secret')
    parser_token.set_defaults(func=create_token)
    parser_init = subparsers.add_parser('init', help='initialises the database, ready to insert training data')
    parser_init.set_defaults(func=initialise_database)
    parser_classify = subparsers.add_parser('classify', help='classifies a specific post using the trained data')
    parser_classify.add_argument('--id', type=str, required=True, help='the submission id of the post to classify')
    parser_classify.set_defaults(func=classify_item)
    args = parser.parse_args(sys.argv[1:])
    args.func(args)
