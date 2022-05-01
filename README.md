# quickmap
Quickmap is a python to create quick visualisation of geographic data. Geographic data can be loaded with geojson or added through the api. Basemaps come from xyz tiles.

## Usage
```python
from quickmap import QuickMap

quick_map = QuickMap()
quick_map.load_geosjon('points.geojson')
quick_map.save_png('example.png')
```

### Point
Example of the class Point.
```python
point = Point.from_lat_lng(lat=41.85, lng=-87.65)
```

### Tile
Example of the class Tile.
```python
point = Point.from_lat_lng(lat=41.85, lng=-87.65)
tile = Tile.for_point(point, zoom=7)
```

## Installation
```bash
pip install -e .

```