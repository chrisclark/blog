Title: Getting Started with Pandas - Predicting SAT Scores for New York City Schools
Date: 2013-01-23 01:20
Author: Chris Clark
Slug: getting-started-with-pandas-predicting
Category: Code & Tutorials

##An Introduction to Pandas

This tutorial will get you started with Pandas - a data analysis library for Python that is great for data preparation, joining, and ultimately generating well-formed, tabular data that's easy to use in a variety of visualization tools or (as we will see here) machine learning applications. This tutorial assumes a solid understanding of core Python functionality, but nothing about machine learning or Pandas.

###Goals

1. Using data from [NYC Open Data] (https://data.cityofnewyork.us/), build a unified, tabular dataset ready for use with machine learning algorithms to predict student SAT scores on a per school basis.
2. Learn and use the Pandas data analysis package.
3. Learn how data is typically prepared for machine learning algorithms (ingestion, cleaning, joining, feature generation).

First, let's ingest the data and get the lay of the land. You can download the data sets referenced below from [NYC Open Data](https://nycopendata.socrata.com/), or directly download a [zip file](http://www.untrod.com/NYC_Schools.zip) with the relevant data.

    :::python
    import pandas as pd
    import numpy as np
    
    # Load the data
    dsProgReports = pd.read_csv('C:/data/NYC_Schools/School_Progress_Reports_-_All_Schools_-_2009-10.csv')
    dsDistrict = pd.read_csv('C:/data/NYC_Schools/School_District_Breakdowns.csv')
    dsClassSize = pd.read_csv('C:/data/NYC_Schools/2009-10_Class_Size_-_School-level_Detail.csv')
    dsAttendEnroll = pd.read_csv('C:/data/NYC_Schools/School_Attendance_and_Enrollment_Statistics_by_District__2010-11_.csv')[:-2] #last two rows are bad
    dsSATs = pd.read_csv('C:/data/NYC_Schools/SAT__College_Board__2010_School_Level_Results.csv') # Dependent

    dsSATs

Output:

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 460 entries, 0 to 459
    Data columns:
    DBN                      460  non-null values
    School Name              460  non-null values
    Number of Test Takers    460  non-null values
    Critical Reading Mean    460  non-null values
    Mathematics Mean         460  non-null values
    Writing Mean             460  non-null values
    dtypes: object(6)

##Outline

Pandas has read the data files without issue. Next let's create a rough map of where we are going.

We have five datasets here, each with information about either schools or districts. We're going to need to join all of this information together into a tabular file, with one row for each school, joined with as much information we can gather about that school & its district, including our dependent variables, which will be the mean SAT scores for each school in 2010.

Drilling down one level of detail, let's look at the dataset dsSATs, which contains the target variables:

    :::python
    dsSATs

Output:

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 460 entries, 0 to 459
    Data columns:
    DBN                      460  non-null values
    School Name              460  non-null values
    Number of Test Takers    460  non-null values
    Critical Reading Mean    460  non-null values
    Mathematics Mean         460  non-null values
    Writing Mean             460  non-null values
    dtypes: object(6)

##Target Variable and Joining Strategy

We are going to build a dataset to predict Critical Reading Mean, Mathematics Mean, and Writing Mean for each school (identified by DBN).

After digging around in Excel (or just taking my word for it) we identify the following join strategy (using SQL-esque pseudocode):

    :::python
    dsSATS join dsClassSize on dsSATs['DBN'] = dsClassSize['SCHOOL CODE']
    join dsProgReports on dsSATs['DBN'] = dsProgReports['DBN']
    join dsDistrct on dsProgReports['DISTRICT'] = dsDistrict['JURISDICTION NAME']
    join dsAttendEnroll on dsProgReports['DISTRICT'] = dsAttendEnroll['District']

Now that we have the strategy identified at a high level, there are a number of details we have to identify and take care of first.

##Primary Keys - Schools

Before we can join these three datasets together, we need to normalize their primary keys. Below we see the mismatch between the way the DBN (school id) field is represented in the different datasets. We then write code to normalize the keys and correct this problem.

    :::python
    pd.DataFrame(data=[dsProgReports['DBN'].take(range(5)), dsSATs['DBN'].take(range(5)), dsClassSize['SCHOOL CODE'].take(range(5))])

Output:

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>DBN</strong></td>
      <td> 01M015</td>
      <td> 01M019</td>
      <td> 01M020</td>
      <td> 01M034</td>
      <td> 01M063</td>
    </tr>
    <tr>
      <td><strong>DBN</strong></td>
      <td> 01M292</td>
      <td> 01M448</td>
      <td> 01M450</td>
      <td> 01M458</td>
      <td> 01M509</td>
    </tr>
    <tr>
      <td><strong>SCHOOL CODE</strong></td>
      <td>   M015</td>
      <td>   M015</td>
      <td>   M015</td>
      <td>   M015</td>
      <td>   M015</td>
    </tr>
  </tbody>
</table>
</div>

    :::python
    #Strip the first two characters off the DBNs so we can join to School Code
    dsProgReports.DBN = dsProgReports.DBN.map(lambda x: x[2:])
    dsSATs.DBN = dsSATs.DBN.map(lambda x: x[2:])
    
    #We can now see the keys match
    pd.DataFrame(data=[dsProgReports['DBN'].take(range(5)), dsSATs['DBN'].take(range(5)), dsClassSize['SCHOOL CODE'].take(range(5))])

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>DBN</strong></td>
      <td> M015</td>
      <td> M019</td>
      <td> M020</td>
      <td> M034</td>
      <td> M063</td>
    </tr>
    <tr>
      <td><strong>DBN</strong></td>
      <td> M292</td>
      <td> M448</td>
      <td> M450</td>
      <td> M458</td>
      <td> M509</td>
    </tr>
    <tr>
      <td><strong>SCHOOL CODE</strong></td>
      <td> M015</td>
      <td> M015</td>
      <td> M015</td>
      <td> M015</td>
      <td> M015</td>
    </tr>
  </tbody>
</table>
</div>



##Primary Keys - Districts

We have a similar story with the district foreign keys. Again, we need to normalize the keys. The only additional complexity here is that dsProgReports['DISTRICT'] is typed numerically, whereas the other two district keys are typed as string. We do some type conversions following the key munging.

    :::python
    #Show the key mismatchs
    #For variety's sake, using slicing ([:3]) syntax instead of .take()
    pd.DataFrame(data=[dsProgReports['DISTRICT'][:3], dsDistrict['JURISDICTION NAME'][:3], dsAttendEnroll['District'][:3]])

Output:

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>DISTRICT</strong></td>
      <td>                1</td>
      <td>                1</td>
      <td>                1</td>
    </tr>
    <tr>
      <td><strong>JURISDICTION NAME</strong></td>
      <td> CSD 01 Manhattan</td>
      <td> CSD 02 Manhattan</td>
      <td> CSD 03 Manhattan</td>
    </tr>
    <tr>
      <td><strong>District</strong></td>
      <td>      DISTRICT 01</td>
      <td>      DISTRICT 02</td>
      <td>      DISTRICT 03</td>
    </tr>
  </tbody>
</table>
</div>

    :::python
    #Extract well-formed district key values
    #Note the astype(int) at the end of these lines to coerce the column to a numeric type
    import re
    dsDistrict['JURISDICTION NAME'] = dsDistrict['JURISDICTION NAME'].map(lambda x: re.match( r'([A-Za-z]*\s)([0-9]*)', x).group(2)).astype(int)
    dsAttendEnroll.District = dsAttendEnroll.District.map(lambda x: x[-2:]).astype(int)
    
    #We can now see the keys match
    pd.DataFrame(data=[dsProgReports['DISTRICT'][:3], dsDistrict['JURISDICTION NAME'][:3], dsAttendEnroll['District'][:3]])

Output:

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>DISTRICT</strong></td>
      <td> 1</td>
      <td> 1</td>
      <td> 1</td>
    </tr>
    <tr>
      <td><strong>JURISDICTION NAME</strong></td>
      <td> 1</td>
      <td> 2</td>
      <td> 3</td>
    </tr>
    <tr>
      <td><strong>District</strong></td>
      <td> 1</td>
      <td> 2</td>
      <td> 3</td>
    </tr>
  </tbody>
</table>
</div>



##Additional Cleanup

At this point we could do the joins, but there is messiness in the data still. First let's reindex the DataFrames so the semantics come out a bit cleaner. Pandas indexing is beyond the scope of this tutorial but suffice it to say it makes these operations easier.

    :::python
    #Reindexing
    dsProgReports = dsProgReports.set_index('DBN')
    dsDistrict = dsDistrict.set_index('JURISDICTION NAME')
    dsClassSize = dsClassSize.set_index('SCHOOL CODE')
    dsAttendEnroll = dsAttendEnroll.set_index('District')
    dsSATs = dsSATs.set_index('DBN')

Let's take a look at one of our target variables. Right away we see the "s" value, which shouldn't be there.

We'll filter out the rows without data.

    :::python
    #We can see the bad value
    dsSATs['Critical Reading Mean'].take(range(5))

Output:

    DBN
    M292    391
    M448    394
    M450    418
    M458    385
    M509      s
    Name: Critical Reading Mean

Now we filter it out
    
    :::python
    #We create a boolean vector mask. Open question as to whether this semantically ideal...
    mask = dsSATs['Number of Test Takers'].map(lambda x: x != 's')
    dsSATs = dsSATs[mask]
    #Cast fields to integers. Ideally we should not need to be this explicit.
    dsSATs['Number of Test Takers'] = dsSATs['Number of Test Takers'].astype(int)
    dsSATs['Critical Reading Mean'] = dsSATs['Critical Reading Mean'].astype(int)
    dsSATs['Mathematics Mean'] = dsSATs['Mathematics Mean'].astype(int)
    dsSATs['Writing Mean'] = dsSATs['Writing Mean'].astype(int)
    
    #We can see those values are gone
    dsSATs['Critical Reading Mean'].take(range(5))

Output:

    DBN
    M292    391
    M448    394
    M450    418
    M458    385
    M515    314
    Name: Critical Reading Mean

##Feature Construction

dsClassSize will be a many-to-one join with dsSATs because dsClassSize contains multiple entries per school. We need to summarize and build features from this data in order to get one row per school that will join neatly to dsSATs.

Additionally, the data has an irregular format, consisting of a number of rows per school describing different class sizes, then a final row for that school which contains no data except for a number in the final column, SCHOOLWIDE PUPIL-TEACHER RATIO.

We need to extract the SCHOOLWIDE PUPIL-TEACHER RATIO rows, at which point we'll have a regular format and can build features via aggregate functions. We'll also drop any features that can't be easily summarized or aggregated and likely have no bearing on the SAT scores (like School Name).

    :::python
    #The shape of the data
    print dsClassSize.columns
    print dsClassSize.take([0,1,10]).values

Output:

    :::python
    array([BORO, CSD, SCHOOL NAME, GRADE , PROGRAM TYPE,
           CORE SUBJECT (MS CORE and 9-12 ONLY),
           CORE COURSE (MS CORE and 9-12 ONLY), SERVICE CATEGORY(K-9* ONLY),
           NUMBER OF CLASSES, TOTAL REGISTER, AVERAGE CLASS SIZE,
           SIZE OF SMALLEST CLASS, SIZE OF LARGEST CLASS, DATA SOURCE,
           SCHOOLWIDE PUPIL-TEACHER RATIO], dtype=object)
    [[M 1 P.S. 015 ROBERTO CLEMENTE 0K GEN ED - - - 1.0 21.0 21.0 21.0 21.0 ATS
      nan]
     [M 1 P.S. 015 ROBERTO CLEMENTE 0K CTT - - - 1.0 21.0 21.0 21.0 21.0 ATS
      nan]
     [M 1 P.S. 015 ROBERTO CLEMENTE nan nan nan nan nan nan nan nan nan nan nan
      8.9]]

Extracting the Pupil-Teacher Ratio
    
    :::python
    #Take the column
    dsPupilTeacher = dsClassSize.filter(['SCHOOLWIDE PUPIL-TEACHER RATIO'])
    #And filter out blank rows
    mask = dsPupilTeacher['SCHOOLWIDE PUPIL-TEACHER RATIO'].map(lambda x: x > 0)
    dsPupilTeacher = dsPupilTeacher[mask]
    #Then drop from the original dataset
    dsClassSize = dsClassSize.drop('SCHOOLWIDE PUPIL-TEACHER RATIO', axis=1)
    
    #Drop non-numeric fields
    dsClassSize = dsClassSize.drop(['BORO','CSD','SCHOOL NAME','GRADE ','PROGRAM TYPE',\
    'CORE SUBJECT (MS CORE and 9-12 ONLY)','CORE COURSE (MS CORE and 9-12 ONLY)',\
    'SERVICE CATEGORY(K-9* ONLY)','DATA SOURCE'], axis=1)
    
    #Build features from dsClassSize
    #In this case, we'll take the max, min, and mean
    #Semantically equivalent to select min(*), max(*), mean(*) from dsClassSize group by SCHOOL NAME
    #Note that SCHOOL NAME is not referenced explicitly below because it is the index of the dataframe
    grouped = dsClassSize.groupby(level=0)
    dsClassSize = grouped.aggregate(np.max).\
        join(grouped.aggregate(np.min), lsuffix=".max").\
        join(grouped.aggregate(np.mean), lsuffix=".min", rsuffix=".mean").\
        join(dsPupilTeacher)
    
    print dsClassSize.columns

Output:

    array([NUMBER OF CLASSES.max, TOTAL REGISTER.max, AVERAGE CLASS SIZE.max,
           SIZE OF SMALLEST CLASS.max, SIZE OF LARGEST CLASS.max,
           NUMBER OF CLASSES.min, TOTAL REGISTER.min, AVERAGE CLASS SIZE.min,
           SIZE OF SMALLEST CLASS.min, SIZE OF LARGEST CLASS.min,
           NUMBER OF CLASSES.mean, TOTAL REGISTER.mean,
           AVERAGE CLASS SIZE.mean, SIZE OF SMALLEST CLASS.mean,
           SIZE OF LARGEST CLASS.mean, SCHOOLWIDE PUPIL-TEACHER RATIO], dtype=object)

##Joining

One final thing before we join - dsProgReports contains distinct rows for separate grade level blocks within one school. For instance one school (one DBN) might have two rows: one for middle school and one for high school. We'll just drop everything that isn't high school.

And finally we can join our data. Note these are inner joins, so district data get joined to each school in that district.

    :::python
    mask = dsProgReports['SCHOOL LEVEL*'].map(lambda x: x == 'High School')
    dsProgReports = dsProgReports[mask]

    final = dsSATs.join(dsClassSize).\
    join(dsProgReports).\
    merge(dsDistrict, left_on='DISTRICT', right_index=True).\
    merge(dsAttendEnroll, left_on='DISTRICT', right_index=True)

##Additional Cleanup 2

We should be in a position to build a predictive model for our target variables right away but unfortunately there is still messy data floating around in the dataframe that machine learning algorithms will choke on. A pure feature matrix should have only numeric features, but we can see that isn't the case. However for many of these columns, the right approach is obvious once we've dug in.

    :::python
    final.dtypes[final.dtypes.map(lambda x: x=='object')]

Output:

    School Name                      object
    SCHOOL                           object
    PRINCIPAL                        object
    PROGRESS REPORT TYPE             object
    SCHOOL LEVEL*                    object
    2009-2010 OVERALL GRADE          object
    2009-2010 ENVIRONMENT GRADE      object
    2009-2010 PERFORMANCE GRADE      object
    2009-2010 PROGRESS GRADE         object
    2008-09 PROGRESS REPORT GRADE    object
    YTD % Attendance (Avg)           object

Next:

    :::python
    #Just drop string columns.
    #In theory we could build features out of some of these, but it is impractical here
    final = final.drop(['School Name','SCHOOL','PRINCIPAL','SCHOOL LEVEL*','PROGRESS REPORT TYPE'],axis=1)
    
    #Remove % signs and convert to float
    final['YTD % Attendance (Avg)'] = final['YTD % Attendance (Avg)'].map(lambda x: x.replace("%","")).astype(float)
    
    #The last few columns we still have to deal with
    final.dtypes[final.dtypes.map(lambda x: x=='object')]

Output:

    2009-2010 OVERALL GRADE          object
    2009-2010 ENVIRONMENT GRADE      object
    2009-2010 PERFORMANCE GRADE      object
    2009-2010 PROGRESS GRADE         object
    2008-09 PROGRESS REPORT GRADE    object


##Ordered Categorical Variables

We can see above that the remaining non-numeric field are grades . Intuitively, they might be important so we don't want to drop them, but in order to get a pure feature matrix we need numeric values. The approach we'll use here is to explode these into multiple boolean columns. Some machine learning libraries effectively do this for you under the covers, but when the cardinality of the categorical variable is relatively low, it's nice to be explicit about it.

    :::python
    gradeCols = ['2009-2010 OVERALL GRADE','2009-2010 ENVIRONMENT GRADE','2009-2010 PERFORMANCE GRADE','2009-2010 PROGRESS GRADE','2008-09 PROGRESS REPORT GRADE']
    
    grades = np.unique(final[gradeCols].values) #[nan, A, B, C, D, F]
    
    for c in gradeCols:
        for g in grades:
            final = final.join(pd.Series(data=final[c].map(lambda x: 1 if x is g else 0), name=c + "_is_" + str(g)))
    
    final = final.drop(gradeCols, axis=1)
    
    #Uncomment to generate csv files
    #final.drop(['Critical Reading Mean','Mathematics Mean','Writing Mean'],axis=1).to_csv('C:/data/NYC_Schools/train.csv')
    #final.filter(['Critical Reading Mean','Mathematics Mean','Writing Mean']).to_csv('C:/data/NYC_Schools/target.csv')

##Modeling

We now have a feature matrix and it's trivial to use it with any number of machine learning algorithms.

    :::python
    from sklearn.ensemble import RandomForestRegressor
    
    target = final.filter(['Critical Reading Mean'])
    #We drop all three dependent variables because we don't want them used when trying to make a prediction.
    train = final.drop(['Critical Reading Mean','Writing Mean','Mathematics Mean'],axis=1)
    model = RandomForestRegressor(n_estimators=100, n_jobs=-1, compute_importances = True)
    model.fit(train, target)
    
    predictions = np.array(model.predict(train))
    rmse = math.sqrt(np.mean((np.array(target.values) - predictions)**2))
    imp = sorted(zip(train.columns, model.feature_importances_), key=lambda tup: tup[1], reverse=True)
    
    print "RMSE: " + str(rmse)
    print "10 Most Important Variables:" + str(imp[:10])

Output:

    RMSE: 80.13105688
    10 Most Important Variables:[('PEER INDEX*', 0.81424747874371173), ('TOTAL REGISTER.min', 0.060086333792196724), ('2009-2010 ENVIRONMENT CATEGORY SCORE', 0.023810405565050669), ('2009-2010 ADDITIONAL CREDIT', 0.021788425210174274), ('2009-2010 OVERALL SCORE', 0.019046860376900468), ('AVERAGE CLASS SIZE.mean', 0.0094882658926829649), ('2009-2010 PROGRESS CATEGORY SCORE', 0.0094678349064146652), ('AVERAGE CLASS SIZE.min', 0.0063723026953534942), ('2009-2010 OVERALL GRADE_is_nan', 0.0057710237481254567), ('Number of Test Takers', 0.0053660239780210584)]
