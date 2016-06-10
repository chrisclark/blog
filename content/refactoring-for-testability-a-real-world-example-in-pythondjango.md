Title: Refactoring for Testability: A Real World Example in Python/Django
Date: 2014-04-21 22:25
Author: Chris Clark
Slug: refactoring-for-testability-quick
Category: code & tutorials

At [ePantry](https://www.epanty.com/), we strive to have enough automated
test coverage that we can deploy with confidence, without being dogmatic
about our approach. We certainly aren't a TDD shop, and we don't have
rules about code coverage metrics ("no commit can reduce code
coverage!"), but it's very unusual that a non-cosmetic change makes it
to production without some sort of test coverage.

But it wasn't a
straightforward journey - our team didn't have much experience with
"good" testing practices. In a few previous companies, tests if they
were required at all, were viewed as a burden; "extra work" to tack on
to your commit at the very end.

So building a culture
around automated testing took time. To the extent we've succeeded, we
did it by brute force: we just wrote the damn tests. After a couple of
months of this and one by one, we built up enough actually internalize
two key lessons:
  
1.  It's actually *faster* to develop if you write the tests alongside
    your code. Clicking around in the browser reproducing bugs is slow
    and unreliable and not very fun.
2.  Writing tests actually catches a *lot* of bugs before they make it
    into production. I'm now physically uncomfortable deploying
    untested code.

But it took a bit of wandering through the testing wilderness to get there.

The other day at ePantry
we refactored a bit of code for testability that I think provides a nice
example of both the mechanics and the value of automated testing -
something that I think can be tricky to understand from toy examples.
The refactoring was simple, but yielded code that is easier to maintain,
more composable, and (most importantly) allowed us to deploy a major
feature with a high degree of confidence.

First, some background:

At ePantry we generate
suggested shipments of household goods based on predicted consumption
habits of the household. When a customers signs up, we generate roughly
a year of suggested shipments. For instance, here's what a schedule
looks like to a user on the front end:

![epantry-dashboard](http://2.bp.blogspot.com/-Afeap6zt2Lk/U1K2rlIGoSI/AAAAAAAAAJU/1Tbe3S6zLAQ/s1600/Screen+Shot+2014-04-19+at+10.46.34+AM.png)

Over time, the household
"consumes" those shipments and we need to generate more to keep the
calendar populated with future shipments. We wrote a function that would
run as an overnight chron job to "top up" the shipments of all of our
customers so each customer always has at least a year of shipments on
the calendar.

Below is a code snippet
as it first appeared in our codebase, sans-tests. The code itself is
simple, but it was a bit scary to deploy into production because it runs
asynchronously, touches a lot of customers, and would not be easy to
unwind if it ran amok. I've removed some bits of logging for clarity,
but this is otherwise just as it appeared in the original commit.

    :::python
    def create_shipments_async():
        search_date = add_months(datetime.date.today(), \
                                 settings.SHIPMENTS_UNTIL_AT_LEAST_MONTHS)
        customers = Customer.objects \
                     .annotate(last_shipment_date=Max('pantry__shipments__arrival_date')) \
                        .filter(last_shipment_date__lt=search_date) \
                        .filter(card_on_file=True)
    
        for customer in customers:
            cur_date = customer.last_shipment_arrival_date()
            while cur_date < search_date:
                shipment = customer.pantry.create_next_shipment()
                cur_date = shipment.arrival_date

Here's what it does:

- First we find the date in the
future that we want all customers to have shipments until. This is set
to 12 months in our settings file.

- Next we get all of the active
customers (those who have a credit card on file) whose last shipment
arrives *before* the cutoff date. These customers need more shipments
generated.

- Finally, for each of the
customers, we loop through and create shipments for each customer until
the arrival date of the last shipment is past our target
date.

Simple! But also
untested and therefore scary. We tested it locally by cloning the
production database and running the function through the Django shell.
It *seemed* to work. But that's not good enough. This is too important
and too complicated to be left to manual testing. So let's write some
unit tests.

As is, this code is
difficult to test. It's one big function doing a bunch of stuff and we
can't test the components in isolation. If you look at the english
language explanation of the code above, there are really three distinct
steps, each of which can be separately verified. We can refactor to
represent each of those three steps:

    :::python
    def _shipments_until_date():
        return add_months(datetime.date.today(), \
                          settings.SHIPMENTS_UNTIL_AT_LEAST_MONTHS)
    
    def _get_customers_without_enough_shipments(search_date):
        return Customer.objects \
            .annotate(last_shipment_date=Max('pantry__shipments__arrival_date')) \
            .filter(last_shipment_date__lt=search_date) \
            .filter(card_on_file=True)
    
    def _create_until(customer, last_shipment_date, search_date):
        if last_shipment_date < search_date:
            _create_until(customer, \
                          customer.pantry.create_next_shipment().arrival_date, \
                          search_date)
        
Now what does our top-level function look like?

    :::python
    def create_shipments_async():
        map(lambda customer: _create_until(customer, \
                                       customer.last_shipment_arrival_date(), \
                                       _shipments_until_date()), \
               , _get_customers_without_enough_shipments(_shipments_until_date()))

Piece of cake! Literally one line of code. We map our \_create\_until function onto the
collection of customers without enough shipments. All the detail is in
our three component functions (note that \_create\_until is just a
recursive loop - it could certainly be implemented in a more imperative
style of that's your thing).

We just need a handful
of tests on these functions, and one good test on the high level
function, and we gain a tremendous amount of confidence and robustness
in the code. I glossed over it here, but I also discovered a few small
bugs in our Django ORM query while writing the tests. Here are a few
example tests, using Django's test framework and Factory Boy to create
mock objects.

    :::python
    from django.test import TestCase
    from pypantry.tests.factories import PantryFactory
    from schedule.tests.factories import ShipmentFactory
    from pypantry.tasks import *
    from datetime import timedelta, datetime
    from utils.utils import add_months
    
    
    class TestShipmentGenTask(TestCase):
    
        def setUp(self):
            self.p = PantryFactory()
            self.c = self.p.customer
            self.c.set_card_on_file('foo')
            self.c.save()
            self.s1 = ShipmentFactory(pantry=self.c.pantry)
    
        def test_finds_customers(self):
            self.s1.arrival_date = _shipments_until_date() - timedelta(1)
            self.s1.save()
            res = _get_customers_without_enough_shipments(_shipments_until_date())
            self.assertEqual(len(res), 1)
    
        def test_ignores_customers_with_enough_shipments(self):
            self.s1.arrival_date = _shipments_until_date()
            self.s1.save()
            res = _get_customers_without_enough_shipments(_shipments_until_date())
            self.assertEqual(len(res), 0)
    
        def test_shipments_get_created(self):
            self.s1.arrival_date = datetime.strptime('15042014', "%d%m%Y").date()
            self.s1.save()
            _create_until(self.c, self.s1.arrival_date, add_months(self.s1.arrival_date, 12))
            # one extra because it goes one shipment "past" the target date
            self.assertEqual(self.p.shipments.count(), 13) 
    
        def test_task(self):
            self.s1.arrival_date = _shipments_until_date() - timedelta(1)
            self.s1.save()
            create_shipments_async()
            self.assertEqual(self.p.shipments.count(), 2)
    
Ta-da! Of course there
are plenty of other tests you could write, but just these four basic
tests exercise the code reasonably well. And it would have been
virtually impossible to get this level of testing fidelity with the
original function. Plus, if one of these tests fails due to a later
commit, we can immediately hone in on the cause. The refactoring and
tests took less than an hour, and it will save me at least that much
worry.

I hope you found this a
useful, real world example of refactoring for testability. Love to hear
any additional thoughts in the comments!

P.S. This code made it
into production yesterday and ran successfully for the first time last
night. Phew! Also -- you should sign up for
[ePantry](https://www.epantry.com/) and never run out of soap or toilet
paper ever again.
