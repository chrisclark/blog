Title: Guidepost - Testing
Date: 2022-04-09
Author: Chris Clark
Slug: guidepost-testing
Category: Guideposts
Status: Published

The primary value of great tests is that it allows developers (especially those who didn’t write the original code!) to refactor. With tests at your back, you can refactor with confidence. Without the ability to refactor, our velocity will slowly decrease to zero.

We love automated testing. If you have ever found yourself deploying code to production based solely on your automated tests, and realizing afterwards - “Oh sh**! I never actually tested this manually!”, then you are doing it right. It is impossible for developers to have confidence their code works without tests.

If you think of tests as “homework”, or something to be added at the end, once it’s working - keep working at automated testing! Tests are your buddy along the development journey, ensuring at each step along the way that your software works the way you expect. If that feeling is not deep in your bones, keep working at it! Train yourself to find the joy and confidence in writing tests as you go.

It’s a very normal state of affairs that your change will have more test code than application code.

As you move from unit tests to integration tests, you take off diagnostic utility for coverage; unit tests cover little, but when they fail, it’s immediately clear what went wrong. Integration tests can cover a huge variety of regressions, but when they fail it’s harder to understand why. You need to be using both.

The broadest tests of all are browser/device automation tests. They are there to ensure that nothing terrible is about to happen in production, not ensure correctness of your code.

We aren’t believers in test-driven-development; it’s a great way to never get anything done.
