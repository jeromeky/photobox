from xml.dom.minidom import parse, Document

class Context:
	"""define some settings"""
	
	LABEL_WIDTH = "width"
	LABEL_HEIGHT = "height"
	LABEL_IMAGES_BY_PAGE = "images_by_page"
	
	width = "200"
	height = "200"
	imagesbypage = "20"
	xmlpath = ""

	
	
	def __init__(self, xmlpath):
		self.xmlpath = xmlpath
		print "init context"
		xmlSettings = ""
		try : 
			xmlSettings = parse(xmlpath)
			
			## store values in tmp in case if there is exception while reading xml
			tmpwidth = xmlSettings.getElementsByTagName(self.LABEL_WIDTH)[0].firstChild.nodeValue
			tmpheight = xmlSettings.getElementsByTagName(self.LABEL_HEIGHT)[0].firstChild.nodeValue
			tmpimagesbypage = xmlSettings.getElementsByTagName(self.LABEL_IMAGES_BY_PAGE)[0].firstChild.nodeValue

			## then we can set in context
			self.width = tmpwidth
			self.height = tmpheight
			self.imagesbypage = tmpimagesbypage
		except (IOError, IndexError) :
			## settings.xml don't exist, in this case we create it.
			## We also create it in case there is some errors 			
			doc = Document()
			print doc
	
			root = doc.createElement("settings")
	
			widthelement = doc.createElement(self.LABEL_WIDTH)
			widthvalue = doc.createTextNode(str(self.width))
			widthelement.appendChild(widthvalue)
			root.appendChild(widthelement)
	
			heightelement = doc.createElement(self.LABEL_HEIGHT)
			heightvalue = doc.createTextNode(str(self.height))
			heightelement.appendChild(heightvalue)
			root.appendChild(heightelement)
	
			imagesbypageelement = doc.createElement(self.LABEL_IMAGES_BY_PAGE)
			imagesbypagevalue = doc.createTextNode(str(self.imagesbypage))
			imagesbypageelement.appendChild(imagesbypagevalue)
			root.appendChild(imagesbypageelement)
			print "xmlpath"
			print xmlpath
			file_handle = open(xmlpath , "wb")
			root.writexml(file_handle)
			file_handle.close()
			
			print root.toprettyxml()
	
		print "finish context"
		print self.width
	def save(self, width, height, imagesbypage):
		if self.width == width and self.height == height and self.imagesbypage == imagesbypage :
			return
		
		self.width = width
		self.height = height
		self.imagesbypage = imagesbypage
		
		xmlSettings = parse(self.xmlpath)
	
		xmlSettings.getElementsByTagName(self.LABEL_WIDTH)[0].firstChild.nodeValue = width
		xmlSettings.getElementsByTagName(self.LABEL_HEIGHT)[0].firstChild.nodeValue = height
		xmlSettings.getElementsByTagName(self.LABEL_IMAGES_BY_PAGE)[0].firstChild.nodeValue = imagesbypage
		
		f = open(self.xmlpath, "w")
		xmlSettings.writexml(f)
		f.close()
	
	def getsize(self):
		return self.width + "x" + self.height