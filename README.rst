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


Highlight example
=================
::

    {% highlight 'language' %}
    your-awesome-code-here
    {% endhighlight %}

Replace `language` with the appropriate Pygments lexer short name: http://pygments.org/docs/lexers/


Using with Flask
================

See the example at: https://github.com/tlatsas/jinja2-highlight/tree/master/examples/flask

