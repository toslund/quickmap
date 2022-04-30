from typing import List

from .feature import FeatureCollection
from .tile import Tile, TileCollection
from .geometry import BoundingBox, Point
from .canvas import MapCanvas


class QuickMap:

    def __init__(self, feature_collection: FeatureCollection = None) -> None:
        if feature_collection:
            self._feature_collection = feature_collection
        else:
            self._feature_collection = FeatureCollection()
        # self.tiles: TileCollection = TileCollection()
        self.canvas = MapCanvas()

    @property
    def features(self):
        for feature in self._feature_collection:
            yield feature

    @property
    def feature_collection(self):
        return self._feature_collection

    @feature_collection.setter
    def feature_collection(self, value):
        self._feature_collection = value
        self.canvas._tiles.calculate_tiles(self.feature_collection.bounding_box)

    def draw_feature_collection(self):
        for feature in self.feature_collection.features:
            self.canvas.draw_feature(feature)

__all__ = ['QuickMap']
