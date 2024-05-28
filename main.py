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

ext_list = {"xml", "json", "yaml", "yml"}


def validation(file, input_ext):
    try:
        f = open(file)
    except FileNotFoundError:
        print(f"No such file: {input_file}")
        return False
    f.close()

    with open(file, "r") as f:
        match input_ext:
            case "json":
                try:
                    json.load(f)
                except ValueError:
                    print("Invalid JSON")
                    return False
            case "yaml" | "yml":
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError:
                    print("Invalid YAML")
                    return False
            case "xml":
                try:
                    xmltodict.parse(f.read())
                except Exception:
                    print("Invalid XML")
                    return False
    return True


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


def convert_xml(file, t_file, target_ext):
    with open(file) as xml_file:
        xml = xmltodict.parse(xml_file.read())

    match target_ext:
        case "json":
            with open(t_file, "w") as outfile:
                json.dump(xml, outfile)
        case "yaml" | "yml":
            with open(t_file, "w") as outfile:
                yaml.dump(xml, outfile)
        case _:
            print("Conversion of the same type")


def main():
    cond = validation(input_file, input_extension)
    if cond is True and target_extension in ext_list:
        match input_extension:
            case "json":
                convert_json(input_file, target_file, target_extension)
            case "yaml" | "yml":
                convert_yaml(input_file, target_file, target_extension)
            case "xml":
                convert_xml(input_file, target_file, target_extension)
            case _:
                print("Conversion not possible/1")
    else:
        print("Conversion not possible/2")


main()
