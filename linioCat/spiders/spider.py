import scrapy
from scrapy.linkextractors import LinkExtractor
import csv
import time
import calendar
from datetime import datetime, date
from ..items import LiniocatItem

import requests
import os
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
		
		#Imprimimos la longitud de los items
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
	name = 'liniocat'
	allowed_domains = ["www.linio.com.mx"]	
	#Corremos así
	# scrapy crawl liniocat -o linioItemsFinal.csv -t csv

	#Vamos a seguir a este link
	#//div[@class="catalogue-list"]/ul/li/a/@href
	def start_requests(self):

		urls = main()

		for i in urls:
			yield scrapy.Request(url=i, callback=self.parse_dir_contents)

	#Funcion que hace click en el link dada una página (2)
	def parse_dir_contents(self, response):
		#Next page
		items = LiniocatItem()
		categoria = response.xpath('normalize-space(/html/body/div[3]/main/ol/li[3]/a/span/text())').extract()

		#Para la fecha de extracción
		x = datetime.now()
		x = datetime.now()
		dia = str(x.strftime("%d"))
		mes = str(x.strftime("%m"))
		anio = str(x.year)

		#Info del producto
		nombre = response.xpath('//div[@class="product-title col-xs-12"]/h1[@class="col-xs-12 col-md-9 col-lg-10"]/span/text()').extract()
		original = response.xpath('//div[@class="product-price"]/div[@class="product-price-container option-container option-1 "]/span[@class="original-price"]/text()').extract()
		descuento = response.xpath('normalize-space(//*[@id="display-zoom"]/div[1]/div[1]/div[1]/div/div/div/span/text())').extract()
		porcentaje = response.xpath('//div[@class="product-price"]/div[@class="product-price-container option-container option-1 "]/span[@class="discount"]/text()').extract()
		vendedor = response.xpath('normalize-space(//div[@class="seller-information product-bg-container"]/a/text())').extract()
		status = response.xpath('normalize-space(//button[@id="buy-now"][1]/text())').extract()
		marca = response.xpath('//div[@class="product-subtitle col-xs-12 col-md-9 col-lg-12"]/div/a[@itemprop="brand"]/text()').extract()
		envio = response.xpath('normalize-space(//div[@class="item-shipping-estimate-title"]/text())').extract()
		meses = response.xpath('normalize-space(//*[@id="usp-menu"]/div/div/a[5]/span[2]/text())').extract()
		descripcion = response.xpath('normalize-space(//span[@itemprop="description"]/text())').extract()
		url = response.xpath('//link[@rel="canonical"]/@href').extract()
		fecha = dia + '-' + mes + '-' + anio

		items['categoria'] = categoria
		items['nombre'] = nombre
		items['original'] = original
		items['descuento'] = descuento
		items['porcentaje'] = porcentaje
		items['marca'] = marca
		items['vendedor'] = vendedor
		items['status'] = status
		items['meses'] = meses
		items['descripcion'] = descripcion
		items['envio'] = envio
		items['link'] = url
		items['fecha'] = fecha

		yield items

