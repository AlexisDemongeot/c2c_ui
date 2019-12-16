"""
This script load data from https://github.com/c2corg/v6_common and save it in a relevant format :

* common.json for attributes arrays
* fixed_strings_common_js.vue, a fake vue component, for attributes values that needs a translation

"""

import requests
import json
import os
import re
import optparse

default_URL = 'https://raw.githubusercontent.com/c2corg/v6_common/master/c2corg_common/'

parser = optparse.OptionParser()
parser.add_option("-p", "--path", dest="path",
                  help="path to common definitions")
parser.add_option("-a", "--api", dest="api",
                  help="path to api definitions")
parser.add_option("-u", "--url", dest="url",
                  help="url to common definitions repo",
                  default=default_URL)

(options, args) = parser.parse_args()

if options.path:
    def read_common_file(name):
        with open(os.path.join(options.path, '{}.py'.format(name))) as f:
            return f.read()

else:
    def read_common_file(name):
        URL = (options.url + '{}.py').format

        proxies = {"https" : os.environ["HTTPS_PROXY"]} if "HTTPS_PROXY" in os.environ else None
        text = requests.get(URL(name), proxies = proxies).text
        return text

# Load python file from c2corg_common, and parse it
def get_fields(name):
    text = read_common_file(name)
    # exec : only in dev mode, lint exception
    exec(text.encode('utf8'))
    return dict(locals())

# Load atributes file
# TODO : replace "values": "langs" by "values": "langs_priority" in fieldsProperties.json
attributes = get_fields('attributes')
attributes["langs"] = attributes["langs_priority"]

result = {}
result["attributes"] = {}

# get attribute list needed by UI
attribute_names = dict()
fields = json.load(open("./src/js/constants/fieldsProperties.json"))
for field in fields.values():
    if "values" in field:
        values = field["values"]
        if isinstance(values, str):
            attribute_names[values] = field.get("i18n", True)

# sort by key to help git tracking
attribute_names = {key: attribute_names[key] for key in sorted(attribute_names)}

# store this attribute in result
for attribute_name in attribute_names:
    result["attributes"][attribute_name] = attributes[attribute_name]

sortable_attributes = get_fields('sortable_search_attributes')
result["sortable_attributes"] = [sa for sa in sortable_attributes.keys()
                                 if "sortable_" in sa]

if options.api:
    with open('./src/js/constants/documentsProperties.json') as f:
        doc_list = ['user' if doc == 'profile'
                    else 'topo_map' if doc == 'map'
                    else doc
                    for doc in json.load(f).keys()]
    search_attributes = set()
    for doc_type in doc_list:
        with open(os.path.join(options.api,
                               '{}_mapping.py'.format(doc_type))) as f:
            map_file = f.read()
            FIELDS = re.findall(' +(FIELDS = \[.*?\])', map_file, re.DOTALL)
            if FIELDS:
                exec(FIELDS[0])
                search_attributes = search_attributes.union(FIELDS)
            ENUM_FIELDS = re.findall(' +(ENUM_RANGE_FIELDS = \[.*?\])',
                                     map_file, re.DOTALL)
            if ENUM_FIELDS:
                exec(ENUM_FIELDS[0])
                search_attributes = search_attributes.union(ENUM_RANGE_FIELDS)
    result["search_attributes"] = list(search_attributes)


# store letter_types
result["letter_types"] = get_fields('document_types')['ALL']

# save result
json.dump(result, open("./src/js/constants/common.json", "w"),
          sort_keys=True, indent=4)

# and update attributes that need a translation
with open("./src/translations/fixed_strings_common_js.vue", "w") as f:
    f.write("<template>\n")
    f.write("  <!-- auto-generated by tools/update-c2c-common.py -->\n")
    f.write("  <span>\n")

    for field in sorted(fields):
        f.write("    <span v-translate>{}</span>\n".format(field))

    for attribute_name in sorted(attribute_names):
        if attribute_names[attribute_name]: # does it need translation ?
            f.write("    <!-- {} -->\n".format(attribute_name))
            for value in attributes[attribute_name]:
                f.write('    <span v-translate translate-context="{}">{}</span>\n'.format(attribute_name, value))

    f.write("  </span>\n")
    f.write("</template>\n")
