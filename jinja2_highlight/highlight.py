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

    Line numbers can be turned on if it is assigned. Either 'inline' or 'table'
    settings in Pygments can be used.

        {% highlight 'python', lineno='inline' %}

        from fridge import Beer

        pint_glass = Beer()
        pint_glass.drink()

        {% endhighlight %}

    Line numbers can also be used even if no language is assigned.
        {% highlight lineno='table' %}

        from fridge import Beer

        pint_glass = Beer()
        pint_glass.drink()

        {% endhighlight %}
    """
    tags = set(['highlight'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # extract the language and line numbering setting if available
        if not parser.stream.current.test('block_end'):
            # If first up we have an assignment, e.g. lineno='inline', work with that
            if parser.stream.current.type == 'name':
                name = parser.stream.expect('name')
                # If the assign is lineno
                if name.value == 'lineno':
                    if parser.stream.skip_if('assign'):
                        # Assume no language and then add the assigned line number setting
                        args = [nodes.Const(None)]
                        args.append(parser.parse_expression())
                # If it's not a lineno assignment, ignore it
                else:
                    if parser.stream.skip_if('assign'):
                        next(parser.stream)
                        # Set our language and line number setting as None
                        args = [nodes.Const(None), nodes.Const(None)]
            else:
                # Otherwise if our first item is not a line numbering setting,
                # assume it's the language setting
                args = [parser.parse_expression()]

                # If we have a comma next
                if parser.stream.skip_if('comma'):
                    # Check to see if we have a lineno assignment
                    if parser.stream.current.type == 'name':
                        name = parser.stream.expect('name')
                        if name.value == 'lineno':
                            if parser.stream.skip_if('assign'):
                                args.append(parser.parse_expression())
                        # If the name of the variable being assigned is not lineno
                        # ignore it
                        else:
                            if parser.stream.skip_if('assign'):
                                next(parser.stream)
                                args.append(nodes.Const(None))
                # Otherwise if there's nothing after the language, set the
                # line number setting as None
                else:
                    args.append(nodes.Const(None))
        else:
            # Otherwise if there are no additional arguments, set lang
            # and line numbering to None
            args = [nodes.Const(None), nodes.Const(None)]

        # body of the block
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        return nodes.CallBlock(self.call_method('_highlight', args),
                               [], [], body).set_lineno(lineno)

    def _highlight(self, lang, linenos, caller=None):
        # highlight code using Pygments
        body = caller()

        # Check the globals to see if a cssclass setting for Pygment's HtmlFormatter
        # has been set
        try:
            cssclass = self.environment.jinja2_highlight_cssclass
        except AttributeError:
            cssclass = None

        try:
            if lang is None:
                lexer = guess_lexer(body)
            else:
                lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound as e:
            print(e)
            sys.exit(1)

        # Set the cssclass if we have one
        # The linenos setting expects either 'inline' or 'table', as per Pygment's
        # settings, any true value except 'inline' results in 'table'. If linenos
        # hasn't been assigned in parse it will be None and will result in no
        # line numbers
        if cssclass is not None:
            formatter = HtmlFormatter(cssclass=cssclass, linenos=linenos)
        else:
            formatter = HtmlFormatter(linenos=linenos)

        # If you place the tag on the line under the code, like this;
        # pint_glass.drink()
        # {% endhighlight %}
        # The result will have an extra blank line underneath, this can cause an extra
        # blank line of line numbering.
        # Use rstrip to remove extraneous white space
        code = highlight(Markup(body.rstrip()).unescape(), lexer, formatter)
        return code

