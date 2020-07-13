# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import calendar
from datetime import datetime, date
from scrapy.exporters import CsvItemExporter

def getFecha():
	x = datetime.now()
	dia = str(x.strftime("%d"))
	mes = str(x.strftime("%m"))
	anio = str(x.year)
	date = dia + '-' + mes + '-' + anio
		
	return date


class LiniocatPipeline(object):

	def __init__(self):
		date = getFecha()
		fileName = "linio-" + date + ".csv"
		
		self.file = open(fileName, 'wb')
		self.exporter = CsvItemExporter(self.file, str)
		self.exporter.fields_to_export = ["sku", "nombre", "original", "descuento", "porcentaje", "marca", "vendedor", "categoria", "status", "meses", "descripcion", "envio", "link", "fecha"]
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()
	
	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
