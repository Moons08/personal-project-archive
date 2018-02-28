# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class MetacrawlerPipeline(object):
    def __init__(self):
        self.csvwriter = csv.writer(open("meta.csv", "w"))
        self.csvwriter.writerow(["date", "title", "metascore", "userscore"])

    def process_item(self, item, spider):
        row = []
        if abs(int(item["metascore"])-float(item["userscore"])*10) >20:
            row.append(item["date"])
            row.append(item["title"])
            row.append(item["metascore"])
            row.append(item["userscore"])
            self.csvwriter.writerow(row)
        return item
