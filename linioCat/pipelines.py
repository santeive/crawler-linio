from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from database_setup import engine
from models import Linio, LinioProductPrice

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
		self.exporter.fields_to_export = ["sku", "name", "price", "discount", "percentage", "brand", "seller", "category", "stock", "description", "link", "date"]
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()
	
	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item

class StoragePipeline(object):

	def __init__(self, db_engine=engine) -> None:
		self.engine = db_engine

	def open_spider(self, spider):
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def close_spider(self, spider):
		self.session.close()

	def process_item(self, item, spider):
		
		linio = Linio()
		linio = (
			self.session.query(Linio)
			.filter_by(sku=item["sku"])
			.first()
		)

		if linio is None:
			linio = Linio(sku=item["sku"])

		linio.sku = item["sku"]
		linio.name = item["name"]
		linio.category = item["category"]
		linio.seller = item["seller"]
		linio.description = item["description"]
		linio.brand = item["brand"]
		linio.image_url = item["image"]
		linio.url = item["url"]

		self.session.add(linio)
		self.session.commit()

		# Check if the BranchProduct already exists
		price_product = (
			self.session.query(LinioProductPrice)
			.filter_by(linio=linio, price=item["price"])
			.first()
		)

		if price_product is None:
			price_product = LinioProductPrice(linio=linio, price=item["price"])

		price_product.stock = item["stock"]
		price_product.discount = item["discount"]
		price_product.price = item["price"]
		price_product.percentage = item["percentage"]
		price_product.date = item["date"]

		self.session.add(price_product)
		self.session.commit()

		return item