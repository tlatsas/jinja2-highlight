# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for
import jinja2_highlight

class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',
        []).append('jinja2_highlight.HighlightExtension')

app = MyFlask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
