Title: Actually Understanding Timezones in PostgreSQL
Date: 2016-08-12 12:09
Author: Chris Clark
Slug: actually-understanding-timezones-in-postgresql
Category: Code & Tutorials

Everyone hates confusing timezone stuff, and everyone has had to deal
with it at some point. It's the worst. And it's also incredibly
boring, so doesn't lend itself to digging in and figuring out what the
hell is going on. But sometimes you don't have a choice, like me,
yesterday, when my slightly-imprecise understanding of how PostgreSQL
handles timestamps and timezones ended with a nervous breakdown at my
desk, and the marketing department looking very concerned. The results
I kept getting seemed *impossible*! Down was up, up was down, Pacific
Time suddenly had no meaning, and I imagined that the official GMT
clock was spinning around like something from Alice in Wonderland,
laughing at me.

But it turns out all is actually right with the world, and everything
makes sense, and I totally know what's going on. Follow along (you
just need the ability to run SQL on PostgreSQL) and join me in the
basking glow of timezone comprehension.

If you make it all the way through, I promise you'll know enough to
puzzle out any Postgres timezone question you have. It's detail, but
it's important detail.
    
## Easy Sample Data

Let's make a test table. Easy.

    :::sql
    CREATE TABLE test
    (
        ts_naked timestamp without time zone,
        ts_tz timestamp with time zone
    );

An pretend that you, like me, live in California and our local time
zone on our computer is 'America/Los_Angeles'.

And we'll also pretend we have a PostgreSQL server running in
California, but it's set to UTC time, via the timezone parameter into
postgresql.conf being set like ``timezone = 'US/Central'``. So that's
our setup.

## Insertin' Stuff

Let the fun begin! Let's first insert some data:

    :::sql
    INSERT INTO
        test (ts_naked, ts_tz)
    VALUES
        (TIMESTAMP '2016-08-12 10:22:31.949271-07',
        TIMESTAMP WITH TIME ZONE '2016-08-12 10:22:31.949271-07',);

Note that *both* of the inserted values have a -07 at the end,
indicating a -7 hour offset from UTC, which, given that I'm writing
this in California (normally a -08 offset), in August, means that
daylight savings time is in effect, thus changing my local UTC offset
by an hour, to UTC-07. Phew. Ok. We're doing great.

But wait a minute! I just inserted an offset time zone into BOTH my
'naked' timestamp field (that doesn't know about timezones) and the
tz-aware field. So what happens when I get the data back out?

    :::psql
    #=> SELECT * FROM test;
              ts_naked          |             ts_tz
    ----------------------------+-------------------------------
     2016-08-12 10:22:31.949271 | 2016-08-12 17:22:31.949271+00


Hm, ok. So basically the naked timezone just took the inserted
timestamp at face value and wrote it on in. It completely ignored the
-07 at the end. And yep, that makes sense. The
[PostgreSQL docs](https://www.postgresql.org/docs/9.1/static/datatype-datetime.html#AEN5788)
confirm it:

> PostgreSQL never examines the content of a literal string before
> determining its type, and therefore will treat both of the above as
> timestamp without time zone. To ensure that a literal is treated as
> timestamp with time zone, give it the correct explicit type:

It's not enough to provide the -07 at the end, you need to actually
say TIMESTAMP WITH TIME ZONE. But also note that postgres *did not
save* the timezone information for the tz-aware field; this is a
really important distinction. Postgres TIMESTAMP WITH TIME ZONE fields
*do not actually store any TZ info*, they just expect TZ info to be
*present* when the fields are written to. Under the covers, Postgres
converts it to whatever time is set in the postgresql.conf file (UTC
in our case) and internally says "yep, great, I am confident that I am
storing this timestamp, normalized to a known time zone". With that
confidence, Postgres can now perform any timezone conversion you'd
like. But there's no way to ever retrieve the fact that I originally
sent down a timestamp with a UTC-07 offset; that information is gone
forever.

## Readin' Stuff

Right, so we have data, let's get it back out and see what happens.

First, let's deal with our stupid ts_naked field. It's pretty easy
to understand. When we wrote to it, it interpreted the timestamp as
literal, and basically just burned it straight into the database. So,
no surprise, bad shit happens when you try to use it with timezones:

    :::psql
    #=> select ts_naked AT TIME ZONE 'America/Los_Angeles' from test;
               timezone
    -------------------------------
     2016-08-12 17:22:31.949271+00
    
    #=> select ts_naked AT TIME ZONE 'UTC' from test;
               timezone
    -------------------------------
     2016-08-12 10:22:31.949271+00

Yeah...that's pretty wacky. Postgres has no idea wtf time you actually
stored, so it just treats it as whatever you configured in
postgresql.conf, applies the offsets you requested, and kinda throws
up its hands and gives up by returning a timestamp without an offset
(as indicated by the +00). So that's not very useful. Don't use
timestamps without time zones in PostgreSQL. There, easy.

Now let's focus on the interesting one. It behaves like you'd
hope...for now.

    :::psql
    #=> select ts_tz AT TIME ZONE 'UTC' from test;
              timezone
    ----------------------------
     2016-08-12 17:22:31.949271
    
    
    #=> select ts_tz AT TIME ZONE 'America/Los_Angeles' from test;
              timezone
    ----------------------------
     2016-08-12 10:22:31.949271

Great. We can select our data, and request it in any time zone we
want, and nothing weird happens. Although...there is one
surprise. Note that we actually did not get any timezone information
back from these queries; there's not offset at the end of the
timestamps. Postgres returned a TIMESTAMP WITHOUT TIME ZONE!

By requesting the data in a particular timezone, Postgres says "you
know the offset, since you just asked for it, so I don't need to give
it you". There's no offset specified at the end of the timestamp. I
don't particularly like this; we're returning ambiguous information
over the wire that we might want later on. Let's try something else.

Recall that a plain-old query will in fact give us a TZ-aware
timestamp, in the server time:

    :::psql
    #=> select ts_tz from test;
                 ts_tz
    -------------------------------
     2016-08-12 17:22:31.949271+00
    
But check this out!

    :::psql
    #=> SET timezone='America/Los_Angeles';
    #=> select ts_tz from test;
                 ts_tz
    -------------------------------
     2016-08-12 10:22:31.949271-07
     
Whaaaaaa??! It turns out that *every Postgres session has its own time
zone*. Whoa.

And this is where it's very easy to get surprised. For instance, when
Django connects to Postgres, it
'[ensures timezone](https://github.com/django/django/blob/master/django/db/backends/postgresql/base.py#L195)'
and slaps the application time zone onto the psycopg2 connection so
you get back timestamps in the same timezone you put them in (assuming
you are inserting local times).
 
That's clever, but can lead to incredibly confusion if you are trying
to compare results from the same database, but via 2 different
connections, which are set to two different time zones. You can always
check the current session TZ via ``SELECT
current_setting('TIMEZONE');``
 
Isn't this fun??
 
## Offsettin' Stuff
 
For extra confusion, Postgres will happily let you do this:
 
    :::psql
    #=> select ts_tz AT TIME ZONE 'PST' from test;
             timezone
    ----------------------------
     2016-08-12 09:22:31.949271
     
Which may not *look* confusing, but I promise it is because 'PST' is
not actually a timezone! And I can prove it. Postgres keeps a list of
all the timezones it knows in a view called ``pg_timezone_names``:
 
    :::psql
    #=> select count(*) from pg_timezone_names;
    count
    -------
     1204
  
Holy smokes that's a lot of timezones! Over 1200 of these:
  
    :::psql
    #=> select * from pg_timezone_names order by random() limit 10;
             name         | abbrev | utc_offset | is_dst
    ----------------------+--------+------------+--------
     Kwajalein            | MHT    | 12:00:00   | f
     posix/W-SU           | MSK    | 03:00:00   | f
     posix/Europe/Vaduz   | CEST   | 02:00:00   | t
     posix/Pacific/Niue   | NUT    | -11:00:00  | f
     Asia/Ashkhabad       | TMT    | 05:00:00   | f
     posix/Australia/LHI  | LHST   | 10:30:00   | f
     posix/Pacific/Tarawa | GILT   | 12:00:00   | f
     posix/America/Adak   | HDT    | -09:00:00  | t
     America/Vancouver    | PDT    | -07:00:00  | t
     Asia/Hovd            | HOVST  | 08:00:00   | t
 
 And not a PST among them:
 
    :::psql
    #=> select * from pg_timezone_names where name='PST';
    name | abbrev | utc_offset | is_dst
    ------+--------+------------+--------
    (0 rows)
    
But it is this other thing, called an 'abbreviation':

    :::psql
    #=> select * from pg_timezone_names where abbrev='PST';
              name          | abbrev | utc_offset | is_dst
    ------------------------+--------+------------+--------
     Pacific/Pitcairn       | PST    | -08:00:00  | f
     posix/Pacific/Pitcairn | PST    | -08:00:00  | f
     posix/SystemV/PST8     | PST    | -08:00:00  | f
     SystemV/PST8           | PST    | -08:00:00  | f
     
So all of those time zones are the same, and can be abbreviated
'PST'. Note that our friend America/Los_Angeles does not appear here
because it takes daylight savings time into account, whereas PST does
not and is a true UTC-08 offset.

## Recap

That's pretty much it! To recap:

1. Use only TIMESTAMP WITH TIME ZONE fields.
2. Remember that Postgres doesn't store time zones; it just normalizes tz-aware timestamps to the server time.
2. Be aware of your server time zone.
3. Be aware of your session time zone (which may be set somewhere deep in your application code). For your own sanity, rely on your session's time zone when possible, rather than using AT TIME ZONE operators in your queries.
4. Be aware that offsets and time zones are not the same.

## A Final Mystery

I've internalized all of this, and really do feel like I understand
it. Except for one lingering mystery. Check this out:

    :::psql
    #=> select * from pg_timezone_names where utc_offset='-08:00:00' and is_dst=false;
              name          | abbrev | utc_offset | is_dst
    ------------------------+--------+------------+--------
     Etc/GMT+8              | GMT+8  | -08:00:00  | f
     Pacific/Pitcairn       | PST    | -08:00:00  | f
     posix/Etc/GMT+8        | GMT+8  | -08:00:00  | f
     posix/Pacific/Pitcairn | PST    | -08:00:00  | f
     posix/SystemV/PST8     | PST    | -08:00:00  | f
     SystemV/PST8           | PST    | -08:00:00  | f
    
Look at those two extra timezones! Look at their names and
abbreviations! They are UTC-08 offsets, but *named* GMT+8?? GMT and
UTC *are the same thing*! Google could literally not be more
categorical about this fact:

![google-says-so]({filename}/images/gmt_and_utc.png)

But apparently Postgres thinks they are opposites. Or something. If
anyone can explain this in the comments, I'd really appreciate
it. Thanks!
