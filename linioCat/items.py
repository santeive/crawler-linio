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

def clean_category(clean_category):
    clean_category = clean_category.replace('/','|')
    return clean_category

def clean_percentage(ls):

    porcentaje = 100 - ( (ls['special_price'])*(100)/(ls['price']) )
    return int(porcentaje)

def clean_image(image):
    image = 'http:'+ image
    return image



class LiniocatItem(scrapy.Item):
    # define the fields for your item here like:

    sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    category = scrapy.Field(
        input_processor=MapCompose(clean_category),
        output_processor=TakeFirst()
    )
    seller = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(clean_description),
        output_processor=TakeFirst()
    )
    brand = scrapy.Field(
        output_processor=TakeFirst()
    )
    image = scrapy.Field(
        input_processor=MapCompose(clean_image),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    stock = scrapy.Field(
        input_processor=MapCompose(clean_stock),
        output_processor=TakeFirst()
    )
    discount = scrapy.Field(
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        output_processor=TakeFirst()
    )
    percentage = scrapy.Field(
        input_processor=MapCompose(clean_percentage),
        output_processor=TakeFirst()
    )
    date = scrapy.Field(
        output_processor=TakeFirst()
    )