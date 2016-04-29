import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn import cross_validation

import model
import main

class TestClassifier(unittest.TestCase):
    def test_classifications(self):
        false_positives = 0
        false_negatives = 0
        correct = 0
        wrong = 0
        engine = create_engine('sqlite:///data.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        training_data = session.query(model.Corpus).all()
        training_values = [rec.title + ' ' + rec.text for rec in training_data]
        training_targets = [rec.category for rec in training_data]
        training_values, testing_values, training_targets, testing_targets = cross_validation.train_test_split(training_values, training_targets, test_size=0.2, random_state=0)
        classifier = main.Classifier(training_values, training_targets)
        for (i, message_text) in enumerate(testing_values):
            classification = classifier.classify(message_text)[0]
            if testing_targets[i] == 'good' and classification != 'good':
                false_positives += 1
                print(message_text)
                print('[Suspected {}]'.format(classification))
                print('---')
            elif testing_targets[i] != 'good' and classification == 'good':
                false_negatives += 1
            elif testing_targets[i] == classification:
                correct += 1
            else:
                wrong += 1
        print('{} false positives ({})'.format(false_positives, float(false_positives)/len(testing_values)))
        print('{} false negatives ({})'.format(false_negatives, float(false_negatives)/len(testing_values)))
        print('{} correct ({})'.format(correct, float(correct)/len(testing_values)))
        print('{} wrong ({})'.format(wrong, float(wrong)/len(testing_values)))
        if float(false_positives) / len(testing_values) > 0.05:
            raise Exception('False positive rate too high!')
        elif float(correct) / len(testing_values) < 0.6:
            raise Exception('Correct identification rate too low!')

if __name__ == '__main__':
    unittest.main()
