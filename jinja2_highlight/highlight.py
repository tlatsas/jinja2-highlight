# -*- coding: utf8 -*-

import sys
from jinja2 import nodes
from jinja2.ext import Extension, Markup

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

class HighlightExtension(Extension):
    """Highlight code blocks using Pygments

    Example::

        {% highlight 'python' %}

        from fridge import Beer

        pint_glass = Beer()
        pint_glass.drink()

        {% endhighlight %}
    """
    tags = set(['highlight'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno

        # TODO:
        # add support to show line numbers

        # extract the language if available
        if not parser.stream.current.test('block_end'):
            lang = parser.parse_expression()
        else:
            lang = nodes.Const(None)

        # body of the block
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        return nodes.CallBlock(self.call_method('_highlight', [lang]),
                               [], [], body).set_lineno(lineno)

    def _highlight(self, lang, caller=None):
        # highlight code using Pygments
        body = caller()
        try:
            if lang is None:
                lexer = guess_lexer(body)
            else:
                lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound as e:
            print(e)
            sys.exit(1)

        formatter = HtmlFormatter()
        code = highlight(Markup(body).unescape(), lexer, formatter)
        return code

