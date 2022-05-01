from quickmap.feature import FeatureCollection

geojson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "population": 100
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-112.0372, 46.608058]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "population": 200
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-80.0372, 40.608058]
      }
    }
  ] 
}

def test_field_access():
  fc = FeatureCollection()
  assert fc.features == []

def test_from_json():
  fc = FeatureCollection()
  fc.load_geojson(geojson)
  assert len(fc.features) == 2