import unittest
import jinja2_highlight

from jinja2 import Environment


class HighlightExtensionTestCase(unittest.TestCase):

    rendered = [
                u'<div',
                u'class="highlight"><pre>',
                u'<span',
                u'class="k">print</span><span',
                u'class="p">(</span><span',
                u'class="s">&quot;Hello',
                u'world&quot;</span><span',
                u'class="p">)</span>',
                u'</pre></div>'
            ]

    def test_python_tpl(self):
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        tpl = env.from_string('''
            {% highlight "python" %}
               print("Hello world")
            {% endhighlight %}
        ''')

        assert tpl.render().split() == self.rendered

    def test_python_tpl_with_autoescape(self):
        # See: https://github.com/tlatsas/jinja2-highlight/pull/1
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        env.add_extension('jinja2.ext.autoescape')
        tpl = env.from_string('''
            {% autoescape true %}
            {% highlight "python" %}
               print("Hello world")
            {% endhighlight %}
            {% endautoescape %}
        ''')

        assert tpl.render().split() == self.rendered
