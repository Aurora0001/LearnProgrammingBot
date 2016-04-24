# How it Works

The code for LearnProgrammingBot is quite simple, but the theory behind it is slightly more difficult to get to grips with. Here's a 'bird's eye view' of how LearnProgrammingBot works:

1. Train support vector machine with known data (a 'corpus')
2. Fetch latest posts from reddit
3. 'Vectorize' the post into a numpy array
4. Classify the array using the trained support vector machine
5. If the post class is not 'good', check the responses dictionary for the correct response, and reply.

Below, I'll try to explain the reasons for each of the steps and how they work.


## The Classifier
 Before explaining how LearnProgrammingBot's classifier works, it might be helpful to briefly talk about the document classification problem as a whole, and the different types of learning techniques.
 
 ### Types of Machine Learning
 There are two types of learning that are used for the majority of AI problems: **supervised learning** and **unsupervised learning**. 
 
 Supervised learning is where the algorithm is shown some samples and the correct answers, and it extrapolates so that it can answer similar questions. It's similar to how a child learns through asking questions and using the answers to predict things in the future.
 
 Unsupervised learning is less useful for classification, because we already know the correct categories. It works better for data mining (finding trends that you don't already know). 
 
 ### Classification Algorithms
 There are a few big solutions to classification problems, which all work in slightly different ways but provide similar outcomes.
 
 [Naive Bayes (NB) classifiers](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) are simple and popular classifiers which are often used for spam detection. They work on a simple principle, which Wikipedia illustrates like this:
 
 ![formula](https://upload.wikimedia.org/math/c/e/d/cedd117f3768b05f1822ae874d3fc303.png)
 
 Usually, NB classifiers work very quickly, but aren't as accurate as Support Vector Machines (SVMs). If you're interested in reading more about their competitiveness with SVMs, you can read [this paper](http://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf).
 
 [Support Vector Machines](https://en.wikipedia.org/wiki/Support_vector_machine) appear similar to NB classifiers, but they are not probability-based - they can only return either 'Category A' or 'Category B'. Essentially, they find a line in a graph that splits the two datasets as accurately as possible, like this:
 
![SVM diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Svm_separating_hyperplanes_%28SVG%29.svg/512px-Svm_separating_hyperplanes_%28SVG%29.svg.png)

It's clear that both $$H_2$$ and $$H_3$$ are suitable lines, but $$H_1$$ is incorrect. The training period allows the SVM to calculate the best line.

 As you can see, SVMs can only split data points into two groups. To allow the SVM to split data points into multiple groups, a strategy called [one-vs-the-rest](https://en.wikipedia.org/wiki/Multiclass_classification#One-vs.-rest) is used. Essentially, this makes multiple graphs, which might be like this:
 
 - 'good' vs rest
 - 'faq' vs rest
 - 'bad' vs rest
 
 Therefore, if it is in the 'rest' section for every graph but 'bad', the document must be 'bad'.
 
 