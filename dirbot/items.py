from scrapy.item import Item, Field


class Website(Item):

    station = Field()
    month = Field()
    day = Field()
    year = Field()
    time = Field()
    weather = Field()
    temperature = Field()
    dewpoint = Field()
    humidity = Field()
    winds = Field()

