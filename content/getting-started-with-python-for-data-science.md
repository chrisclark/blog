Title: Getting Started With Python for Data Science
Date: 2012-07-20 22:17
Author: Chris Clark
Slug: getting-started-with-python-for-data
Category: Code & Tutorials

As the product manager at [Kaggle](http://www.kaggle.com/)
I'm fortunate enough to hang around with some of the world's top machine
learning experts. And working at a place that specializes in running
predictive modelling competitions means that I inevitably got the itch
to learn some of this stuff myself.

I don't have a super-strong math or machine learning background, but I
figured I'm a decent-enough programmer and have all these smart people
around me, so I figured I should be able to figure out how to use some
off-the-shelf tools to build some predictive models of my own.

I wrote the following tutorial after my experience hacking away on a
Kaggle competition for a weekend. I hope it serves to get other
programming-literate but machine learning-ignorant people like me up and
running, building their own models, and learning data science. So
without further ado...

## Who is this for and what will I learn?

(Cross posted on Kaggle's blog, [No Free Hunch](http://blog.kaggle.com/).)

This tutorial assumes some knowledge of Python and programming, but no
knowledge whatsoever of data science, machine learning, or predictive
modeling (or, heck, even statistics). To the extent there is a target
audience, it's probably hacker types who learn best by doing.

**All the code from this tutorial is available
on [github](https://github.com/chrisclark/PythonForDataScience).**

You might encounter terms you're not familiar with, but that shouldn't
stop you from completing the tutorial. By the end, you won't know a heck
of a lot more about data science *per se*, but you'll have a nice
environment set up where you can easily play with lots of different data
science tools and even make credible entries to Kaggle competitions.
Most importantly you'll be in a great position to experiment and learn
more data science.

Here's what you'll learn:

-   How to install popular scientific and statistical computing
    libraries for Python
-   Use those libraries to create a benchmark model and submit it to
    a competition.
-   Write your own evaluation function, and learn how to use
    cross-validation to  
   test out ideas on your own.

Excited? I thought so!

## 1. Environment Setup

First thing, we'll need a Python environment suitable for scientific and
statistical computing. Assuming you already have Python installed (no?
Well then [get it](http://www.python.org/getit/)! Python 2.7 is
recommended), we'll need three packages. You should install each in the
order they appear here:

-   [numpy](http://sourceforge.net/projects/numpy/files/) -
    (pronounced *num-pie*) Powerful numerical arrays. A foundational
    package  
   for the two packages below.
-   [scipy](http://sourceforge.net/projects/scipy/files/) - (*sigh-pie*)
    Scientific, mathematical, and engineering package
-   [scikit-learn](http://scikit-learn.org/stable/install.html) - Easy
    to use machine learning library

Note: 64 bit versions of these libraries can be
found [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

Click through the links above for the home pages of each project and get
the installation for your operating system or, if you're running Linux,
you can install from a package manager (pip). If you're on a Windows
machine, it's easiest to install using the setup executables for scipy
and scikit-learn rather than installing from a package manager.
                                   
I'd also highly recommend to setting up a decent Python development
environment. You can certainly execute Python scripts from the command
line, but it's a heck of a lot easier to use a proper environment with
debugging support. I use [PyDev](http://pydev.org/), but even something
like IPython is better than nothing.

Now you're ready for machine learning greatness!

## 2. Your First Submission

The [Biological
Response](https://www.kaggle.com/c/bioresponse) competition provides a
great data set to get started with because the value to be predicted is
a simple binary classifier (0 or 1) and the data is just a bunch of
numbers, so
feature [extraction](http://en.wikipedia.org/wiki/Feature_extraction) and [selection](http://en.wikipedia.org/wiki/Feature_selection) aren't
as important as in some other Kaggle
competitions. [Download](https://www.kaggle.com/c/bioresponse/data) the
training and test data sets now. Even though this competition is over,
you can still make submissions and see how you compare to the world's
best data scientists.

In the code below, we'll use an ensemble classifier called a [random
forest](http://en.wikipedia.org/wiki/Random_forest) that often performs
very well as-is, without much babysitting and parameter-tweaking.
Although a random forest is actually a pretty sophisticated classifier,
it's a piece of cake to get up and running with one thanks to sklearn.

*Remember: You don't have to understand all of the underlying
mathematics to use these techniques. Experimentation is a great way to
start getting a feel for how this stuff works. Understanding the models
is important, but it's not necessary to get started, have fun, and
compete.*

Here's the code:

    :::python
    from sklearn.ensemble import RandomForestClassifier
    from numpy import genfromtxt, savetxt
    
    def main():
        #create the training & test sets, skipping the header row with [1:]
        dataset = genfromtxt(open('Data/train.csv','r'), delimiter=',', dtype='f8')[1:]    
        target = [x[0] for x in dataset]
        train = [x[1:] for x in dataset]
        test = genfromtxt(open('Data/test.csv','r'), delimiter=',', dtype='f8')[1:]
    
        #create and train the random forest
        #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
        rf = RandomForestClassifier(n_estimators=100)
        rf.fit(train, target)
        predicted_probs = [x[1] for x in rf.predict_proba(test)]
    
        savetxt('Data/submission.csv', predicted_probs, delimiter=',', fmt='%f')
    
    if __name__=="__main__":
        main()

At this point you should go ahead and *actually get this running* by
plopping the into a new Python script and saving it as
makeSubmission.py. You should now have directories and files on your
computer like this:

    "My Kaggle Folder")
     |
     |---"Data"
     |   |
     |   |---train.csv
     |   |
     |   |---test.csv
     |
     |---makeSubmission.py

Once you've run makeSubmission, you'll also have
``my_first_submission.csv`` in your data folder. Now it is time to do
something very important:

### Submit this file to the bio-response competition

Did you do it? You did it! Great! You could stop here - you know how to
make a successful Kaggle entry - but if you're the curious type, I'm
sure you'll want to play around with other types of models, different
parameters, and other shiny things. Keep reading to learn an important
technique that will let you test models locally, without burning through
your daily Kaggle submission limit.

## 3. Evaluation and Cross-Validation

Let's say we wanted to try out sklearn's [gradient boosting
machine](http://scikit-learn.org/stable/modules/ensemble.html#gradient-tree-boosting) instead
of a random forest. Or maybe some simple [linear
models](http://scikit-learn.org/stable/modules/linear_model.html). It's
easy enough to important these things from sklearn and generate
submission files, but it's not so easy to compare their performance.
It's not practical to upload a new submission every time we make a
change to the model - we'll need a way to test things out locally, and
we'll need two things in order to do that:

1.  An evaluation function
2.  Cross validation

You'll always need some kind of evaluation function to determine how
your models are performing. Ideally, these would be identical to the
evaluation metric that Kaggle is using to score your entry. Competition
participants often post evaluation code in the forums, and Kaggle has
detailed descriptions of the metrics available on
the [wiki](https://www.kaggle.com/wiki/Metrics). In the case of the
bio-response competition, the evaluation metric
is [log-loss](https://www.kaggle.com/wiki/LogarithmicLoss) and user
Grunthus
has [posted](https://www.kaggle.com/c/bioresponse/forums/t/1831/python-code-for-log-loss) a
Python version of it. We won't spend too much time on this (read the
forum post for more information), but go ahead and save the following
into your working directory as logloss.py.

    :::python
    import scipy as sp
    def llfun(act, pred):
        epsilon = 1e-15
        pred = sp.maximum(epsilon, pred)
        pred = sp.minimum(1-epsilon, pred)
        ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
        ll = ll * -1.0/len(act)
        return ll

Finally, we'll need data to test our models against. When you submitted
your first Kaggle competition entry earlier in this tutorial, Kaggle
compared (using log-loss) your answers to the actual real world results
(the "ground truth") associated with the test data set. Without access
to those answers, how can we actually test our models locally?
Cross-validation to the rescue!

Cross-validation is a simple technique that basically grabs a chunk of
the training data and holds it in reserve while the model is trained on
the remainder of the data set. In case you haven't realized it yet,
sklearn it totally awesome and is here to help. It has built in tools to
generate cross validation sets. The
sklearn [documentation](http://scikit-learn.org/0.10/modules/cross_validation.html) has
a lot of great information on cross-validation.

The code below creates 10 cross-validation sets (called *folds*), each
with 10% of the training data set held in reserve, and tests our random
forest model against that withheld data.

    :::python
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import cross_validation
    import logloss
    import numpy as np
    
    def main():
        #read in  data, parse into training and target sets
        dataset = np.genfromtxt(open('Data/train.csv','r'), delimiter=',', dtype='f8')[1:]    
        target = np.array([x[0] for x in dataset])
        train = np.array([x[1:] for x in dataset])
    
        #In this case we'll use a random forest, but this could be any classifier
        cfr = RandomForestClassifier(n_estimators=100)
    
        #Simple K-Fold cross validation. 5 folds.
        cv = cross_validation.KFold(len(train), k=5, indices=False)
    
        #iterate through the training and test cross validation segments and
        #run the classifier on each one, aggregating the results into a list
        results = []
        for traincv, testcv in cv:
            probas = cfr.fit(train[traincv], target[traincv]).predict_proba(train[testcv])
            results.append( logloss.llfun(target[testcv], [x[1] for x in probas]) )
    
        #print out the mean of the cross-validated results
        print "Results: " + str( np.array(results).mean() )
    
    if __name__=="__main__":
        main()

Note that your cross-validated results might not exactly match the score
Kaggle gives you on the model. This could be for a variety of
(legitimate) reasons: random forests have a random component and won't
yield identical results every time; the actual test set might deviate
from the training set (especially when the sample size is fairly low,
like in the bio-response competition); the evaluation implementation
might differ slightly. Even if you are getting slightly different
results, you can compare model performance locally and you should know
when you have made an improvement.

## That's a wrap!

That's it! We're done! You now have great tools at your disposal, and I
expect to see you at the top of the leaderboard in no time!
