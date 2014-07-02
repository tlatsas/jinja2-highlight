jinja2-highlight
################

About
=====

A simple Jinja2 extension that uses Pygments to highlight code blocks.


.. image:: https://travis-ci.org/tlatsas/jinja2-highlight.svg?branch=master
    :target: https://travis-ci.org/tlatsas/jinja2-highlight


Source
======

Github: https://github.com/tlatsas/jinja2-highlight

Pypi: http://pypi.python.org/pypi/jinja2-highlight


Requirements
============

* Jinja2 >= 2.4
* Pygments >= 1.5


Highlight examples
=================
::

    {% highlight 'language' %}
    your-awesome-code-here
    {% endhighlight %}

Replace `language` with the appropriate Pygments lexer short name: http://pygments.org/docs/lexers/

Line numbering can be turned on using `lineno='inline'` or `lineno='table'` depending on the style of line numbering you want (as per Pygment's documentation: http://pygments.org/docs/formatters/#HtmlFormatter)

::

    {% highlight 'language', lineno='inline' %}
    your-awesome-code-here
    {% endhighlight %}

This can also be used without a language setting

::

    {% highlight lineno='table' %}
    your-awesome-code-here
    {% endhighlight %}

Optional settings
================

By default Pygments renders the code block inside a div with the class 'highlight', if you want to change the name you can set the environment variable `jinja2_highlight_cssclass` to the class name you would like.

In jinja this can be done after you've created your environment;
::

    env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
    # Set the css class name to 'codehilite'
    env.extend(jinja2_highlight_cssclass = 'codehilite')

In Flask this can be done with the following (after creating your app):
::

    app.jinja_env.extend(jinja2_highlight_cssclass = 'codehilite')



Using with Flask
================

See the example at: https://github.com/tlatsas/jinja2-highlight/tree/master/examples/flask

