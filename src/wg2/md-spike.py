import markdown

MD="""Title: Contact us!
Type: Info
Label: Contact
Text: This is multi-line text
      I will see what PythonMarkdown makes
      Of it.

RAREkits is the trading name of [Romilly Cocking](/about.html); RAREblog is his technical blog.

RAREkits is a virtual business, with no office or shop.

You can reach Romilly by email as romilly (dot) cocking (at) gmail (dot) com.
"""

md = markdown.Markdown(extensions = ['meta'])
html = md.convert(MD)
print(html)
print(md.Meta)