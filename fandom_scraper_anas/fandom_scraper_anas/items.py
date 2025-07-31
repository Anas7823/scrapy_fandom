import scrapy

class GameItem(scrapy.Item):
    type = scrapy.Field(default="game")
    url = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    attributes = scrapy.Field()
    personnages = scrapy.Field()

class CharacterItem(scrapy.Item):
    type = scrapy.Field(default="character")
    url = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    attributes = scrapy.Field()
    game = scrapy.Field()

