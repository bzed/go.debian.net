# -*- coding: utf-8 -*-
__author__ = "Bernd Zeimetz"
__contact__ = "bzed@debian.org"
__license__ = """
Copyright (C) 2010-2013 Bernd Zeimetz <bzed@debian.org>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import urllib

from ..manage import get_url, add_url, add_static_url, update_static_url, count
from ..config import FlaskConfig, UrlencoderConfig

from .jsonrpc import jsonmethod, jsondispatch

try:
    from . import flask
except ImportError:
    import flask

import werkzeug


app = flask.Flask(__name__)
__all__ = ["app"]
app.debug = FlaskConfig.debug
app.request_class.max_content_length = FlaskConfig.max_content_length

class RegexConverter(werkzeug.routing.BaseConverter):
    """ This converter accepts regular expressions to match URLs.

    Example:

        Rule('/pages/<re(regex=r"[234asd]+[a-z]*"):page>')

    :param regexp: regular expression to match. Will be passed to
                    the converter's self.regexp as it is.
    """
    def __init__(self, map, regex):
        werkzeug.routing.BaseConverter.__init__(self, map)
        self.regex = regex
app.url_map.converters['re'] = RegexConverter

class ShortUrlConverter(RegexConverter):
    def __init__(self, map):
        regex = '[' + UrlencoderConfig.alphabet + ']+'
        RegexConverter.__init__(self, map, regex)
app.url_map.converters['shorturl'] = ShortUrlConverter


class RawRequest(flask.Request):
    def _load_form_data(self):
        if not self.use_raw_stream:
            return werkzeug.Request._load_form_data()

        if 'stream' in self.__dict__:
            return
        if self.shallow:
            raise RuntimeError('A shallow request tried to consume '
                               'form data.  If you really want to do '
                               'that, set `shallow` to False.')
        cls = self.parameter_storage_class or werkzeug.datastructures.MultiDict
        content_length = self.headers.get('content-length', type=int)
        if self.max_content_length is not None and content_length > self.max_content_length:
            raise werkzeug.exceptions.RequestEntityTooLarge
        if content_length is not None:
            stream = werkzeug.wsgi.LimitedStream(self.environ['wsgi.input'],
                                                 content_length)
        else:
            raise werkzeug.exceptions.LengthRequired
        data = (stream, cls(), cls())
        d = self.__dict__
        d['stream'], d['form'], d['files'] = data
app.request_class = RawRequest


def _check_access(ip):
    for allowed_ip in FlaskConfig.allowed_rpc_ips:
        if ip in allowed_ip:
            return True
    return False

__robots_txt = """User-agent: *
Allow: /
"""
@app.route('/robots.txt')
def robots_txt():
    return app.response_class(__robots_txt, mimetype='text/plain')


__indexopts = { 'title' : 'Welcome!' }
if FlaskConfig.google_site_verification:
    __indexopts['google_site_verification'] = FlaskConfig.google_site_verification
@app.route('/')
def index():
    return flask.render_template('index.html', **__indexopts)

@app.route('/imprint.html')
def imprint():
    return flask.render_template('imprint.html')


@app.route('/<shorturl:key>')
def redirect_by_key(key):
    url = get_url(key)
    if url:
        return flask.redirect(urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]").encode('ascii'))
    else:
        return flask.abort(404)

@app.route('/p/<shorturl:key>')
def redirect_by_key_with_preview(key):
    url = get_url(key)
    if not url:
        return flask.abort(404)
    return flask.render_template('redirect-preview.html',
        domain=FlaskConfig.domain,
        key=key,
        url=url, url_quoted=urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))

@app.route('/<re(regex=r".+@.+"):msgid>')
def redirect_to_lists_debian_org(msgid):
    return flask.redirect('https://lists.debian.org/msgid-search/%s' %(msgid, ), code=301)

@app.route('/stats.html')
def statistics():
    return flask.render_template('statistics.html',
        static_urls=count(is_static=True),
        non_static_urls=count(is_static=False))


def __remote_address__():
    uwsgi = flask.request.environ.get('uwsgi.version')
    if uwsgi:
        remote_address = flask.request.remote_addr
    else:
        try:
            remote_address = flask.request.headers.getlist("X-Forwarded-For")[0]
        except Exception:
            remote_address = flask.request.remote_addr
    return remote_address

@app.route('/rpc/json', methods=['POST'])
def rpc_json():
    remote_address = __remote_address__()
    if not _check_access(remote_address):
        return flask.abort(401)
    flask.request.use_raw_stream = True
    result = jsondispatch(flask.request.data)
    if result == None:
        return flask.abort(400)
    return flask.jsonify(**result)

@jsonmethod('add_url')
def json_add_url(url):
    return add_url(url, log=__remote_address__())

@jsonmethod('add_static_url')
def json_add_static_url(url, key):
    return add_static_url(url, key, log=__remote_address__())

@jsonmethod('update_static_url')
def json_update_static_url(url, key):
    return update_static_url(url, key, log=__remote_address__())

@jsonmethod('get_url')
def json_get_url(key):
    return get_url(key)


def show_errormessage(error):
    template_data = { 
        'code' : error.code,
        'name' : error.name,
        'description' : error.get_description(flask.request.environ)
    }
    return flask.render_template('error.html', **template_data), error.code

def _assign_errorhandler(i):
    app.error_handlers[i] = show_errormessage
map(_assign_errorhandler,
    werkzeug.exceptions.default_exceptions.iterkeys())
del _assign_errorhandler

