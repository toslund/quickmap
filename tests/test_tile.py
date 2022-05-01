from quickmap.tile import BaseTile, Tile
from quickmap.tile import Point

import pytest

@pytest.fixture
def point():
    return Point(-87.65, 41.85)

def test_basetile():
    tile = BaseTile(1, 1, 1)
    assert tile.x == 1
    assert tile.y == 1
    assert tile.zoom == 1

def test_from_point(point):
    tile = Tile.for_point(point, zoom=7)
    assert tile.x == 32
    assert tile.y == 47
    