# Map Maker

An simple script for generating fully customizable geomaps.


## Requirements

This script requires Python 2.7


## Usage

```
> ./map-maker <config file> <output file>
```

**Arguments:**
  - `config file` - the yaml file describing your dataset and map
  - `output file` - the name of the svg file you want to create


 ## Config File

 Config files are simple yaml files that contain everything needed to populate a map. Effectively the map-maker script just reads this file and applies the contents to an existing map template. You can see examples of config files in the [examples](./examples) folder and the structure is described below:

  - **map** - this is the only root level object in the yaml file. All data used to populate a map is nested under the map object.
  - **type** - this is the type of map you want to create. The value for this field should match the name of one of the templates in the [map-templates](./map-templates) folder. For example, to create a map of the United States, your map type would be 'USA'.
  - **colors** - this is an ordered list of colors to use when shading the map. The values of your dataset will automatically be scaled to the colors listed. **Note**: 0 is the only value not scaled. Any 0 value in your dataset will be assigned to the first color in the list.
  - **title** - This is the title of your map.
  - **data** - This is a map of __names__ to __values__. If your map is of the United States, each name should be a state, and its corresponding value is the numeric value for that state. For example, your values might be the population of each state, or the percentage of registered voters in each state. As long as it is a number, the map will be shaded accordingly. Similarly, if your map is of a state, then your data set would be county names and their corresponding values.


## Map Templates

There are a few map templates already provided in the [map-templates](./map-templates) folder. Templates are SVG drawings with elements that follow the convention described below:

All maps should have the following elements:
  - A __tspan__ element with the id 'Map-Title'
  - A legend of color elements (one for each color in the list of colors). If your config file has fewer colors, the extra ones will be removed from the svg file:
    - A __rect__ element with the id 'Scale#-Color', where the number represents the index of the color in the **colors** list. 
    - A __tspan__ element with the id 'Scale#-Text'. This will be filled in with the range that particular color represents

Depending on the type of map you are creating, it needs to have __path__ or __g__ elements for with ids that match each of the names in the data set. For example, if your map is of the United States, there should be __path__ elements with the ids 'California', 'Texas', 'New York', etc.

**NOTE** SVG files are basically just xml. You can edit them in a text editor or in an vector editing tool such as inkscape.

Any new svg file you add to the [map-templates](./map-templates) folder will automatically be available to the map-maker script.


## Debugging

When creating new config files or templates, it may be useful to see the substitutions being matched or not matched. You can enable debugging output by adding the `-d` flag.


## Contributions

Just open a pull request!

## License

I consider this code public domain. Do what you want with it. I offer no warranty.

