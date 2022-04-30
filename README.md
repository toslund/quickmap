# quickmap
Quickmap is a python to create quick visualisation of geographic data. Geographic data can be loaded with geojson or added through the api. Basemaps come from xyz tiles.

## Usage
```python
from quickmap import QuickMap, FeatureCollection

quick_map = QuickMap()
fc = FeatureCollection.from_geosjon(geojson)
quick_map.feature_collection = fc
quick_map.canvas.stitch_tiles()
quick_map.draw_feature_collection()
quick_map.canvas.save_image()
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