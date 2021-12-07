import scrapy


class NovelCategorySpider(scrapy.Spider):
    name = "novel_category"

    def start_requests(self):
        urls = ["http://www.quanshuxs.com/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.novel_categories)

    def novel_categories(self, response):
        novel_categories = []
        class_list = ["heads", "headz"]
        for class_item in class_list:
            categories = response.xpath("//td[@class='{}']/a".format(class_item))
            category_urls = response.xpath("//td[@class='heads']/a/@href")
            for i in range(1, len(categories)):
                novel_category = categories[i].xpath("text()").extract()[0]
                novel_category_url = category_urls[i].extract()
                novel_categories.append({"novel_category": novel_category, "novel_category_url": novel_category_url})
                yield scrapy.Request(
                    url=novel_category_url,
                    meta={"novel_category": novel_category, "novel_category_url": novel_category_url},
                    callback=self.novel_list_in_category
                )

        print(novel_categories)

    def novel_list_in_category(self, response):
        novel_category = response.meta["novel_category"]
        novel_category_url = response.meta["novel_category_url"]
        novel_list = {"novel_category": novel_category, "novel_category_url": novel_category_url, "novel_list": []}
        novels = response.xpath("//td[@class='m11']/a")
        novel_urls = response.xpath("//td[@class='m11']/a/@href")
        for n in range(len(novels)):
            novel_name = novels[n].xpath("text()").extract()
            novel_url = novel_urls[n].extract()
            novel_list["novel_list"].append({"novel_name": novel_name, "novel_url": novel_url})
        pages = response.xpath("//td[@class='mlist']/a/@href")
        for i in range(1, len(pages) - 2):
            next_novel_list_page_url = pages[i].extract()
            # yield scrapy.Request(url=next_novel_list_page_url, meta={"list": novel_list},
            #                      callback=self.next_page)
        print(next_novel_list_page_url)

    def next_page(self, response):
        novel_list = response.meta["list"]
        novels = response.xpath("//td[@class='m11']/a")
        novel_urls = response.xpath("//td[@class='m11']/a/@href")
        for n in range(len(novels)):
            # for n in range(len(novels)):
            novel_name = novels[n].xpath("text()").extract()
            novel_url = novel_urls[n].extract()
            novel_list["novel_list"].append({"novel_name": novel_name, "novel_url": novel_url})
        print(novel_list)
