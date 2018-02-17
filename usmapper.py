#! /usr/bin/env python2

import os
import sys
import us

from xml.etree import ElementTree


oregon = os.path.join(os.path.dirname(__file__), "USA-Blank.svg")

style = "fill-opacity:1;stroke:#ffffff;stroke-width:2;stroke-linejoin:round;stroke-opacity:1;fill:"

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

data_colors = goldfish


# Legend
# 1 - nothing
# 2 - CBD
# 3 - medical
# 4 - legal

states = {
 'Alabama': 2,
 'Alaska': 4,
 'Arizona': 3,
 'Arkansas': 3,
 'California': 4,
 'Colorado': 4,
 'Connecticut': 3,
 'Delaware': 3,
 'District of Columbia': 4,
 'Florida': 2,
 'Georgia': 2,
 'Hawaii':3,
 'Idaho': 1,
 'Illinois': 3,
 'Indiana': 3,
 'Iowa': 2,
 'Kansas': 1,
 'Kentucky': 2,
 'Louisiana': 3,
 'Maine': 4,
 'Maryland': 3,
 'Massachusetts': 4,
 'Michigan': 3,
 'Minnesota': 3,
 'Mississippi': 1,
 'Missouri': 3,
 'Montana': 3,
 'Nebraska': 1,
 'Nevada': 4,
 'New Hampshire': 3,
 'New Jersey': 3,
 'New Mexico': 3,
 'New York': 3,
 'North Carolina': 2,
 'North Dakota': 3,
 'Ohio': 1,
 'Oklahoma': 2,
 'Oregon': 4,
 'Pennsylvania': 3,
 'Rhode Island': 3,
 'South Carolina': 2,
 'South Dakota': 1,
 'Tennessee': 2,
 'Texas': 2,
 'Utah': 2,
 'Vermont': 4,
 'Virginia': 2,
 'Washington': 4,
 'West Virginia': 1,
 'Wisconsin': 2,
 'Wyoming': 2
}

data = states

abbr_map = dict([(x.abbr, x.name) for x in us.states.STATES])

# def chooseColor(value):
#     input_range = float(max(data.values()) - 0)
#     output_range = float(len(data_colors) - 1)
#     output_color = (((value - 0) * output_range) / input_range) + 0
#     return data_colors[int(round(output_color))]

def chooseColor(value):
    return data_colors[value]

def main():
    # Load the SVG map
    with open(oregon) as f:
        tree = ElementTree.parse(f)

    root = tree.getroot()

    # Find counties
    elements = [e for e in root.iter()]

    for e in elements[1:]:
        # trim w3 spec version
        tag = e.tag.split('}')[-1]
        attrs = dict(e.attrib.items())
        if tag == 'path' and attrs.get('id') in abbr_map:
            abbr = attrs['id']
            state = abbr_map[abbr]
            color = chooseColor(data[state])
            new_style = style + color

            # print "%s - %s"%(state, color)

            e.set('style', new_style)
        elif tag == 'g' and attrs.get('id') in abbr_map:
                abbr = attrs['id']
                state = abbr_map[abbr]
                color = chooseColor(data[state])

                # print "%s - %s"%(state, color)

                for ge in e.iter():
                    ge_attrs = dict(ge.attrib.items())
                    if 'style' in ge_attrs:
                        # set color of sub-county
                        new_style = style + chooseColor(data[state])
                        ge.set('style', new_style)

    # write new svg
    tree.write(sys.stdout)


if __name__ == "__main__":
    main()