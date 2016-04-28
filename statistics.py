from sklearn.learning_curve import learning_curve
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt

import main
import model
import settings

if __name__ == '__main__':
    # Adapted from http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html (BSD license)
    engine = create_engine(settings.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(model.Corpus).all()
    data_values = [col.title + ' ' + col.text for col in data]
    data_targets = [col.category for col in data]
    classifier = main.Classifier()
    classifier.vectorizer.fit_transform(data_values)
    train_sizes, train_scores, test_scores = learning_curve(classifier.classifier, classifier.vectorizer.transform(data_values), data_targets, cv=6)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.figure()
    plt.title('LearnProgrammingBot Training Scores')
    plt.xlabel("Training Samples")
    plt.ylabel("Accuracy")
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")
    plt.ylim(0, 1)
    plt.show()
