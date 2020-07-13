# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LiniocatItem(scrapy.Item):
    # define the fields for your item here like:
    sku = scrapy.Field()
    categoria = scrapy.Field()
    nombre = scrapy.Field()
    original = scrapy.Field()
    descuento = scrapy.Field()
    porcentaje = scrapy.Field()
    marca = scrapy.Field()
    vendedor = scrapy.Field()
    status = scrapy.Field()
    meses = scrapy.Field()
    descripcion = scrapy.Field()
    envio = scrapy.Field()
    link = scrapy.Field()
    fecha = scrapy.Field()
