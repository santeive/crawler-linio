import scrapy
import time
import json
from datetime import datetime, date
from ..items import LiniocatItem
from scrapy.loader import ItemLoader
from .xml_maps import main, getFecha
import re

class LinioCat(scrapy.Spider):
	name = 'liniobench'
	allowed_domains = ["www.linio.com.mx"]	

	def start_requests(self):

		#urls = main()
		urls = [
			"https://www.linio.com.mx/p/dorado-u-nico-adulto-impermeable-adhesivo-pegatinas-de-tatuajes-temporales-de-belleza-belleza-multi-color-mezclado-v9jqkd",
			"https://www.linio.com.mx/p/vajilla-de-pajitas-de-bambu-natural-de-1-par-para-la-fiesta-de-cumplea-wyecfk",
			"https://www.linio.com.mx/p/sg906-gps-5g-wifi-fpv-con-selfie-plegable-4-k-1080-p-hd-ca-mara-drone-rc-drone-quadcopter-rtf-del-xs809s-xs809hw-sg106-blanco--vbjesv",
			"https://www.linio.com.mx/p/meeting-love-beach-pool-play-ball-inflable-nin-os-pvc-multicolor-summer-n2ymjm",
			"https://www.linio.com.mx/p/kit-de-herramientas-manhattan-530217-s0h8e2",
			"https://www.linio.com.mx/p/metal-fidget-hand-tri-spinner-finger-gro-ceramic-ball-toy-e-tmqa53",
			"https://www.linio.com.mx/p/fibra-de-polie-ster-fitness-deportes-tobillo-soporte-guardia-gimnasio-t-lea2a1",
			"https://www.linio.com.mx/p/10-pcs-9h-25d-tempered-glass-film-para-galaxy-j2-2016--yp238g",
			"https://www.linio.com.mx/p/e-aplica-al-mercedes-clase-s-w222-s350-s400-s500-may-bach-amg-14-17-tn64bg",
			"https://www.linio.com.mx/p/funda-para-tablet-resistente-a-los-golpes-con-soporte-y-colgante-para-samsung-galaxy-tab-a-a6-10-1-2016-t580-t585-sm-t585-t580n-funda-pen-n13lsj",
			"https://www.linio.com.mx/p/type-c-para-hd-hdmi-cable-usb-31-a-hdmi-cable-de-conexio-n-de-la-li-nea-de-proyeccio-n-de-tv-hd-vd5r36",
			"https://www.linio.com.mx/p/topsky-doble-fila-colgante-10-ganchos-estante-portavasos-organizador-s26wyv",
			"https://www.linio.com.mx/p/android-100-nueva-red-smart-tv-box-tv-boxh313-decodificador-rentable-ldmiah",
			"https://www.linio.com.mx/p/1-par-ajustable-claro-mujer-ropa-interior-invisible-bra-set-correas-para-el-hombro-tnc56p",
			"https://www.linio.com.mx/p/alfombrilla-de-rato-n-para-juegos-extra-grande-la-alfombrilla-antideslizante-alfombrilla-rato-n-patro-n-flamingo-n2zz79",
			"https://www.linio.com.mx/p/1-16-especificacio-n-del-juguete-del-coche-rc-de-alta-velocidad-con-tra-tnz3j1",
			"https://www.linio.com.mx/p/vestido-informal-holgado-de-manga-corta-con-cuello-redondo-para-mujer-de-estilo-casual-wt-rojo--lcxy02",
			"https://www.linio.com.mx/p/para-samsung-galaxy-a5-2016-a510-con-incrustaciones-de-diamante-electrochapado-espejo-cubierta-protectora-caso-con-anillo-oculta-titular-oro--n35w93",
			"https://www.linio.com.mx/p/er-360-lecho-n-soporte-de-ducha-cromo-plata-n0t972",
			"https://www.linio.com.mx/p/pensamientos-para-surgir-lhg4tx",
			"https://www.linio.com.mx/p/altavoz-bluetooth-resistente-al-agua-para-bicicletas-al-aire-libre-porta-til-subwoofer-altavoces-lan-rypkn5",
			"https://www.linio.com.mx/p/can-a-de-pescar-eva-handle-building-vd2vpo",
			"https://www.linio.com.mx/p/corto-y-flexible-porta-til-de-emergencia-micro-usb-cable-de-carga-y-sincronizacio-n-de-datos-blanco-n43nec",
			"https://www.linio.com.mx/p/cortinas-de-ventana-tratamientos-animal-lindo-zorro-dormir-profundo-divertido-170-200cm-lhsr8h",
			"https://www.linio.com.mx/p/bolsa-de-cosme-ticos-con-estampado-impermeable-de-pug-bonito-deanfun--v9ly1g",
			"https://www.linio.com.mx/p/-envi-o-gratis-flash-deal-12-li-neas-nivel-la-ser-3d-autonivelante-luz-qgfoed",
			"https://www.linio.com.mx/p/1-uds-mini-mu-ecas-originales-de-3-pulgadas-mga-mu-ecas-lalaloopsy-para-casa-yl8yib",
			"https://www.linio.com.mx/p/marca-camiseta-de-po-ker-juego-de-cartas-camisetas-de-juego-camise--qfoewh",
			"https://www.linio.com.mx/p/sensor-automa-tico-de-induccio-n-infrarroja-ahorro-de-agua-cocina-grifo-s3z69r",
			"https://www.linio.com.mx/p/reloj-deportivo-skmei-para-hombre-reloj-de-pulsera-militar-de-marca-de-lujo-relojes-digitales-analo-gicos-de-cuarzo-para-hombre-reloj-masculino-1391-rzxd1i",
			"https://www.linio.com.mx/p/batidora-inmersio-n-bikm-800-koblenz-n4o7e6",
			"https://www.linio.com.mx/p/funda-para-huawei-y6s-y6-2019-con-ranura-para-tarjeta-marro-n-oscuro-or8hk8",
			"https://www.linio.com.mx/p/organizador-de-pared-caja-de-almacenamiento-papeleri-a-caso-cosme-ticos-maquillaje-tenedor-multicolor-n2t2qg",
			"https://www.linio.com.mx/p/skmei-hombres-deportes-hombre-reloj-de-cuenta-atra-s-digital-de-moda-de-acero-inoxidable-reloj-resistente-al-agua-relojes-de-pulsera-hombre-reloj-relogio-masculino-tp8ytm",
			"https://www.linio.com.mx/p/cuentas-de-silicona-para-morder-de-12mm-envi-o-gratis-cuentas-de-denticio-n-de-silicona-para-mama-s-100-unids-lote-cuentas-de-silicona-para-mordedor-de-bebe-baby-rosado-fuc-n29py6",
			"https://www.linio.com.mx/p/contena-6229g-hot-style-reloj-de-pulsera-de-moda-para-mujer-relojes-para-mujer-marca-famosa-reloj-de-cuarzo-reloj-femenino-relogio-feminino-montre-femme-x2m2mc",
			"https://www.linio.com.mx/p/20pc-14mm-hexa-gono-de-silicona-mordedor-para-bebe-diy-para-cadena-de-chupete-de-grado-de-alimentos-perle-silicona-collar-denticio-n-bebe-para-los-nin-os-blanca-fuc-opt04m",
			"https://www.linio.com.mx/p/zivok-8013-correa-de-cuero-de-moda-reloj-de-oro-rosa-para-mujer-reloj-de-pulsera-de-cuarzo-creativo-para-amantes-ocasionales-vestido-de-mujer-relojes-de-lujo-para-mujer-vcoa8b",
			"https://www.linio.com.mx/p/contena-6229g-hot-style-reloj-de-pulsera-de-moda-para-mujer-relojes-para-mujer-marca-famosa-reloj-de-cuarzo-reloj-femenino-relogio-feminino-montre-femme-qfav7s",
			"https://www.linio.com.mx/p/500-1000mah-mini-porta-til-inala-mbrico-bluetooth-42-altavoz-hifi-bas-s10e4x",
			"https://www.linio.com.mx/p/funda-para-samsung-galaxy-s7-edge-volteo-magne-tico-lhv2jl",
			"https://www.linio.com.mx/p/reloj-pulsera-hombre-reloj-pulsera-deportivo-cuarzo-deportivo-lujo-caqui-le51pv",
			"https://www.linio.com.mx/p/luckyly-bolsa-lily-azul-celeste-yof41t",
			"https://www.linio.com.mx/p/dropshipping-mascota-inteligente-escape-gato-de-juguete-juguetes-aut-tx--x04ket",
			"https://www.linio.com.mx/p/topk-q-bien-magne-tico-cable-para-galaxy-s9-plus-s8-usb-3-0-d-1m-fuc-qcbwvz",
			"https://www.linio.com.mx/p/lala-cartoon-pig-series-novedad-mesa-la-mpara-de-escritorio-3d-led-nigh-oqiq1q",
			"https://www.linio.com.mx/p/zanzea-blusala-camisamanga-larga-batwing-atractivo-tmv6uj",
			"https://www.linio.com.mx/p/agujero-doble-canal-vagina-3d-oral-masturbador-masculino-p--vbblwv",
			"https://www.linio.com.mx/p/650w-1300w-mini-calentador-ele-ctrico-porta-til-ventilador-ca-tnwf3o",
			"https://www.linio.com.mx/p/rodillo-de-microagujas-540-para-terapia-me-dica-herramienta-de-cuida--onf87t",
			"https://www.linio.com.mx/p/las-mujeres-usan-vibraciones-de-frecuencia-7-g-spot-masturbacio-n-estimulacio-n-dispositivo-f305-morado-opb5e4",
			"https://www.linio.com.mx/p/cubierta-de-seguridad-infantil-ajustador-correa-bandolera-kids-clip-de-cinturo-n-jrvw1w",
			"https://www.linio.com.mx/p/ventilador-ele-ctrico-de-la-ma-quina-de-burbujas-que-sopla-bubble-g-n-nin-os-jugando-ga-lffhrq",
			"https://www.linio.com.mx/p/auriculares-bluetooth-50-mini-tws-twins-v5-auriculares-este-reo-inala-mbricos-tojp3z",
			"https://www.linio.com.mx/p/2in1-perro-mascota-puppy-cat-training-clicker-whistle-click-entrenador-obediencia-negro-s3tjch",
			"https://www.linio.com.mx/p/para-huawei-nova-2-lite-funda-billetera-de-cuero-flip-vintage-rojo-jq67d1",
			"https://www.linio.com.mx/p/funda-para-oppo-r11s-estuche-resistente-os5x8h",
			"https://www.linio.com.mx/p/juguete-sexual-estimulador-de-cli-toris-ventosa-de-pezo-n--wyi79u",
			"https://www.linio.com.mx/p/no-es-posible-no-comunicar-lcad92",
			"https://www.linio.com.mx/p/maleti-n-moda-cuero-pu-maletines-marca-comercial-para-hombres-bolsos-al-por-n31fp6",
			"https://www.linio.com.mx/p/bufanda-hecha-a-mano-mujer-100-ela-stica-diadema-aute-ntica-rex-bufa-tquxzc",
			"https://www.linio.com.mx/p/forsining-moda-plata-movimiento-esqueleto-relojes-azul-luminoso-manos-jsjyl1",
			"https://www.linio.com.mx/p/christams-style-baby-boys-girls-romper-mamelucos-co-modos-de-manga-larg-ymldit",
			"https://www.linio.com.mx/p/exceso-de-velocidad-l298n-tablero-de-controlador-de-motor-de-puente-do-qbp691",
			"https://www.linio.com.mx/p/carcasas-funda-huawei-p10-billetera-de-cuero-flip-vintage-marro-n-lhavqo",
			"https://www.linio.com.mx/p/1par-sonda-universal-cable-de-prueba-1000v-20a-para-multi-metro-medidor-vc99-vc97-vc9808-wt-s3v4fq",
			"https://www.linio.com.mx/p/novedosas-camisetas-para-hombre-en-4-colores-con-cuello-en-v-profund--lfuxdb",
			"https://www.linio.com.mx/p/reproductor-mp3-de-64-gb-de-mu-sica-media-player-grabadora-de-voz-de-fm-radio-s1hkz6",
			"https://www.linio.com.mx/p/3-pcs-pantalones-cortos-hombre-ropa-sexy-terapia-magne-tica-shorts-salud-lun-yn8v8j",
			"https://www.linio.com.mx/p/li-nea-de-datos-de-mezclilla-plana-duradera-para-android-shark-fin-woven-flat-noodle-line-s3ywz9",
			"https://www.linio.com.mx/p/socofy-las-mujeres-calzan-los-holgazanes-planos-suaves-opj6t7",
			"https://www.linio.com.mx/p/botella-de-agua-de-dibujos-animados-capa-de-termo-de-vaci-o-de-doble-pa-osbd8k",
			"https://www.linio.com.mx/p/sudadera-con-capucha-de-disen-o-crop-para-mujer-con-estampado-de-moda--ryp3pe",
			"https://www.linio.com.mx/p/una-marca-producto-tipo-pieza-para-levantar-nalgas-aumenta-la-almohadilla-falsa-ventilacio-n-de-tras-js0r6d",
			"https://www.linio.com.mx/p/el-disen-o-del-estilo-de-coche-faros-traseras-traslu-cidas-luz-peli-cula-girada-pegados-a-los-coches-tq9rnj",
			"https://www.linio.com.mx/p/led-de-la-placa-del-carnet-de-proyeccio-n-de-luz-la-ser-para-bmw-x3-x5-x6-3-y-serie-5-ykmjdm",
			"https://www.linio.com.mx/p/ban-o-impermeable-libros-bebe-ban-o-de-agua-juguetes-con-dispositivo-bb-n30j8c",
			"https://www.linio.com.mx/p/decodificador-de-televisor-inteligente-2020-nuevo-h96-mini-h8-andro--lfbakf",
			"https://www.linio.com.mx/p/24-tipos-de-juguetes-de-marco-de-ajuste-fino-para-nin-os-con-transmisores-s3uvyv",
			"https://www.linio.com.mx/p/hugo-energise-de-hugo-boss-eau-de-toilette-125-ml-ld7rhr",
			"https://www.linio.com.mx/p/enganche-polar-de-coral-moda-toalla-toalla-colgante-de-toalla-absorbente-toalla-de-cocina-va6b2j",
			"https://www.linio.com.mx/p/la-moda-coreana-margaritas-flor-rosa-pulsera-de-oro-reloj-de-pulsera-nin-a-mujer-regalo-yobrp9",
			"https://www.linio.com.mx/p/poder-inala-mbrico-universal-de-carga-del-cargador-del-coji-n-para-el-tele-fono-mo-vil-mo-vil-tq89mn",
			"https://www.linio.com.mx/p/10-pc-car-auto-5v-adaptador-usb-adaptador-para-encendedor-de-21a-1a-para-la-mayoria-de-telefonos-oro--wxej5s",
			"https://www.linio.com.mx/p/funda-xiaomi-redmi-9a-billetera-de-cuero-flip-vintage-rosa-tpm296",
			"https://www.linio.com.mx/p/rycb-006-jaula-del-pene-con-llave-50-mm-con-orificio-uretral-de-acero-inoxidable-de-castidad-masculina-lock-ju1479",
			"https://www.linio.com.mx/p/benice-brand-snowboard-goggles-double-lens-anti-fog-uv-spher-tm91qc",
			"https://www.linio.com.mx/p/zlimsn-negra-correa-cuero-genuino-reloj-correa-18mm-20mm-22mm-24mm-24m-m-fuc-qbq2o0",
			"https://www.linio.com.mx/p/kawaii-plush-snowy-cuddly-owl-mun-ecas-coleccionables-parent-child-inte-vax209",
			"https://www.linio.com.mx/p/moda-2019-bufanda-de-sate-n-hiyab-de-seda-para-mujer-chal-cuadrado--s2088g",
			"https://www.linio.com.mx/p/sandalias-de-lentejuelas-de-taco-n-llamativo-de-moda-para-mujeres-con-dedos-desnudos-plata-wyuzym",
			"https://www.linio.com.mx/p/esca-ner-porta-til-bluetooth-inala-mbrico-1d-2d-co-digo-de-barras-esca--ykl7k8",
			"https://www.linio.com.mx/p/abridor-de-botellas-de-cerveza-personalidad-creativa-tirano-pun-o-abridor-de-botellas-de-cerveza-gold-jqj7qz",
			"https://www.linio.com.mx/p/wiko-lenny-5-funda-volteo-magne-tico-funda-tnbs35",
		]

		for i in urls:
			yield scrapy.Request(url=i, callback=self.parse_dir_contents, meta={'url':i})

	def parse_dir_contents(self, response):
		loader = ItemLoader(item=LiniocatItem(), response=response)

		#Extract from datalayer
		data = re.findall("var dataLayer =(.+?);\n", response.body.decode("utf-8"), re.S)
		
		descripcion = response.xpath('normalize-space(//div[@itemprop="description"] )').extract()
		porcentaje = response.xpath('(//span[@class="discount"])[last()]/text()').extract()
		if not porcentaje:
			porcentaje = 0
		stock = response.xpath('normalize-space(//button[@id="buy-now"][1]/text())').extract()
		#months = response.xpath('normalize-space(//*[@id="usp-menu"]/div/div/a[5]/span[2]/text())').extract()

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
		
		#loader.add_value("months", months)
		loader.add_value("url", response.meta.get('url'))
		loader.add_value("stock", stock)
		loader.add_value("discount", ls[0]["special_price"])
		loader.add_value("price", ls[0]["price"])
		loader.add_value("percentage", ls[0])
		loader.add_value("date", getFecha())

		return loader.load_item()