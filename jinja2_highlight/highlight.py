# -*- coding: utf8 -*-

import sys
from jinja2 import nodes
from jinja2.ext import Extension, Markup

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

class HighlightExtension(Extension):
    """Highlight code blocks using Pygments.

    Example::

        {% highlight 'python' %}

        from fridge import Beer

        pint_glass = Beer()
        pint_glass.drink()

        {% endhighlight %}

    Line numbers can be turned in if True is passed in addition to the language.

        {% highlight 'python', True %}

        from fridge import Beer

        pint_glass = Beer()
        pint_glass.drink()

        {% endhighlight %}
    """
    tags = set(['highlight'])

    # TO DO: What if they want line numbers but don't pass the language?
    # E.g. {% highlight True %}

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # extract the language if available
        if not parser.stream.current.test('block_end'):
            args = [parser.parse_expression()]

            # If there's a comma, get the next argument
            if parser.stream.skip_if('comma'):
                args.append(parser.parse_expression())
            else:
                args.append(nodes.Const(None))
        else:
            args = [nodes.Const(None)]

        # body of the block
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        return nodes.CallBlock(self.call_method('_highlight', args),
                               [], [], body).set_lineno(lineno)

    def _highlight(self, lang, linenos, caller=None):
        # highlight code using Pygments
        body = caller()

        if 'jinja2_highlight_cssclass' in self.environment.globals:
            cssclass = self.environment.globals['jinja2_highlight_cssclass']
        else:
            cssclass = None

        if linenos:
            linenos = 'inline'

        try:
            if lang is None:
                lexer = guess_lexer(body)
            else:
                lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound as e:
            print(e)
            sys.exit(1)

        if cssclass is not None:
            formatter = HtmlFormatter(cssclass=cssclass, linenos=linenos)
        else:
            formatter = HtmlFormatter(linenos=linenos)
        # If you place the tag on the line under the code, like this;
        # pint_glass.drink()
        # {% endhighlight %}
        # The result will have an extra blank line underneath, use strip
        # to remove extraneous white space? Will this cause issues?
        # Maybe just use rstrip instead?
        code = highlight(Markup(body.strip()).unescape(), lexer, formatter)
        return code

