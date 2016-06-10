Title: Engineering Practices in Data Science
Date: 2012-10-04 17:28
Author: Chris Clark
Slug: engineering-practices-in-data-science
Category: Data Science

[Josh
Wills](http://twitter.com/jasonbaldridge/statuses/198115689175859201)
wrote this excellent, pithy definition of a data scientist:  

> Data Scientists (n.): Person who is better at statistics than any
> software engineer and better at software engineering than any
> statistician.

It's certainly true that software engineering and data science are two
different disciplines, and for good reason - they require different
skills. But as this definition points out, in the same way an artist and
an interior painter might share the medium of paint and thus a set of
best practices (invest in canvas drop cloths, write down color choices),
so do data scientists and software engineers share the medium of code.
  
Among the [Kaggle](http://www.kaggle.com/) community there seem to be a
few consistent ways that engineering practices intersect with data
science. These trends are thrown into particularly sharp relief by the
competition format we use at Kaggle, but are present to varying extents
in data science teams across industry.
  
To start, it terrifies me that....

### ...many data scientists don't use source control.

To those who breathe Git and dream in command line interfaces, it might
be hard to believe that many data scientists (smart ones! great ones!)
just plain don't use version control. If you ask them they might say
something like "Sure I use version control! I email myself every new
version of the R script. Plus it's on dropbox."  
  
I can't back it up with hard data, but it seems data scientists who use
R, Matlab, SAS, or other statistical programming languages use source
control less frequently than people who use Python or Java. And this
sort of makes sense - the stats community is often more academically
oriented and not as steeped in engineering practices as the Python
community, for instance.
  
And frankly - who can blame data scientists for not using source
control? The de facto choice, Git, might be free but is totally obtuse
(though R isn't exactly a haven of good design...) and most of the time
saving files to disk with clever names seems to work OK. For data
scientists, source control on its own just isn't valuable enough to
bother with. Contrast this with software engineering: source control
isn't just source control but the jumping off point for continuous
integration builds, deployments, and code reviews. For data scientists
to use source control (and they should - it makes collaboration easier,
and mistakes less likely), it has to be more valuable. And I'm
optimistic that we will get there as...

### ....successful data scientists learn the value of good pipeline engineering.

A well-engineered pipeline gets data scientists iterating much faster,
which can be a big competitive edge in a Kaggle competition. This is
especially true for datasets that require a lot of feature engineering -
a crisp pipeline with well defined phases (data ingestion -&gt; feature
extraction -&gt; training -&gt; ensembling -&gt; validation) allows
disciplined data scientists to try out a lot more ideas than someone
with a pile of spaghetti Python code.
  
I expect we'll soon start to see more open source data science pipelines
that couple nicely with popular machine learning libraries and tools.
The more tooling and community support we have for good pipelines, the
less we'll see...
  
### ...good engineering going out the window quickly with elaborate ensembling.
  
This effect is probably more specific to Kaggle than the others but it's
fun and instructive, so I'll write about it anyway.
  
In the final hours of a competition we sometimes see unholy ensembles of
different languages and techniques being mashed together for a final
push. It's something we try to discourage by encouraging team formation
early on (so a nice pipeline gets built), but it does occasionally
happen. In one particularly gruesome case we saw some Java code spawning
processes which ran command line shells in order to launch the R
executable while the Java program piped data and commands back and forth
between the shells. Yikes!
  
### In Closing...
  
Data scientists are slowly but surely adopting engineering practices
that enable them to get the goo of software out of the way so they can
focus on valuable data problems. I hope that we'll soon start to see
well engineered data pipelines emerge as open source projects that
generalize well over particular classes of problems, complement existing
data science libraries, and encourage modular development and use of
source control.
  
Or someone writes a killer general-purpose deep learning library and we
all just use that.
