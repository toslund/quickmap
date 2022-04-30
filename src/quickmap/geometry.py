import math, sys
from dataclasses import dataclass
from typing import Optional
from collections import namedtuple

from .meta import resolution, ORIGIN_SHIFT, TILE_SIZE

from pyproj import Transformer

# BasePoint = namedtuple('BasePoint', 'latitude longitude')

@dataclass(unsafe_hash=True)
class BasePoint:
    '''Class for representing a point geometry'''
    x: Optional[float] = None
    y: Optional[float] = None

@dataclass(unsafe_hash=True)
class BoundingBox:
    '''Class for min max of Geometry, Feature, or FeatureCollection'''
    x_min: Optional[float] = sys.float_info.max
    x_max: Optional[float] = sys.float_info.min
    y_min: Optional[float] = sys.float_info.max
    y_max: Optional[float] = sys.float_info.min

    def as_points(self):
        points = [(self.x_min, self.y_min), (self.x_min, self.y_max), (self.x_max, self.y_max), (self.x_max, self.y_min)]
        return [BasePoint(x=xy[0], y=xy[1]) for xy in set([(self.x_min, self.y_min), (self.x_min, self.y_max), (self.x_max, self.y_max), (self.x_max, self.y_min)])]

class Point(BasePoint):
    """Immutable Point class"""

    TRAN_4326_TO_3857 = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    
    @classmethod
    def from_geometry_dict(cls, geometry_dict):
        return cls(x=geometry_dict["coordinates"][0], y=geometry_dict["coordinates"][1])

    @classmethod
    def from_lat_lng(cls, lng=0.0, lat=0.0):
        """Creates a point from lat/lon in WGS84"""
        assert -180.0 <= lng <= 180.0
        assert -90.0 <= lat <= 90.0
        return cls(x=lng, y=lat)

    @classmethod
    def from_pixel(cls, pixel_x=0, pixel_y=0, zoom=None):
        """Creates a point from pixels X Y Z (zoom) in pyramid"""
        max_pixel = (2 ** zoom) * TILE_SIZE
        assert 0 <= pixel_x <= max_pixel, 'Point X needs to be a value between 0 and (2^zoom) * 256.'
        assert 0 <= pixel_y <= max_pixel, 'Point Y needs to be a value between 0 and (2^zoom) * 256.'
        meter_x = pixel_x * resolution(zoom) - ORIGIN_SHIFT
        meter_y = pixel_y * resolution(zoom) - ORIGIN_SHIFT
        meter_x, meter_y = cls._sign_meters(meters=(meter_x, meter_y), pixels=(pixel_x, pixel_y), zoom=zoom)
        return cls.from_meters(meter_x=meter_x, meter_y=meter_y)

    @classmethod
    def from_meters(cls, meter_x=0.0, meter_y=0.0):
        """Creates a point from X Y Z (zoom) meters in Spherical Mercator EPSG:900913"""
        assert -ORIGIN_SHIFT <= meter_x <= ORIGIN_SHIFT, \
            'Meter X needs to be a value between -{0} and {0}.'.format(ORIGIN_SHIFT)
        assert -ORIGIN_SHIFT <= meter_y <= ORIGIN_SHIFT, \
            'Meter Y needs to be a value between -{0} and {0}.'.format(ORIGIN_SHIFT)
        longitude = (meter_x / ORIGIN_SHIFT) * 180.0
        latitude = (meter_y / ORIGIN_SHIFT) * 180.0
        latitude = 180.0 / math.pi * (2 * math.atan(math.exp(latitude * math.pi / 180.0)) - math.pi / 2.0)
        return cls(latitude=latitude, longitude=longitude)

    @property
    def latitude_longitude(self):
        """Gets lat/lon in WGS84"""
        return self.latitude, self.longitude

    @property
    def lat(self):
        """Gets lat in WGS84"""
        return self.y

    @property
    def lng(self):
        """Gets lat in WGS84"""
        return self.x

    @property
    def bounding_box(self) -> BoundingBox:
        return BoundingBox(
            x_min=self.x,
            x_max=self.x,
            y_min=self.y,
            y_max=self.y
        )

    def pixels(self, zoom=None):
        """Gets pixels of the EPSG:4326 pyramid by a specific zoom, converted from lat/lon in WGS84"""
        meter_x, meter_y = self.web_mercator
        pixel_x = (meter_x + ORIGIN_SHIFT) / resolution(zoom=zoom)
        pixel_y = (meter_y - ORIGIN_SHIFT) / resolution(zoom=zoom)
        return abs(round(pixel_x)), abs(round(pixel_y))

    @property
    def web_mercator(self):
        """Gets the XY meters in Spherical Mercator EPSG:3857, converted from lat/lon in WGS84"""
        meter_x = self.lng * ORIGIN_SHIFT / 180.0
        meter_y = math.log(math.tan((90.0 + self.lat) * math.pi / 360.0)) / (math.pi / 180.0)
        meter_y = meter_y * ORIGIN_SHIFT / 180.0
        # print(self.TRAN_4326_TO_3857.transform(self.lng, self.lat))
        return meter_x, meter_y

    @staticmethod
    def _sign_meters(meters, pixels, zoom):
        half_size = int((TILE_SIZE * 2 ** zoom) / 2)
        pixel_x, pixel_y = pixels
        meter_x, meter_y = meters
        meter_x, meter_y = abs(meter_x), abs(meter_y)
        if pixel_x < half_size:
            meter_x *= -1
        if pixel_y > half_size:
            meter_y *= -1
        return meter_x, meter_y

class Polygon:
    
    def __init__(self) -> None:
        self.bounding_box = BoundingBox()


__all__ = ['Point', 'Polygon', 'BoundingBox']
