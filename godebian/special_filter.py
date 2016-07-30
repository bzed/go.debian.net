from __future__ import print_function

# key,value = char, char to be replaced
_special_chars = {"%2B": "XXYYZZ"}


def pre_filter(url):
    url = url.encode('utf-8')
    assert type(url) is str, "Url must be string"
    for key, value in _special_chars.items():
        if key in url:
            url = url.replace(key, value)
    return unicode(url, "utf-8")


def post_filter(url):
    url = url.encode('utf-8')
    assert type(url) is str, "url must be string"
    for key, value in _special_chars.items():
        if value in url:
            url = url.replace(value, key)
    return unicode(url, "utf-8")


def special_filter_test(urls=[]):
    for url in urls:
        resp = pre_filter(url=url)
        print(resp)
        resp2 = post_filter(url=resp)
        print(resp2)


if __name__ == '__main__':
    special_filter_test(urls=[
        "http://www.example.com/?q=foo%2Bbar"
    ])
