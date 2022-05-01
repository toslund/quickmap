from dataclasses import dataclass
import importlib
from typing import Optional

from PIL import Image, ImageDraw

from .tile import TileCollection
from .geometry import BoundingBox, Point
from .feature import Feature, FeatureCollection

class MapCanvas:
    def __init__(self, feature_collection: FeatureCollection) -> None:
        self._image = None
        self._basemap = None
        self._tiles = TileCollection()
        self._feature_collection = feature_collection

    def stitch_tiles(self):
        width = self._tiles.x_tiles * 256
        height = self._tiles.y_tiles * 256
        self._basemap = Image.new('RGBA', (width, height))

        for tile in self._tiles.tiles:
            im = Image.open(tile.fetch()).convert('RGBA')
            x = (tile.x - self._tiles.min_x_tile) * 256
            y = (tile.y - self._tiles.min_y_tile) * 256
            self._basemap.paste(im, (x, y))

    def render(self):
        self._image = self._basemap.copy()
        self.draw_features()

    def save_png(self, output_path):
        self.render()
        self._image.save(output_path, quality=95)

    def ellipse_from_pixel(self, x, y, px):
        radius = px/2
        x = x - self._tiles.min_x_tile * 256
        y = y - self._tiles.min_y_tile * 256
        xy = [(x - radius, y-radius), (x + radius, y + radius)]
        # translate
        return {'xy': xy, 'fill': 'black', 'outline': 'grey'}

    def translated(self, x, y):
        x = x - self._tiles.min_x_tile * 256
        y = y - self._tiles.min_y_tile * 256
        return x, y

    def draw_features(self):
        for feature in self._feature_collection.features:
            if isinstance(feature.geometry, Point):
                pixel_x, pixel_y = feature.geometry.pixels(self._tiles.zoom)
                with importlib.resources.path(__package__+'.icons', 'circle.png') as p:
                    data_path = p
                    icon = Image.open(data_path)
                    self._image.paste(icon, self.translated(pixel_x, pixel_y), icon)

                # d = ImageDraw.Draw(self._image)
                # self._image.paste(im, (x, y))
                # d.ellipse(**self.ellipse_from_pixel(pixel_x, pixel_y, 10))