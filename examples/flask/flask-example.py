# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for
from flask.helpers import locked_cached_property
import jinja2_highlight

class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',
        []).append('jinja2_highlight.HighlightExtension')

    # If you'd like to set the class name of the div code blocks are rendered in
    # Uncomment the below lines otherwise the option below can be used
    #@locked_cached_property
    #def jinja_env(self):
    #    jinja_env = self.create_jinja_environment()
    #    jinja_env.extend(jinja2_highlight_cssclass = 'codehilite')
    #    return jinja_env

app = MyFlask(__name__)

# The second way to set the cssclass name for jinja2_highlight
#app.jinja_env.extend(jinja2_highlight_cssclass = 'codehilite')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
