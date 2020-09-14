from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy
import re

def clean_stock(stock):
    if stock == "Añadir al carrito":
        stock = "Disponible"
    else:
        stock = "Agotado"
    return stock

def clean_description(descripcion):
    return descripcion

def clean_percentage(porcentaje):
    if len(porcentaje) == 0:
        porcentaje = "No aplica"
    return porcentaje


class LiniocatItem(scrapy.Item):
    # define the fields for your item here like:

    sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )

    category = scrapy.Field(
        output_processor=TakeFirst()
    )
    seller = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field()

    brand = scrapy.Field(
        output_processor=TakeFirst()
    )
    image = scrapy.Field(
        output_processor=TakeFirst()
    )
    months = scrapy.Field(
        output_processor=TakeFirst()
    )
    link = scrapy.Field(
        output_processor=TakeFirst()
    )
    stock = scrapy.Field(
        output_processor=TakeFirst()
    )
    discount = scrapy.Field(
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        output_processor=TakeFirst()
    )
    percentage = scrapy.Field(
        output_processor=TakeFirst()
    )
    date = scrapy.Field(
        output_processor=TakeFirst()
    )