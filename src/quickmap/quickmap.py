from typing import List
from copy import deepcopy


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
        self.canvas = MapCanvas(self._feature_collection)

    @property
    def features(self):
        for feature in self._feature_collection:
            yield feature

    @property
    def feature_collection(self):
        return self._feature_collection

    @feature_collection.setter
    def feature_collection(self, value: FeatureCollection):
        self._feature_collection = value
        self.render_basemap()

    def load_geosjon(self, data):
        previous_bb = deepcopy(self._feature_collection.bounding_box)
        new_features = self._feature_collection.load_geojson(data)
        if previous_bb != self._feature_collection.bounding_box:
            self.render_basemap()
        print(previous_bb)
        print(self._feature_collection.bounding_box)
        return new_features

    def save_png(self, fpath):
        return self.canvas.save_png(fpath)

    def render_basemap(self):
        self.canvas._tiles.calculate_tiles(self.feature_collection.bounding_box)
        self.canvas.stitch_tiles()
        print("rendered basemap")

    def draw_feature_collection(self):
        for feature in self.feature_collection.features:
            self.canvas.draw_feature(feature)

__all__ = ['QuickMap']
