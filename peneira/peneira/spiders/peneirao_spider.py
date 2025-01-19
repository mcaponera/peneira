from pathlib import Path

import scrapy


class PeneiraoSpider(scrapy.Spider):
    name = 'peneira'
    start_urls = [
            "https://portaldegovernanca.cbf.com.br/documentos-da-partida"
        ]
    
    def parse(self, response):
        years_ = response.xpath("//select[@id='ano']/option/text()").extract()
        years = [int(year) for year in years_ if year.isdigit()]

        for year in years:
            next_url = f"https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/{year}"
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_year,
                meta={'year': year}
            )

    def parse_year(self, response):
        year = response.meta['year']
        contests_ = json.loads(response.text)
        contests = contests_[1]