#! /usr/bin/env python2

from argparse import ArgumentParser
import os
import sys

from xml.etree import ElementTree
import yaml

oregon = os.path.join(os.path.dirname(__file__), "oregon-blank-scale.svg")

style = "fill-opacity:1;stroke:#a9a9a9;stroke-width:103;stroke-linejoin:round;stroke-opacity:1;fill:"
josehphine = "fill-opacity:1;stroke:#000000;stroke-width:103;stroke-linejoin:round;stroke-opacity:1;fill:"

scale_style = "opacity:1;fill-opacity:1;fill-rule:nonzero;stroke:#ffffff;stroke-width:94.64063263;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:18.89763832;stroke-opacity:1;paint-order:stroke fill markers;fill:"
star_style = "opacity:1;fill-opacity:1;fill-rule:nonzero;stroke:#ffffff;stroke-width:94.64063263;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:18.89763832;stroke-opacity:1;paint-order:stroke fill markers;fill:#f38630"


# green colors
greens = [
    "#f7fcfd",
    "#e5f5f9",
    "#ccece6",
    "#99d8c9",
    "#66c2a4",
    "#41ae76",
    "#238b45",
    "#006d2c",
    "#00441b"
]

goldfish = [
    "#ffffff",
    "#E0E4CC",
    "#A7DBD8",
    "#69D2E7",
    "#F38630",
    "#FA6900",
    "#333333"
]

total_colors_in_map = 9
data_colors = goldfish

producers = {
    "Baker":  1,
    "Benton": 21,
    "Clackamas":  127,
    "Clatsop": 9,
    "Columbia":   16,
    "Coos":   20,
    "Curry":  6,
    "Deschutes":  24,
    "Douglas": 2,
    "Harney": 1,
    "Hood River": 18,
    "Jackson": 189,
    "Jefferson":  0,
    "Josephine":  119,
    "Lake":   1,
    "Lane":   124,
    "Lincoln": 7,
    "Marion": 18,
    "Multnomah":  63,
    "Polk":   35,
    "Tillamook":  8,
    "Wasco":  10,
    "Washington": 58,
    "Yamhill": 35
}

processors = {
    "Baker":   1,
    "Benton":  5,
    "Clackamas":   24,
    "Clatsop": 0,
    "Columbia":    0,
    "Coos":    2,
    "Curry":   0,
    "Deschutes":   11,
    "Douglas": 0,
    "Harney":  0,
    "Hood River": 1,
    "Jackson": 13,
    "Jefferson":   0,
    "Josephine":   2,
    "Lake":    0,
    "Lane":    23,
    "Lincoln": 2,
    "Marion":  3,
    "Multnomah":   48,
    "Polk":    0,
    "Tillamook":   0,
    "Wasco":   2,
    "Washington":  4,
    "Yamhill": 3
}

both = {
    "Baker":   1,
    "Benton":  2,
    "Clackamas":   2,
    "Clatsop": 0,
    "Columbia":    0,
    "Coos":    1,
    "Curry":   0,
    "Deschutes":   3,
    "Douglas": 0,
    "Harney":  0,
    "Hood River": 0,
    "Jackson": 8,
    "Jefferson":   0,
    "Josephine":   0,
    "Lake":    0,
    "Lane":    8,
    "Lincoln": 0,
    "Marion":  2,
    "Multnomah":   8,
    "Polk":    1,
    "Tillamook":   0,
    "Wasco":   2,
    "Washington ": 0,
    "Yamhill": 0
}

#data = producers
data = processors


#
# TODO: Add support for a config/data file and or command line options..
#


color_map = {}


def readConfig(path):
    with open(path) as f:
        config = yaml.safe_load(f)

    # Validate the config
    print config

    return config


def chooseColor(value):
    # input_range = float(max(data.values()) - 0)
    # output_range = float(len(data_colors) - 1)
    # output_color = (((value - 0) * output_range) / input_range) + 0
    # return data_colors[int(round(output_color))]
    return color_map[value]


def main():
    #
    # Parse the command line options
    #
    parser = ArgumentParser(description="Generate a colored map")
    parser.add_argument("config_file", help="yaml config for your dataset")
    parser.add_argument("output", help="The output SVG you want created")
    args = parser.parse_args()

    config_file = args.config_file
    output_file = args.output_file
    if not output_file.endswith(".svg"):
        output_file += ".svg"

    #
    # Parse the config file
    #
    config = readConfig(config_file)
    sys.exit(1)


    # Load the SVG map
    with open(oregon) as f:
        tree = ElementTree.parse(f)

    root = tree.getroot()


    #
    # Setup the color scale
    #
    max_val = max(data.values())
    min_val = 0
    per_color = round((float(max_val) - 0) / (len(data_colors)-1))
    x = 1
    color_map[0] = data_colors[0]
    for i in range(1, max_val+1):
        if i%per_color == 0:
            x += 1
            if x > len(data_colors) - 1:
                x = len(data_colors) - 1

        color_map[i] = data_colors[x]
        # print "data_value: %d,  color index: %d"%(i, x)

    # print color_map
    reverse_color_map = {}
    for k, v in color_map.iteritems():
        reverse_color_map[v] = reverse_color_map.get(v, [])
        reverse_color_map[v].append(k)
    # print reverse_color_map
    # print color_map

    # Find counties
    elements = [e for e in root.iter()]
    parent_map = dict((c, p) for p in root.getiterator() for c in p)

    for e in elements[1:]:
        # trim w3 spec version
        tag = e.tag.split('}')[-1]
        attrs = dict(e.attrib.items())
        if tag == 'path' and attrs.get('id') in data:
            if 'style' in attrs:
                county = attrs['id']
                color = chooseColor(data[county])
                if county == "Josephine":
                    new_style = josehphine + color
                else:
                    new_style = style + color

                # print "%s - %s"%(county, color)

                e.set('style', new_style)
        elif tag == 'g' and attrs.get('id') in data:
                county = attrs['id']
                color = chooseColor(data[county])

                # print "%s - %s"%(county, color)

                for ge in e.iter():
                    ge_attrs = dict(ge.attrib.items())
                    if 'style' in ge_attrs:
                        # set color of sub-county
                        new_style = style + chooseColor(data[county])
                        ge.set('style', new_style)

    #
    # Set the scale
    #
    max_val = max(data.values())
    min_val = min(data.values())

    for e in elements[1:]:
        # trim w3 spec version
        tag = e.tag.split('}')[-1]
        attrs = dict(e.attrib.items())

        for c in range(total_colors_in_map):
            if tag == 'rect' and attrs.get('id') == "Scale%d-Color"%(c):
                if c >= len(data_colors):
                    # delete the element
                    parent_map[e].remove(e)
                elif 'style' in attrs:
                    new_style = scale_style + data_colors[c]
                    e.set('style', new_style)
            elif tag == 'tspan' and attrs.get('id') == "Scale%d-Text"%(c):
                if c >= len(data_colors):
                    # delete the element
                    parent_map[e].remove(e)
                else:
                    # print c, color_map[c], min(reverse_color_map[data_colors[c]]), max(reverse_color_map[data_colors[c]])
                    e.text = "%d - %d"%(min(reverse_color_map[data_colors[c]]), max(reverse_color_map[data_colors[c]]))
                    # print "Scale: %d, text: %s"%(c, e.text)

    # write new svg
    tree.write(sys.stdout)


if __name__ == "__main__":
    main()