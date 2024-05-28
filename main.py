import json
import sys
import yaml
import xmltodict
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml

input_file = sys.argv[1]
input_extension = sys.argv[1].split(".")[-1]
target_file = sys.argv[2]
target_extension = target_file.split(".")[-1]


def convert_json(file, t_file, target_ext):
    with open(file) as json_file:
        data = json.load(json_file)

    match target_ext:
        case 'yaml' | "yml":
            with open(t_file, "w") as outfile:
                yaml.dump(data, outfile)
        case "xml":
            with open(t_file, "w") as outfile:
                xml = dicttoxml(data)
                dom = parseString(xml)
                dump = dom.toprettyxml()
                outfile.write(dump)
        case _:
            print("Conversion of the same type")
            with open(t_file, "w") as outfile:
                json.dump(data, outfile)


def convert_yaml(file, t_file, target_ext):
    with open(file) as yaml_file:
        data = yaml.safe_load(yaml_file)

    match target_ext:
        case "json":
            with open(t_file, "w") as outfile:
                json.dump(data, outfile)
        case "xml":
            with open(t_file, "w") as outfile:
                xml = dicttoxml(data)
                dom = parseString(xml)
                dump = dom.toprettyxml()
                outfile.write(dump)
        case _:
            print("Conversion of the same type")
