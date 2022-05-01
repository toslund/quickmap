from typing import Union, Optional

from .geometry import Point, Polygon, BoundingBox
from .io_service import read_geojson

class Feature:
    supported_geometry_types = ['Point']
    unsupported_geometry_types = [
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
        "GeometryCollection"]

    # default_gcs = "epsg:4326"
    # default_projection = "epsg:3857"

    def __init__(self, geometry: Union[Point, Polygon] = None, properties: dict = None):
        self.properties = properties
        self.geometry = geometry

    def __repr__(self):
        return f'Feature(properties={self.properties}, geometry={self.geometry})'

    @classmethod
    def from_feature_dict(cls, feature_dict):
        if feature_dict['type'] != 'Feature':
            raise TypeError('Feature_dict must be a valid Geojson feature object')
        properties = feature_dict['properties']
        geometry = cls.geom_loader(feature_dict['geometry'])
        return cls(geometry, properties)

    @classmethod
    def from_geometry_dict(cls, geometry_dict):
        if geometry_dict['type'] in cls.unsupported_geometry_types:
            raise TypeError(f'Geometry: {geometry_dict["type"]} not supported at this time')
        geometry = cls.geom_loader(geometry_dict)
        return cls(geometry, properties = {})

    # def multipolygon_loader(self, coords):
    #     polygons = []
    #     for polygon in coords:
    #         _polygon = Polygon(polygon[0], self.projection)
    #         _polygon.holes = [Polygon(hole, self.projection) for hole in polygon[1:]]
    #         polygons.append(_polygon)
    #     return polygons

    @staticmethod
    def geom_loader(geometry_dict):
        if geometry_dict['type'] == 'Point':
            return Point.from_geometry_dict(geometry_dict)
        raise TypeError(f'Unsuported geometry type: {geometry_dict["type"]}')

    @property
    def bounding_box(self): #TODO Naive bb that does not factor in the antimeridian. Replace.
        return self.geometry.bounding_box


class FeatureCollection(Feature):

    def __init__(self, features: Optional[list[Feature]] = None):
        if features:
            self.features = features
        else:
            self.features = []

    # def load_features(self, data):
    #     """Load features from geojson data"""
    #     features = FeatureCollection.get_features(read_geojson(data))
    #     self.features.append(features)

    def load_geojson(self, data):
        """Load features from geojson data"""
        features = FeatureCollection.get_features(read_geojson(data))
        self.features.extend(features)

    # @staticmethod
    # def load_geosjon(data):
    #     """Load features from geojson data"""
    #     return FeatureCollection.get_features(read_geojson(data))

    @staticmethod
    def get_features(data):
        if isinstance(data, list):
            raise ValueError('Types list is not valid geojson object. Iterate lists containing valid geojson objects')      
        if data['type'] == "FeatureCollection":
            return [Feature.from_feature_dict(_feature) for _feature in data['features']]
        elif data['type'] == "Feature":
            return[Feature.from_feature_dict(data)]
        elif data['type'] in Feature.supported_geometry_types + Feature.unsupported_geometry_types:
            return[Feature.from_geometry_dict(data)]
        else:
            raise ValueError('Data must be a valid geojson object')

    @property
    def bounding_box(self): #TODO Naive bb that does not factor in the antimeridian. Replace.
        _bounding_boxes =  [n.bounding_box for n in self.features]
        if not _bounding_boxes:
            print('empty list')
            return BoundingBox()
        x_min = min([n.x_min for n in _bounding_boxes])
        x_max = max([n.x_max for n in _bounding_boxes])
        y_min = min([n.y_min for n in _bounding_boxes])
        y_max = max([n.y_max for n in _bounding_boxes])
        return BoundingBox(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)

__all__ = ['Feature', 'FeatureCollection']
