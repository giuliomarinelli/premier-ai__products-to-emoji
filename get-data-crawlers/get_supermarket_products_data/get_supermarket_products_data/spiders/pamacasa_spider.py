import scrapy


class PamacasaSpider(scrapy.Spider):
    name = "pamacasa"
    start_urls = [
        "https://pamacasa.pampanorama.it/spesa-consegna-domicilio/10149?changingStore=true"
    ]

    def parse(self, response):
        for category in response.css('a[class^="columns__item-cat"]'):
            category_url = response.urljoin(category.css("::attr(href)").get())
            category_name = category.css("small::text").get().strip()
            yield scrapy.Request(
                category_url,
                callback=self.parse_category,
                meta={"category_name": category_name if (category_name) else "Unknown"},
            )

    def parse_category(self, response):           
        category_name = response.meta.get('category_name', "Unknown") 
        for product in response.css('section[class^="product_"]'):
            yield {
                "name": product.css("::attr(title)").get(default='N/A').strip().lower(),
                "category": category_name
            }

