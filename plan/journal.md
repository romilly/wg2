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
uses a local `img` directory and copy all the files to the output directory.


## Friday 15 May 2020

After a rest, time to resume.

I was tempted to do a third version but that's silly: I can create the core site with the current architecture, and the key thing now is to deliver business value as fast as I can.

All tests are passing but the template is in a muddle; it looks like the old clean-blog template.

## Saturday 16 May 2020

Also, I need to make sure that I have separate contents fro production and test, and that the correct templates are being used.

PM: Things are going well, and bow I want to tackle menu highlighting: the menu for each page is slightly different for each page type.

It looks as if the templates used in the non-webdriver tests are old, and based on clean blog, not the small business template.

I've been puzled by `<span class="sr-only">(current)</span>`; it turns out that `sr-only` indicates that the element is only shown to screen-readers to help with accessibility.

So the tests could check for the presence/absence of the span as well as the `active` class in the menu item.

## Sunday 17 May 2020

I'm now using inheritance and inclusion for menus.


## Monday 18 May 2020

While I still need to keep production and test data separate, there's no reason not to share templates where that is appropriate, so I am going to

1. Provide an environment, rather than a directory, to HtmlFormatter.
1. Provide a fixed template to the appropriate HtmlFormatter unit test
1. Use the production templates for the e2e tests as well as the webdriver tests.

Next step: smarter menu generation, with the active page highlit.

That in turn requires generation of a resources index, so I'll add a test for the page and get that passing.


## Tuesday 19 May 2020

I realised two things before I started work this morning:
 
1. I don't *have* to generate the resources index page from multiple resources and create it in a separate directory
1. The old tree-walking code should create a resources index page in the resources sub-directory anyway, and I could then just put the resources material into the resources template.

Next step: get menus done.

## Thursday 21 May 2020

Lots more progress.

Asset links now start with a /.

Menus are looking good.

All pages are styled, though the templates need work.

### Responsive fonts

I tweaked [this example](https://bootstrapcreative.com/can-adjust-text-size-bootstrap-responsive-design/) to change the paragraph font size on large screens.

I've also just spotted that `small-business.css` and `blog-post.css` are identical, so I'll get rid of one of them which will simplify the header stuff.



