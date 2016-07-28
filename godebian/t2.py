from __future__ import print_function
__author__ = 'Harsh Daftary'

try:
    import requests
    import json
    import inspect

except ImportError as e:
    print(e)
    exit(1)

from functools import wraps

class ApiError(Exception):
    pass


class GoDebianApi(object):

    def __init__(self, host="http://127.0.0.1:5000/"):
        """
        :param host: by default it will use go.debian.net for generating preview and short urls
        use host = http://deb.li/ if you want in that format
        json api url is deb.li/rpc/json
        if you want to change it then subclass this class and override __init__ to make your changes.

        :return None
        """
        self.api_url = "http://deb.li/rpc/json"
        self.host = host
        self.preview = host + "p/%s"
        self.headers = {'Content-type': 'application/json'}

    def _api_call(func):

        @wraps(func)
        def _tmp(self, *args, **kwargs):
            print(args)
            function_name = func.__name__

            data = {'method': function_name, 'params': args, 'id': "jsonrpc"}
            print(data)
            r = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
            #print(r.status_code)

            if r.status_code == 200:
                resp = r.json()
                print(resp)
                if resp.get('result', False):
                    return self.host + resp.get('result')
                else:
                    raise ApiError(resp.get('error', "Some error occurred"))
            else:
                raise ApiError("May be your host is not whitelisted in the api, visit https://wiki.debian.org/deb.li for more details.")
        return _tmp


    @_api_call
    def add_url(self, url):
        """
        :param url: Provides shortened link for given URL
                    repeated URLs don't get different Keys.
        :return str: shortened URL
        """
        pass

    def get_preview_url(self, key):
        """
        :param key: Returns preview URL for provided key
        :return str
        """
        return self.preview % key

    @_api_call
    def get_url(self, key):
        """
        :param key: Enter the key to get associated URL
        Get key from following format : http://deb.li/p/<key>
        :return str: URL associated
        """
        pass

    @_api_call
    def add_static_url(self, url, keyword):
        """
        :param url: Url to be shortened
        :param keyword: Static keyword against which url needs to be stored
        example : go.debian.net/<keyword>
        :return:
        """
        pass

    @_api_call
    def update_static_url(self, url, keyword):
        """
        :param url: new url
        :param keyword: Static keyword against which url needs to be stored
        example : go.debian.net/<keyword>
        :return:
        """

urls = ["www.debian.net","www.gmail.com","www.facebook.com"]
static_urls = [dict(url="http://www.debian.org",id="debian23")]


class BaseTest(object):
    api = GoDebianApi()

    def test_non_static_urls(self):
        for i in urls:
            key = self.api.add_url(url=i)
            url = self.api.get_url(key=key)
            assert url == i, "Error"

    def test_static_urls(self):
        for i in static_urls:
            self.api.add_static_url(url=i["url"],keyword=i["id"])
            url = self.api.get_url(key=i["id"])
            assert url == i["url"], "Error"

if __name__ == '__main__':
    test = BaseTest()
    test.test_static_urls()
    test.test_non_static_urls()
