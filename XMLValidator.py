from lxml import etree


def validate(xmlparser, xmlfilename):
    try:
        with open(xmlfilename, 'rb') as f:
            etree.fromstring(f.read(), xmlparser)
        return True
    except etree.XMLSchemaError:
        return False


schema_file = 'sample.xsd'
with open(schema_file, 'rb') as f:
    schema_root = etree.XML(f.read())

schema = etree.XMLSchema(schema_root)
xmlparser = etree.XMLParser(schema=schema)

filenames = ['sample.xml', ]
for filename in filenames:
    if validate(xmlparser, filename):
        print("%s passes validation" % filename)
    else:
        print("%s does not pass validation" % filename)
