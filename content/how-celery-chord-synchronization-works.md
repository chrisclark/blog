Title: How Celery Chord Synchronization Works
Date: 2015-03-26 10:20
Authors: Chris
Slug: how-celery-chord-synchronization-works
Category: Code & Tutorials

Celery is a powerful tool for managing asynchronous tasks in
Python. The basic model is synchronous Python code pushes a task
(in the form of a serialized message) into a message queue (the Celery
"broker", which can be a variety of technologies - Redis, RabbitMQ,
Memcached, or even a database), and worker processes pull tasks off
the queue and execute them. But Celery's
[16,000](http://celery.readthedocs.org/en/latest/faq.html#does-celery-really-consist-of-50-000-lines-of-code)
lines of application code certainly provide a lot more functionality
than a simple task queue. Celery exposes a number of powerful
synchronization (or "workflow" in Celery parlance)
[primitives](http://celery.readthedocs.org/en/latest/userguide/canvas.html) -
ways to execute groups of tasks together, chain async task results in
a synchronous manner, or execute a callback after a group of tasks
have finished executing.

At [Grove](https://www.grove.co), we make extensive use of this final
primitive, called a "chord" in Celery. Here's a trivial chord example,
from the Celery docs:

```
>>> from celery import chord
>>> from tasks import add, tsum

>>> chord(add.s(i, i)
...       for i in xrange(100))(tsum.s()).get()
9900
```

This queues up 100 'add' tasks, the results of which Celery aggregates
into a list, which is passed into the callback function (``tsum``)
when all of the tasks have finished executing.

We use chords for all sorts of tasks. For example, every night we
charge recurring shipments, and send out an internal email with the
results of how many charges succeeded, and how many failed due to
things like expired credit cards. The charge tasks are all
asynchronous, distributed across many workers, and the final email is
the chord's callback function.

Pretty cool! But wait...how exactly does this coordination work? The
Celery docs leave this somewhat cryptic comment:

> "The synchronization step is costly, so you should avoid using chords
as much as possible. "

Err...

Reading a bit further, we learn that:

By default the synchronization step is implemented by having a
recurring task poll the completion of the group every second, calling
the signature when ready.

That does sound a bit costly. But wait! There's more!

This is used by all result backends except Redis and Memcached, which
increment a counter after each task in the header, then applying the
callback when the counter exceeds the number of tasks in the set.
Ah-ha! The most common broker backends for Celery are Redis and
RabbitMQ, which will serve as exemplars for the two types of
synchronization as we dig in.

Redis is
[often described](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=redis%20swiss%20army%20knife)
as a "swiss army knife" for data. It functions great as a message
broker, but also as a general-purpose (non-relational) data
store. This means that Celery can store a count in Redis, of the
number of tasks originally in the chord, and increment that counter
every time a task completes. Here's the
[relevant code](https://github.com/celery/celery/blob/master/celery/backends/redis.py#L198)
from the Celery source:

    :::python
    _, readycount, totaldiff, _, _ = client.pipeline()               \
         .rpush(jkey, self.encode([1, tid, state, result]))          \
         .llen(jkey)                                                 \
         .get(tkey)                                                  \
         .expire(jkey, 86400)                                        \
         .expire(tkey, 86400)                                        \
         .execute()
    
         totaldiff = int(totaldiff or 0)
    
         try:
             callback = maybe_signature(request.chord, app=app)
             total = callback['chord_size'] + totaldiff
             if readycount == total:
                 decode, unpack = self.decode, self._unpack_chord_result
                    ...


This code (which is part of a larger function) executes every time one
of the chord's subtasks completes by
[binding](https://github.com/celery/celery/blob/master/celery/backends/redis.py#L100)
to the ``on_chord_part_return`` property. Through some clever Redis
pipelining, the count gets incremented, then retrieved into
``readycount``. Then, ``if readycount==total``, the chord callback
gets executed. Cool!

Is it expensive, as the docs claim? Well...sort of. It causes a slew
of Redis commands to fire after every subtasks completes, but it uses
connection pooling, and the pipeline redis primitive, so there is only
one round-trip to the broker. It depends on your use case whether you
consider this expensive or not. it seems like a small price to pay for
the synchronization.

Now that we understand Redis, let's see how RabbitMQ does it.

RabbitMQ is a message queue. It is not designed to persist arbitrary
data, but is purpose built as a broker. There isn't a place to store a
counter, so Celery relies on a polling strategy to determine if the
chord is ready to complete. The code for this is spread out across a
number of source files, but it all starts with
[apply_chord()](https://github.com/celery/celery/blob/b3d8ba2781189b7de0894f11295e815fa0bbd0b5/celery/backends/base.py#L358)
in the base broker class (which RabbitMQ, referred to as 'amqp' in
Celery,
[inherits from](https://github.com/celery/celery/blob/b3d8ba2781189b7de0894f11295e815fa0bbd0b5/celery/backends/amqp.py)).

When the chord starts, ``apply_chord`` calls
``callback_chord_unlock``, which in turn queues up the builtin
``celery.chord_unlock``
[task](https://github.com/celery/celery/blob/04e77c0bd14596d8ddc9214e7cca5e817f74c9d2/celery/app/builtins.py#L59). Here's
the crucial bit of code in chord_unlock that polls for the completion
of the subtasks:

    :::python
    try:
        ready = deps.ready()
    except Exception as exc:
        raise self.retry(
                   exc=exc, countdown=interval, max_retries=max_retries,
                   )
    ...
    callback.delay(ret)

If the subtasks are ready, the callback gets queued for
execution. Otherwise, ``chord_unlock`` gets queued for a
retry. So...is this expensive? Well, maybe. Certainly more so than
checking a counter. Check out how ``ResultSet.ready()``
[works](https://github.com/celery/celery/blob/5c9ee7eb72f31fca789485d5bc3a8a4f3ee7b7a7/celery/result.py#L498)
-- it checks the ``.ready()`` property of each subtask, which
ultimately results in a call to ``_get_task_meta`` for each
subtask. Celery does a good job caching the task metadata, but
nonetheless this means examining the metadata for each task, each time
the chord_unlock polling task runs. I suspect this is what the docs
refer to when they warn of the synchronization being potentially
expensive.

So that's it -- an under-the-covers look at how Celery actually
coordinates tasks. I was surprised to learn that the strategy varied
to radically based on the broker backend, but certainly reaffirms my
love for Redis and all its flexibility.
