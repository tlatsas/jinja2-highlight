# -*- coding: utf8 -*-

import sys
from jinja2 import nodes
from jinja2.ext import Extension, Markup

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer
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
        valid_arguments = ('lineno',)
        parsed_args = {}

        # extract the language and line numbering setting if available
        while not parser.stream.current.test('block_end'):
            cur_token_type = parser.stream.current.type
            # If up we have an assignment, e.g. lineno='inline', work with that
            if cur_token_type == 'name':
                name = parser.stream.expect('name')
                if name.value in valid_arguments and parser.stream.skip_if('assign'):
                    parsed_args[name.value] = parser.parse_expression()
                else:
                    parser.fail('Unrecognized argument %s' % name.value)
            elif cur_token_type == 'string':
                # The only valid string argument is the language
                parsed_args['lang'] = parser.parse_expression()
            else:
                parser.fail('Unexpected %s encountered' % cur_token_type)

            # Skip over optional commas
            parser.stream.skip_if('comma')

        # body of the block
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        # The args passed to call_method below need to be a list, but we can at
        # least set the order here.
        parsed_args_list = [
            parsed_args.get('lang', nodes.Const(None)),
            parsed_args.get('lineno', nodes.Const(None))
        ]

        return nodes.CallBlock(self.call_method('_highlight', parsed_args_list),
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
            # default to the plaintext lexer
            lexer = TextLexer()

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

