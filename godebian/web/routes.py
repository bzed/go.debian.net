# -*- coding: utf-8 -*-
__author__ = "Bernd Zeimetz"
__contact__ = "bzed@debian.org"
__license__ = """
Copyright (C) 2010 Bernd Zeimetz <bzed@debian.org>

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

import cgi
import os

from .bottle import jinja2_view, jinja2_template, route, redirect, request, debug, send_file, HTTPError, HTTP_CODES

from ..manage import get_url, add_url, add_static_url, count
from ..config import BottleConfig, UrlencoderConfig

from .jsonrpc import jsonmethod, jsondispatch

debug(BottleConfig.debug)


_template_lookup=[os.path.realpath(BottleConfig.template_dir)]
def view(tpl_name, **kargs):
    kargs['template_lookup'] = _template_lookup
    return jinja2_view(tpl_name, **kargs)

def template(tpl_name, **kargs):
    kargs['template_lookup'] = _template_lookup
    return jinja2_template(tpl_name, **kargs)


class NiceHTTPError(HTTPError):
    def __repr__(self):
        kargs = {
                    'status' : self.status,
                    'url' : request.path,
                    'error_name' : HTTP_CODES.get(self.status, 'Unknown').title(),
                    'error_message' : cgi.escape(''.join(self.output)),
                    'debug' : BottleConfig.debug
                }
        if self.traceback:
            kargs['traceback'] = cgi.escape(str(self.traceback))
        if self.exception:
            kargs['exception'] = cgi.escape(str(self.excetion))
        return template('error', **kargs)

def abort(code=500, text='Unknown Error: Appliction stopped.'):
    raise NiceHTTPError(code, text)

def _check_access(ip):
    for allowed_ip in BottleConfig.allowed_rpc_ips:
        if ip in allowed_ip:
            return True
    return False

__indexopts = { 'title' : 'Welcome!' }
if BottleConfig.google_site_verification:
    __indexopts['google_site_verification'] = BottleConfig.google_site_verification
@route('/')
@view('index')
def index():
    return __indexopts

@route('/imprint.html')
@view('imprint')
def imprint():
    return {}

@route('/static/:filename')
def static_file(filename):
    send_file(filename, root=BottleConfig.static_dir)

@route('/robots.txt')
def static_file(filename):
    send_file('robots.txt', root=BottleConfig.static_dir)


@route('/:key#[' + UrlencoderConfig.alphabet + ']+#')
def redirect_by_key(key):
    url = get_url(key)
    if url:
        redirect(url)
    else:
        abort(404, "Unable to find an URL to redirect to.")

@route('/p/:key#[' + UrlencoderConfig.alphabet + ']+#')
@view('redirect-preview')
def redirect_by_key_with_preview(key):
    url = get_url(key)
    if not url:
        abort(404, "Unable to find an URL to redirect to.")
    return {
        'domain' : BottleConfig.domain,
        'key' : key,
        'url' : url
    }

@route('/:msgid#.+@.+#')
def redirect_to_lists_debian_org(msgid):
    redirect('http://lists.debian.org/%s' %(msgid, ))

@route('/rpc/json', method='POST')
def rpc_json():
    remote_address = request.environ['REMOTE_ADDR']
    if not _check_access(remote_address):
        abort(401)
    return jsondispatch(request.body.getvalue())

@route('/stats.html')
@view('statistics')
def statistics():
    return {
        'static_urls' : count(is_static=True),
        'non_static_urls' : count(is_static=False)
    }

@jsonmethod('add_url')
def json_add_url(url):
    return add_url(url, log=request.environ['REMOTE_ADDR'])

@jsonmethod('add_static_url')
def json_add_static_url(url, key):
    return add_static_url(url, key, log=request.environ['REMOTE_ADDR'])

@jsonmethod('get_url')
def json_get_url(key):
    return get_url(key)

