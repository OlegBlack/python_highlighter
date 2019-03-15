"""Flask module
file: __init__.py
date: 12.12.2012
author smith@example.com
license: MIT"""

import re
from flask import Flask, render_template, request, Markup


def create_app():
    """Create flask app for binding."""
    app = Flask(__name__)

    template_file_name = 'index.html'

    @app.route('/', methods=['GET'])
    def index():
        return render_template(template_file_name)

    @app.route('/', methods=['POST'])
    def process():
        search_text = request.form['search']
        text = request.form['text']
        highlighted_text = highlight_text(text, search_text)
        result = {'text': text,
                  'highlighted_text': Markup(highlighted_text),
                  }
        return render_template(template_file_name, **result)

    def markup_text(text):
        """Markup given text.
        @:param text - string text to be marked
        @:return marked text, e.g., <mark>highlighted text</mark>."""

        result = "<mark>" + text + "</mark>"

        return result

    def prefix(sub_string):
        """Return array of p(i) - list of prefix function result"""
        p = [0, ]
        j = 0
        i = 1
        while i < len(sub_string):
            if sub_string[i] == sub_string[j]:
                p.append(j + 1)
                i += 1
                j += 1
            else:
                if j == 0:
                    p.append(0)
                    i += 1
                else:
                    j = p[j - 1]
        return p

    def kmp(s, sub_s):
        """Find substring in string by Knuth-Morris-Pratt algorithm
        and return a list of first index of substring in string"""
        k = 0
        j = 0
        p = prefix(sub_s)
        result = []

        while k < len(s):
            if sub_s[j] == s[k]:
                k += 1
                j += 1
                if j == len(sub_s):
                    result.append(k - len(sub_s))
                    j = 0
            elif j == 0:
                k += 1
            else:
                j = p[j - 1]

        return result

    def highlight_text(text, expr):
        """Markup searched string in given text.
        @:param text - string text to be processed
        @:return marked text, e.g., "sample text <mark>highlighted part</mark> rest of the text"."""

        # result = re.sub(re.compile(expr), markup_text(expr), text)
        # result = text.replace(text, markup_text(expr))

        length_sub_s = len(expr)
        i = kmp(text, expr)
        n = 0
        j = 0
        ch_sub = markup_text(expr)
        result = ''

        while n < len(i):
            result += text[j:i[n]] + ch_sub
            j = len(text[:i[n]]) + length_sub_s
            n += 1
        result += text[j:]

        return result

    return app
