# -*- coding: utf-8 -*-
__author__ = "Michael Fogleman, Bernd Zeimetz"
__contact__ = "bzed@debian.org"
__credits__ = ['http://www.michaelfogleman.com/2009/09/python-short-url-generator/']
__license__ = """
Copyright (C) 2009 Michael Fogleman
Copyright (C) 2010 Bernd Zeimetz <bzed@debian.org>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from .config import UrlencoderConfig
DEFAULT_ALPHABET = UrlencoderConfig.alphabet
DEFAULT_BLOCK_SIZE = UrlencoderConfig.blocksize

class UrlEncoder(object):
    def __init__(self, alphabet=DEFAULT_ALPHABET, block_size=DEFAULT_BLOCK_SIZE):
        self.alphabet = alphabet
        self.block_size = block_size
        self.mask = (1 << block_size) - 1
        self.mapping = range(block_size)
        self.mapping.reverse()
    def encode_url(self, n, min_length=0):
        return self.enbase(self.encode(n), min_length)
    def decode_url(self, n):
        return self.decode(self.debase(n))
    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)
    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result
    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)
    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result
    def enbase(self, x, min_length=0):
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)
    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self.enbase(x/n) + self.alphabet[x%n]
    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n**i)
        return result
        
DEFAULT_ENCODER = UrlEncoder()

def encode(n):
    return DEFAULT_ENCODER.encode(n)
    
def decode(n):
    return DEFAULT_ENCODER.decode(n)
    
def enbase(n, min_length=0):
    return DEFAULT_ENCODER.enbase(n, min_length)
    
def debase(n):
    return DEFAULT_ENCODER.debase(n)
    
def encode_url(n, min_length=0):
    return DEFAULT_ENCODER.encode_url(n, min_length)
    
def decode_url(n):
    return DEFAULT_ENCODER.decode_url(n)


