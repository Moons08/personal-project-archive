# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CrawlerPipeline(object):
    def __init__(self):
        # self.csvwriter = csv.writer(open("user_review.csv", "w"))
        self.csvwriter = csv.writer(open("critic_review.csv", "w"))
        self.csvwriter.writerow(["title", "id", "score", "review"])

    def process_item(self, item, spider):
        row = []
        row.append(item["title"])
        row.append(item["id"])
        row.append(item["score"])
        row.append(item["review"])
        self.csvwriter.writerow(row)
        return item
