import scrapy
from scrapy.linkextractors import LinkExtractor
import csv
import time
import json
import calendar
from datetime import datetime, date
from ..items import LiniocatItem

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
	name = 'liniobench'
	allowed_domains = ["www.linio.com.mx"]	
	#Corremos así
	# scrapy crawl liniobench -o linioItemsFinal.csv -t csv

	#Vamos a seguir a este link
	#//div[@class="catalogue-list"]/ul/li/a/@href
	def start_requests(self):

		urls = main()
		for i in urls:
			yield scrapy.Request(url=i, callback=self.parse_dir_contents)


		#Mandar mensaje de 'TERMINAMOS'
		

	#Funcion que hace click en el link dada una página (2)
	def parse_dir_contents(self, response):
		#Next page
		items = LiniocatItem()

		#Info del producto
		data = re.findall("var dataLayer =(.+?);\n", response.body.decode("utf-8"), re.S)
		# print("Esto es lo que tengo")
		# print(data)

		# print("")
		ls = []
		if data:
			ls = json.loads(data[0])
		
		if ls:
			# Info del producto
			nombre    = ls[0]["product_name"]
			original  = ls[0]["price"]
			descuento = ls[0]["special_price"]
			categoria = ls[0]["category_full"] 
			sku 	  = ls[0]["sku_config"]
			marca 	  = ls[0]["brand"]
			vendedor  = ls[0]["seller_name"]

			porcentaje = response.xpath('(//span[@class="discount"])[last()]/text()').extract()
			if len(porcentaje) == 0:
				porcentaje = "No aplica"

			envio = response.xpath('//div[@class="item-shipping-estimate-title"]/text()').extract()
			if len(envio) == 0:
				envio = "No aplica"

			status = response.xpath('normalize-space(//button[@id="buy-now"][1]/text())').extract()
			if status == "Añadir al carrito":
				status = "Disponible"
			meses = response.xpath('normalize-space(//*[@id="usp-menu"]/div/div/a[5]/span[2]/text())').extract()
			descripcion = response.xpath('normalize-space(//div[@itemprop="description"] )').extract()
			url = response.xpath('//link[@rel="canonical"]/@href').extract()
			fecha = getFecha()

			items['sku']  = sku
			items['nombre'] = nombre
			items['original'] = original
			items['descuento'] = descuento
			items['porcentaje'] = porcentaje
			items['categoria'] = categoria
			items['marca'] = marca
			items['vendedor'] = vendedor
			items['status'] = status
			items['meses'] = meses
			items['descripcion'] = descripcion
			items['envio'] = envio
			items['link'] = url
			items['fecha'] = fecha

			yield items

			

