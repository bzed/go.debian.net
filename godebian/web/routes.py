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


from bottle import route, view, redirect, request, abort, debug, TEMPLATE_PATH
from ..manage import get_url
from ..config import BottleConfig
from .jsonrpc import jsonmethod, jsondispatch

debug(BottleConfig.debug)
TEMPLATE_PATH = BottleConfig.templatepath

@route('/')
def index():
    return 'Hello World!'

@route('/:key#[0-9a-zA-Z]+#')
def redirect_by_key(key):
    url = get_url(key)
    if url:
        redirect(url)
    else:
        abort(404, "Unable to find site's URL to redirect to.")

@route('/rpc/json', method='POST')
def rpc_json():
    return jsondispatch(request.POST.keys()[0])

@jsonmethod('add_url')
def json_add_url(url):
    return 12314

@jsonmethod('add_static_url')
def json_add_static_url(url, key):
    pass

@jsonmethod('get_url')
def json_get_url(key):
    pass

