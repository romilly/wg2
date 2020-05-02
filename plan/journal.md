# Project journal for wg2

Most of wg2 is now working, but I think the pass-the-buck architecture is more trouble than it's worth.

In particular, I can get rid of a lot of mocks!

For each transformer I will
1. Return a result as well as passing the buck
1. Change the unit tests to check the result, writing new unit tests as necessary.
1. Change build to do a series of functional transformations
1. Get the e2e test running
1. Get rid of the buck-passing


