from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt

import main
import model
import settings

param_grid = [
    {
        'C': [1, 5, 10, 50],
        'loss': ['hinge', 'squared_hinge'],
        'tol': [1e-6, 1e-4, 1e-2, 1e-1],
        'multi_class': ['ovr', 'crammer_singer'],
        'class_weight': ['balanced']
    }
]

if __name__ == '__main__':
    engine = create_engine(settings.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(model.Corpus).all()
    data_values = [col.title + ' ' + col.text for col in data]
    data_targets = [col.category for col in data]
    classifier = main.Classifier()
    classifier.vectorizer.fit_transform(data_values)
    grid_search = GridSearchCV(classifier.classifier, param_grid, n_jobs=-1)
    grid_search.fit(classifier.vectorizer.transform(data_values), data_targets)
    print('Best score: {}'.format(grid_search.best_score_))
    parameters = grid_search.best_estimator_.get_params()
    for parameter in parameters.keys():
        print("{} - {}".format(parameter, parameters[parameter]))
