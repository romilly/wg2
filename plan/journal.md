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

Prepared for the switch.
  
1. diffed the sample home page and my template so I have a list of stuff to add.
1. committed the current state.
1. deleted the current bootstrap stuff and add a clean copy
1. unzipped the two templates
1. Edited the home page and a post page to see what they are like

The templates use bootstrap 4.3.1, with all that's needed in the vendor directory.

I will leave as much of the current structure unchanged. I'll copy and rename the two index.html files for the start-bootstrap templates into our template directory.

The builder should
1. copy one of the start-bootstrap template directories to the output directory
1. do the generation


## Friday 08 May 2020

Some progress yesterday, but mostly a day of reflection.

I'm still getting my head around what I want as the home page CTA.

I'll take a look at some non-shop sites; developerWorks, TW, Raspberry Pi.


## Tuesday 12 May 2020

I realised on Saturday that the CTA could be `Ko-fi me`. I'm going to give that a go.

Also, home page content could be a static template to start with, adding news items at the bottom later on.

Generation could also be simpler, with the 3 page locations being hard-coded.

I'm going to change the tests to use test data, not live data (which is a lesson I thought I'd learned long ago).

I'll eventually have Navigation tests (and maybe some others) that use the live data.

I am going to remove the image moving stuff for from the pipeline for now. It will be useful for the blog conversion, but for the main site I will assume that markdown
uses a local resources/images directory and copy all the files to the output directory.

