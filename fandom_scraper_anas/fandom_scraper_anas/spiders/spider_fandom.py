import scrapy
from fandom_scraper_anas.items import GameItem, CharacterItem

class SpiderFandom(scrapy.Spider):
    name = "fandom"
    start_urls = [
        "https://reddead.fandom.com/wiki/Red_Dead_Redemption_2",
        "https://nfs.fandom.com/wiki/Need_for_Speed:_Unbound",
        "https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki",
        "https://detroit-become-human.fandom.com/wiki/Detroit:_Become_Human",
        "https://gta.fandom.com/wiki/Grand_Theft_Auto_V"
    ]
    
    custom_settings = {
        
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 30000,
        "FEEDS": {
            "../data/fandom_data.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
    }

    visited_characters = set()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"playwright": True}
            )

    def parse(self, response):
        self.logger.info(f"Visiting game page: {response.url}")
        # game_name = response.css("h1#firstHeading::text").get()
        game_name = response.css("h1.page-header__title, h1#firstHeading").xpath(".//text()").getall()
        game_name = " ".join([n.strip() for n in game_name if n.strip()])

        image_url = response.css(".portable-infobox img::attr(src), .infobox img::attr(src)").get()
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        description = " ".join(response.css(".mw-parser-output > p::text").getall()).strip()

        attributes = {}
        for row in response.css(".portable-infobox .pi-item, .infobox tr"):
            label = row.css(".pi-data-label::text, th::text").get()
            value = row.css(".pi-data-value *::text, td *::text").getall()
            if label and value:
                attributes[label.strip()] = " ".join([v.strip() for v in value if v.strip()])

        yield GameItem(
            url=response.url,
            name=game_name,
            image=image_url,
            description=description,
            attributes=attributes
        )

        character_links = set()
        for link in response.css("a::attr(href)").getall():
            if not link.startswith("/wiki/") or ':' in link:
                continue

            full_url = response.urljoin(link)
            if full_url in self.visited_characters:
                continue

            # Détection améliorée
            if any(word in full_url.lower() for word in ["character", "personnage", "protagonist", "villain"]):
                self.visited_characters.add(full_url)
                character_links.add(full_url)

        for link in character_links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_character,
                meta={"playwright": True}
            )

    def parse_character(self, response):
        self.logger.info(f"Visiting character page: {response.url}")

        # name = response.css("h1.page-header__title::text").get()
        # name = response.css("h1.page-header__title *::text").getall()
        name = response.css("h1.page-header__title, h1#firstHeading").xpath(".//text()").getall()
        name = " ".join([n.strip() for n in name if n.strip()])

        image_url = response.css(".portable-infobox img::attr(src), .infobox img::attr(src)").get()
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        description = " ".join(response.css(".mw-parser-output > p::text").getall()).strip()

        attributes = {}
        for row in response.css(".portable-infobox .pi-item, .infobox tr"):
            label = row.css(".pi-data-label::text, th::text").get()
            value = row.css(".pi-data-value *::text, td *::text").getall()
            if label and value:
                attributes[label.strip()] = " ".join([v.strip() for v in value if v.strip()])

        if not name or not image_url or not image_url.startswith("http"):
            self.logger.warning(f"[SKIP] {response.url} - no image or name")
            return

        yield CharacterItem(
            url=response.url,
            name=name,
            image=image_url,
            description=description,
            attributes=attributes
        )

    def closed(self, reason):
        import os
        if not os.path.exists("logs"):
            os.makedirs("logs")
        with open("logs/report.md", "w", encoding="utf-8") as f:
            f.write(f"# Rapport de scraping\n\n")
            f.write(f"- Statut : `{reason}`\n")
            f.write(f"- Pages personnages uniques visitées : {len(self.visited_characters)}\n")

