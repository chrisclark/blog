Title: Entering Kaggle Competitions with Google Predict
Date: 2013-01-17 16:30
Author: Chris Clark
Slug: entering-kaggle-competitions-with
Category: Code & Tutorials

BigML had a [great series of
posts](http://blog.bigml.com/2013/01/04/machine-learning-throwdown-the-reckoning/)
over the summer pitting some prediction-as-a-service products against
each other. One of those was the [Google Predict
API](https://developers.google.com/prediction/). I thought it might be
fun to enter a Kaggle competition using the API and see how it did
against some of the world's top data scientists.  
  
It turns out this was a terrible, terrible waste of time.  
  
If you are expecting a rigorous analysis of the Google Predict API, this
post will be a disappointment. In fact, I'll go so far as to ruin the
surprise right now: on the Biological Response competition, the Predict
API turned in a 0.67245 on the private leaderboard, just edging out the
optimized constant value benchmark (in a nutshell - it did badly). It
fared a bit better on the Titanic competition, scoring a
somewhat-reasonable 0.79426 (tied with 55 other users for 112th place as
of this writing).  
  
So instead of focusing on the actual performance of the algorithm, I
will instead share some tips and tricks for using the Google Predict
API:  

### Chris' Tips for Using the Google Predict API:

-   Turn off two factor authentication, unless your idea of a good time
    is spending a furious evening at home, battling OAuth. It is a
    formidable enemy.
-   If you are predicting a binary response, be sure to replace those 0s
    and 1s in your response column with strings like TRUE and FALSE, or
    else Google will attempt to perform Magic (stand back!) and decide
    that your model is actually a regression model and will cheerfully
    return values like -0.8 and 1.2.
-   Nice work - now your response column is now filled with TRUE and
    FALSE strings and you have persuaded Google that you want a
    categorical response. You also remembered to remove that header row,
    right? Oh...you didn't? Well then get ready for the excitement of
    responses like this:

        :::javascript
        "outputMulti": [
           {
             "label": "TRUE",
             "score": 0.2001
           },
           {
             "label": "FALSE",
             "score": 0.7829
           },
           {
             "label": "HEADER_TEXT",
             "score": 0.017
           }
         ],

-   So yeah, remove those headers. And on a related note, have fun
    writing your own custom parsing code to extract the most likely
    label from this unsorted list. Because we certainly wouldn't want to
    pollute the integrity of the response schema with something as handy
    as providing the predicted label as a first class property.
-   The thing you are creating is a TrainedModel, *not* a HostedModel.
    Just trust me on this - they may have identical predict methods, and
    be used interchangeably in example code, but you are making
    TrainedModels and will get errors if you ever accidentally refer
    to HostedModels.
-   If you are using [Google's Python API
    wrappers](http://code.google.com/p/google-api-python-client/), be
    sure you are constructing your feature array like this:
    ``["foo","bar",1.23\]``
    and *not* like this:
    ``["foo","bar","1.23"\]``. I made the mistake of reading in my
    training CSV file as an array of strings, which caused my requests
    to look like the latter. The result?  The Predict API merrily
    chirps back with a valid, but completely terrible, prediction.
-   Get a cup of coffee. Google gets angry if you make too many
    prediction requests in a row and starts throwing errors. So you have
    to resort to weird throttling tricks if you need more than a few
    hundred predictions at once. And bulk prediction is not available.

My terrible, horrible code that does this [is on
github](https://github.com/chrisclark/GooglePredictForKaggle). It's not
a particularly usable form and does some...questionable things because I
didn't learn some of these lessons until it was too late. But if you are
absolutely determined to use the Google Predict API (god help you), it
might get you started.

Also, kudos to the BigML engineers who are either way smarter than me
and got this working right away, or have a remarkable amount of
self-restraint and did not complain one jot.
