from __future__ import print_function
import requests
import json
import unittest

__author__ = 'Harsh Daftary'
_host = "http://127.0.0.1:5000/"


class ApiError(Exception):
    pass


class GoDebianApi(object):

    def __init__(self, host=_host):
        """
        :param host: by default it will use go.debian.net for generating preview and short urls
        use host = http://deb.li/ if you want in that format
        json api url is deb.li/rpc/json

        if you want to change it then subclass this class and override __init__ to make your changes.
        :return None
        """
        self.api_url = _host + "rpc/json"
        self.host = host
        self.headers = {'Content-type': 'application/json'}

    def dispatch_req(self, method, *args, **kwargs):
        data = {'method': method, 'params': args, 'id': "jsonrpc"}
        # print(data)
        r = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        # print(r.status_code)

        if r.status_code == 200:
            resp = r.json()
            # print(resp)
            if resp.get('result', False):
                return resp.get('result')
            else:
                # print(resp)
                raise ApiError(resp.get('error', "Some error occurred"))
        else:
            raise ApiError(
                "May be your host is not whitelisted in the api, visit https://wiki.debian.org/deb.li for more details.")

    def add_url(self, url):
        """
        :param url: Provides shortened link for given URL
                    repeated URLs don't get different Keys.
        :return str: shortened URL
        """
        return self.dispatch_req("add_url", url)

    def get_url(self, key):
        """
        :param key: Enter the key to get associated URL
        Get key from following format : http://deb.li/p/<key>
        :return str: URL associated
        """
        return self.dispatch_req("get_url", key)

    def add_static_url(self, url, keyword):
        """
        :param url: Url to be shortened
        :param keyword: Static keyword against which url needs to be stored
        example : go.debian.net/<keyword>
        :return:
        """
        return self.dispatch_req("add_static_url", url, keyword)


def dependency_check():
    try:
        import sqlalchemy
        import memcache
        import psycopg2
        import flask
        import IPy
        import json
        import requests
        import sqlite3
        import inspect
        return True
    except Exception as e:
        print(e)
        return False


class BaseTest(unittest.TestCase):
    urls = ["http://www.debian.net",
            "http://www.gmail.com",
            "http://www.facebook.com",
            "http://999fitness.com",
            "http://a.update.51edm.net",
            "http://ab.usageload32.com",
            "http://abcdespanol.com",
            "http://above.e - rezerwacje24.pl",
            "http://absurdity.flarelight.com",
            "http://achren.org",
            "http://acool.csheaven.com",
            "http://ad - beast.com",
            "http://adgallery.whitehousedrugpolicy.gov",
            "http://adlock. in",
            "http://adobeflashupdate14.com",
            "http://ads.wikipartes.com",
            "http://adserving.favorit-network.com",
            "http://adv.riza.it",
            "http://advancetec.co.uk",
            "http://afa15.com.ne.kr",
            "http://agsteier.com",
            "http://aintdoinshit.com",
            "http://aippnetworks.com",
            "http://aircraft.evote.cl",
            "http://ajewishgift.com",
            "http://akirkpatrick.com",
            ]
    percent_encoded_url = ["http://www.example.com/?q=foo%2Bbar",
                           "http://www.example2.com/?q=foo+bar",
                           'http://1.1.1.6/@#/index.htm',
                           'http://1.1.1.6/@#/dsds/index?$/user=2121l',
                           'http://1.1.1.5/?foo=index.htm&sda=12&dsdsd/asdsd/url',
                           'http://1.1.1.5/?&sda=12&dsdsd/asdsd/url'
                           ]
    static_urls = [dict(url="http://www.debian.org", keyword="somekey")]

    api = GoDebianApi()

    def test_dependencies(self):
        self.assertTrue(dependency_check(), msg="Dependencies not satisfied")

    def test_non_static_urls(self):
        for i in self.urls:
            self.assertEqual(i,self.api.get_url(key=self.api.add_url(url=i)), msg="Problem in adding & getting URL API")

    def test_static_urls(self):
        for i in self.static_urls:
            self.api.add_static_url(url=i["url"], keyword=i["keyword"])
            self.assertEqual(i["url"],self.api.get_url(key=i["keyword"]),msg="Problem in STATIC URL API")

    def test_percent_encoded_urls(self):
        for i in self.percent_encoded_url:
            self.assertEqual(i,self.api.get_url(key=self.api.add_url(url=i)), msg="Problem in PERCENT ENCODED URL API")

if __name__ == '__main__':
    """
    Basic output of tests
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 1.443s

    OK
    """
    unittest.main()