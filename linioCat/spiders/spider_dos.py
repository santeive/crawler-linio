import scrapy
import time
import json
from datetime import datetime, date
from ..items import LiniocatItem

from scrapy.loader import ItemLoader
from scrapers.items import ProductItem

import requests
import os
import re
from urllib.request import urlopen
import urllib.request
import xml.etree.ElementTree as ET

def getFecha():
	#Traemos la fecha
	x = datetime.now()

	dia = str(x.strftime("%d"))
	mes = str(x.strftime("%m"))
	anio = str(x.year)

	return dia + '_' + mes + '_' + anio

def getName(count):
	#Traemos la fecha
	x = datetime.now()

	dia = str(x.strftime("%d"))
	mes = str(x.strftime("%m"))
	anio = str(x.year)
	hora = str(x.strftime("%H"))

	return 'sitemap.' + str(count) + '_'+ dia + '_' + mes + '_' + anio

def loadSitemap(sitemapList):

	count = 0
	listNames = []
	for s in sitemapList :
		resp = requests.get(s)
		name = getName(count) + ".xml"
		with open(name, 'wb') as f:
			f.write(resp.content)
		listNames.append(name)
		count += 1

	return listNames

def loadRRS():
	url = 'https://www.linio.com.mx/sitemap.xml'
	
	resp = requests.get(url)
	date = "Linio_" + getFecha() + '.xml'

	with open(date, 'wb') as f:
		f.write(resp.content)

	return date

def parseXML(xmlFile):
	#Creamos el arbol
	tree = ET.parse(xmlFile)
	#Obtenemos la raiz
	root = tree.getroot()

	#Lista de almacenamiento
	listaP = []

	#Almacenamos aqui los items
	for movie in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
			link = movie.text 
			#print(link)
			listaP.append(link)
	return listaP

def downloadUrl(listNames):
	listUrl = []
	for li in listNames:
		tree = ET.parse(li)

		root = tree.getroot()

		for r in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
			link = r.text
			listUrl.append(link)
		
	return listUrl

def main():
	#Cargamos la URL del XML
	date = loadRRS()

	#Descargamos cada uno de los URLS
	xmlLinio = parseXML(date)

	#Descargamos cada link
	listNames = loadSitemap(xmlLinio)

	#Leemos todos los xml y los guardamos en una lista y leer todos los links
	return downloadUrl(listNames)

class LinioCat(scrapy.Spider):
	name = 'liniobench'
	allowed_domains = ["www.linio.com.mx"]	

	def start_requests(self):

		urls = main()
		for i in urls:
			yield scrapy.Request(url=i, callback=self.parse_dir_contents, meta={'url':i})

	def parse_dir_contents(self, response):
		loader = ItemLoader(item=LiniocatItem(), response=response)

		#Extract from datalayer
		data = re.findall("var dataLayer =(.+?);\n", response.body.decode("utf-8"), re.S)
		
		descripcion = response.xpath('normalize-space(//div[@itemprop="description"] )').extract()
		porcentaje = response.xpath('(//span[@class="discount"])[last()]/text()').extract()
		stock = response.xpath('normalize-space(//button[@id="buy-now"][1]/text())').extract()
		months = response.xpath('normalize-space(//*[@id="usp-menu"]/div/div/a[5]/span[2]/text())').extract()

		ls = []
		if data:
			ls = json.loads(data[0])

		loader.add_value("sku", ls[0]["sku_config"])
		loader.add_value("name", ls[0]["product_name"])
		loader.add_value("category", ls[0]["category_full"])
		loader.add_value("seller", ls[0]["seller_name"])
		loader.add_value("description", descripcion)
		loader.add_value("brand", ls[0]["brand"])
		loader.add_value("image", ls[0]["small_image"])
		
		loader.add_value("months", months)
		loader.add_value("link", response.meta.get('url'))
		loader.add_value("stock", stock)
		loader.add_value("discount", ls[0]["special_price"])
		loader.add_value("price", ls[0]["price"])
		loader.add_value("percentage", porcentaje)
		loader.add_value("date", getFecha())

		return loader.load_item()