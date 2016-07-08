# -*- coding: utf-8 -*-
from __future__ import print_function
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

try:
    from .flask import json
except ImportError:
    from flask import json

import sys
import traceback

_JSONMETHODS = {}


def jsonmethod(methodname):
    def wrapper(handler):
        _JSONMETHODS[methodname] = handler

    return wrapper


def jsondispatch(data):
    try:
        rawdata = json.loads(data)
    except SyntaxError:
        print("SyntaxError in data: %s" % (data,))
        return None
    except ValueError:
        print("ValueError in data: %s" % (data,))
        return None
    id = rawdata.get('id', 0)
    ret_dict = {'id': id, 'error': None}

    # method = rawdata.get('method', None)
    method = rawdata.get('method')
    if not method:
        ret_dict['error'] = 'method missing in request'
        return json.dumps(ret_dict)

    params = rawdata.get('params', [])

    # handler = _JSONMETHODS.get(method, None)
    handler = _JSONMETHODS.get(method)
    if not handler:
        ret_dict['error'] = 'unknown method'
        return json.dumps(ret_dict)

    # todo:
    # fix calling function explicitly.

    try:
        ret_dict['result'] = handler(*params)
    except:
        traceback.print_exc(file=sys.stdout)
        ret_dict['result'] = None
        ret_dict['error'] = "%s:%s" % (sys.exc_type, sys.exc_value)
    finally:
        return ret_dict
