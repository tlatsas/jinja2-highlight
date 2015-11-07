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

    inline_rendered = [
                u'<div',
                u'class="highlight"><pre>'
                u'<span',
                u'class="lineno">1</span>',
                u'<span',
                u'class="k">print</span><span',
                u'class="p">(</span><span',
                u'class="s">&quot;Hello',
                u'world&quot;</span><span',
                u'class="p">)</span>',
                u'</pre></div>'
            ]

    def test_python_tpl_with_inline(self):
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        tpl = env.from_string('''
            {% highlight "python", lineno="inline" %}
               print("Hello world")
            {% endhighlight %}
        ''')

        assert tpl.render().split() == self.inline_rendered

    table_rendered = [
                u'<table',
                u'class="highlighttable"><tr><td',
                u'class="linenos"><div',
                u'class="linenodiv"><pre>1</pre></div></td><td',
                u'class="code"><div',
                u'class="highlight"><pre>',
                u'<span',
                u'class="k">print</span><span',
                u'class="p">(</span><span',
                u'class="s">&quot;Hello',
                u'world&quot;</span><span',
                u'class="p">)</span>',
                u'</pre></div>',
                u'</td></tr></table>'
            ]

    def test_python_tpl_with_table(self):
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        tpl = env.from_string('''
            {% highlight "python", lineno="table" %}
               print("Hello world")
            {% endhighlight %}
        ''')

        assert tpl.render().split() == self.table_rendered

    inline_no_lang_rendered = [
        u'<div',
        u'class="highlight"><pre><span',
        u'class="lineno">1',
        u'</span>',
        u'<span',
        u'class="kn">from</span>',
        u'<span',
        u'class="nn">mypackage.mymodule</span>',
        u'<span',
        u'class="kn">import</span>',
        u'<span',
        u'class="n">myfn</span>',
        u'</pre></div>'
    ]

    def test_python_tpl_with_inline_no_lang(self):
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        tpl = env.from_string('''
            {% highlight lineno="inline" %}
               from mypackage.mymodule import myfn
            {% endhighlight %}
        ''')

        assert tpl.render().split() == self.inline_no_lang_rendered

    table_no_lang_rendered = [
        u'<table',
        u'class="highlighttable"><tr><td',
        u'class="linenos"><div',
        u'class="linenodiv"><pre>1</pre></div></td><td',
        u'class="code"><div',
        u'class="highlight"><pre>',
        u'<span',
        u'class="kn">from</span>',
        u'<span',
        u'class="nn">mypackage.mymodule</span>',
        u'<span',
        u'class="kn">import</span>',
        u'<span',
        u'class="n">myfn</span>',
        u'</pre></div>',
        u'</td></tr></table>'
    ]

    def test_python_tpl_with_table_no_lang(self):
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        tpl = env.from_string('''
            {% highlight lineno="table" %}
               from mypackage.mymodule import myfn
            {% endhighlight %}
        ''')


        assert tpl.render().split() == self.table_no_lang_rendered

    cssclass_rendered = [
                u'<div',
                u'class="codehilite"><pre>',
                u'<span',
                u'class="k">print</span><span',
                u'class="p">(</span><span',
                u'class="s">&quot;Hello',
                u'world&quot;</span><span',
                u'class="p">)</span>',
                u'</pre></div>'
            ]

    def test_python_tpl_with_cssclass(self):
        env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        env.extend(jinja2_highlight_cssclass = 'codehilite')
        #env.globals['jinja2_highlight_cssclass'] = 'codehilite'
        tpl = env.from_string('''
            {% highlight "python" %}
               print("Hello world")
            {% endhighlight %}
        ''')

        assert tpl.render().split() == self.cssclass_rendered
