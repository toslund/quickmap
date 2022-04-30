import math
from dataclasses import dataclass
from typing import Optional, List
import urllib.request

from .geometry import Point, BoundingBox
from .meta import TILE_SIZE

@dataclass(unsafe_hash=True)
class BaseTile:
    '''Class for representing a tile'''
    x: Optional[int] = None
    y: Optional[int] = None
    zoom: Optional[int] = None

class Tile(BaseTile):
    """Immutable Tile class"""

    @classmethod
    def for_point(cls, point: Point, zoom):
        """Returns tile that covers a given point"""
        return cls.for_latitude_longitude(lat=point.y, lng=point.x, zoom=zoom)

    # @classmethod
    # def for_meters(cls, meter_x, meter_y, zoom):
    #     """Creates a tile from X Y meters in Spherical Mercator EPSG:900913"""
    #     point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)
    #     pixel_x, pixel_y = point.pixels(zoom=zoom)
    #     return cls.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)
    
    @classmethod
    def for_latitude_longitude(cls, lat, lng, zoom):
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom  # 1 << zoom
        xtile = int((lng + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return cls(xtile, ytile, zoom)

    def fetch(self):
        url = f'https://tile.openstreetmap.org/{self.zoom}/{self.x}/{self.y}.png'
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Python-Package: quickmap')]
        image_data = opener.open(url)

        # image_data = urlopen(url)
        return image_data

    @property
    def bounds(self):
        """Gets the bounds of a tile represented as the most west and south point and the most east and north point"""
        google_x, google_y = self.google
        pixel_x_west, pixel_y_north = google_x * TILE_SIZE, google_y * TILE_SIZE
        pixel_x_east, pixel_y_south = (google_x + 1) * TILE_SIZE, (google_y + 1) * TILE_SIZE

        point_min = Point.from_pixel(pixel_x=pixel_x_west, pixel_y=pixel_y_south, zoom=self.zoom)
        point_max = Point.from_pixel(pixel_x=pixel_x_east, pixel_y=pixel_y_north, zoom=self.zoom)
        return point_min, point_max


class TileCollection:

    MAX_TILES = 16

    def __init__(self, zoom=15) -> None:
        self.tiles: List[Tile] = []
        self.zoom = zoom

    def calculate_tiles(self, bounding_box: BoundingBox, lazy=True):
        searching = True
        while self.zoom > 0 and searching:
            num_tiles = TileCollection.calculate_tile_coverage(bounding_box, self.zoom)
            if num_tiles <= self.MAX_TILES:
                searching = False
                break
            self.zoom -= 1

        tiles = [Tile.for_point(point, self.zoom) for point in bounding_box.as_points()]

        tile_xs = [tile.x for tile in tiles]
        tile_ys = [tile.y for tile in tiles]
        for x in range(min(tile_xs), max(tile_xs) + 1):
            for y in range(min(tile_ys), max(tile_ys) + 1):
                self.tiles.append(Tile(x=x, y=y, zoom=self.zoom))
        # if not lazy:
        #     self.fetch_tiles()

    # def fetch_tiles(self):
    #     for tile in self.tiles:
    #         tile.fetch()
    #         print('fetched')

    @property
    def min_x_tile(self):
        return min([tile.x for tile in self.tiles])
    
    @property
    def max_x_tile(self):
        return max([tile.x for tile in self.tiles])
    
    @property
    def min_y_tile(self):
        return min([tile.y for tile in self.tiles])
    
    @property
    def max_y_tile(self):
        return max([tile.y for tile in self.tiles])

    @property
    def x_tiles(self):
        return (self.max_x_tile - self.min_x_tile) + 1

    @property
    def y_tiles(self):
        return (self.max_y_tile - self.min_y_tile) + 1

    # @property
    # def origin_tile(self):
    #     min_x = self.min_x_tile
    #     min_y = self.min_y_tile
    #     for tile in self.tiles:
    #         if tile.x == min_x and tile
    #     return (self.max_y_tile - self.min_y_tile) + 1

    @staticmethod
    def calculate_tile_coverage(bounding_box: BoundingBox, zoom):
        tiles = [Tile.for_point(point, zoom) for point in bounding_box.as_points()]
        tile_x_min = min([tile.x for tile in tiles])
        tile_x_max = max([tile.x for tile in tiles])
        tile_y_min = min([tile.y for tile in tiles])
        tile_y_max = max([tile.y for tile in tiles])
        x_dimension = (tile_x_max - tile_x_min) + 1
        y_dimension = (tile_y_max - tile_y_min) + 1
        long_side = max([x_dimension, y_dimension])
        return long_side**2

__all__ = ['Tile', 'TileCollection']
