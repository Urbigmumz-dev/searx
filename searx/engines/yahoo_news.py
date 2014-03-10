#!/usr/bin/env python

from urllib import urlencode
from lxml import html
from searx.engines.xpath import extract_text, extract_url
from searx.engines.yahoo import parse_url

categories = ['news']
search_url = 'http://news.search.yahoo.com/search?{query}&b={offset}'
results_xpath = '//div[@class="res"]'
url_xpath = './/h3/a/@href'
title_xpath = './/h3/a'
content_xpath = './/div[@class="abstr"]'
suggestion_xpath = '//div[@id="satat"]//a'

paging = True


def request(query, params):
    offset = (params['pageno'] - 1) * 10 + 1
    if params['language'] == 'all':
        language = 'en'
    else:
        language = params['language'].split('_')[0]
    params['url'] = search_url.format(offset=offset,
                                      query=urlencode({'p': query}))
    params['cookies']['sB'] = 'fl=1&vl=lang_{lang}&sh=1&rw=new&v=1'\
        .format(lang=language)
    return params


def response(resp):
    results = []
    dom = html.fromstring(resp.text)

    for result in dom.xpath(results_xpath):
        url = parse_url(extract_url(result.xpath(url_xpath), search_url))
        title = extract_text(result.xpath(title_xpath)[0])
        content = extract_text(result.xpath(content_xpath)[0])
        results.append({'url': url, 'title': title, 'content': content})

    if not suggestion_xpath:
        return results

    for suggestion in dom.xpath(suggestion_xpath):
        results.append({'suggestion': extract_text(suggestion)})

    return results