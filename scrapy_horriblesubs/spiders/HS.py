# -*- coding: utf-8 -*-
import re

import scrapy


class HSSpider(scrapy.Spider):
    name = 'hsubs'
    allowed_domains = ['horriblesubs.info']

    default_start_url = 'https://horriblesubs.info/shows/one-punch-man-s2//'
    start_urls = []
    title = ""

    script_marker = "hs_showid"
    script_regex = r".*?hs_showid\s?=\s?(\d*)"
    getshow_link = "https://horriblesubs.info/api.php?method=getshows&type=show&showid={}"

    getshow_link_with_id = ""
    next_id = 0

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)

        if 'url' in kwargs and 'title' in kwargs:
            self.start_urls.append(kwargs['url'])
            self.title = kwargs['title']
        else:
            self.start_urls.append(self.default_start_url)
            self.title = "hsubs"

    def parse(self, response):
        scripts = [x for x in response.xpath(
            ".//script/text()").getall() if self.script_marker in x]
        if len(scripts) > 0:
            match = re.match(self.script_regex, scripts[0])
            if match:
                print("Anime id : " + match[1])
                print("Retrieving links", end='')
                self.getshow_link_with_id = self.getshow_link.format(match[1])
                return scrapy.Request(url=self.getshow_link_with_id, callback=self.getshow_callback)

    def getshow_callback(self, response):
        try:
            if response.text == "DONE":  # no more
                print("\nDone")
                return
            print(".", end='')
            magnets = {"title": self.title}
            episodes = response.xpath(
                ".//div[has-class('rls-info-container')]")

            for ep in episodes:
                link = self.get_link(ep)
                ep_id = ep.attrib['id']
                magnets[ep_id] = link

            yield magnets

            self.next_id += 1
            yield scrapy.Request(url=self.getshow_link_with_id + "&nextid={}".format(self.next_id),
                                 callback=self.getshow_callback)

        # for debug
        except Exception as e:
            print(repr(e))
            pass

    def get_link(self, ep):
        selector = ep.xpath(
            ".//div[has-class('link-720p')]//span[has-class('hs-magnet-link')]//a")
        if 'href' in selector.attrib:
            return selector.attrib['href']

        selector = ep.xpath(
            ".//div[has-class('link-360p')]//span[has-class('hs-magnet-link')]//a")
        if 'href' in selector.attrib:
            return selector.attrib['href']

        return ""
