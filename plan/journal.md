# Project journal for wg2

Most of wg2 is now working, but I think the pass-the-buck architecture is more trouble than it's worth.

In particular, I can get rid of a lot of mocks!

For each transformer I will
1. Return a result as well as passing the buck
1. Change the unit tests to check the result, writing new unit tests as necessary.
1. Change build to do a series of functional transformations
1. Get the e2e test running
1. Get rid of the buck-passing

So - almost there, and I realise that the one thing I must use pass-the-buck to test is the site-builder itself.

So I guess I need to undo all the work - or do I? I'll have a ponder.

Maybe do the transformation chain in a PipelineConverter, which takes MarkdownPages in and passes on HtmlPages to a Writer?


## Sunday 03 May 2020

I'm getting rid of the ADRs as these duplicate the more detailed discussion in this journal.

Slept on it, and am growing to try a PipelineConverter which combines the transformers, taking MarkdownPages as inputs
sending HtmlPages to a writer.

I made more progress than I gave myself credit for, but adding some good unit tests for the transformers.

So:

1. Create a PipelineConverter which implements Converter constructed from a list of transformers ending with a sink. 
1. Use it in the e2e test.
1. See what happens!

After some refactoring all tests are passing.


Next, remove successors from each transformer.

All working - time to return to adding functionality from Trello!

18:20 - Navigation tests started. Home page working!

Tomorrow - handle images in background-image metadata.


## Monday 04 May 2020

Tomorrow -  try [mobile testing](https://www.axelerant.com/resources/team-blog/how-to-test-and-debug-local-sites-on-mobile-devices-connected-to-a-network)?

## Wednesday 06 May 2020

Not much coding done yesterday, but some profitable research.

I'm going to use two example bootstrap pages and use a CTA card instead of a sticky footer.

Here are the links:
1. [Home page](https://blackrockdigital.github.io/startbootstrap-small-business)
1. [Blog post](https://startbootstrap.com/templates/blog-post/)

So. Preparing for the switch I will
  
1. ~~diff the sample home page and my template so I have a list of stuff to add.~~
1. commit the current state
1. delete the current bootstrap stuff and add a clean copy
1. unzip the two templates
1. Edit the home page and a post page to see what they are like