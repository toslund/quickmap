from quickmap.geometry import BasePoint, Point

import pytest

def test_basepoint():
    point = BasePoint(-87.65, 41.85)
    assert point.y == 41.85
    assert point.x == -87.65

def test_from_lat_lng():
    point = Point.from_lat_lng(lat=41.85, lng=-87.65)
    assert point.y == 41.85
    assert point.x == -87.65
    print(point.web_mercator)

def test_web_mercator():
    point = Point(-87.65, 41.85)
    assert pytest.approx(point.web_mercator[0], 0.0001) == -9757153.36803043
    assert pytest.approx(point.web_mercator[1], 0.0001) == 5138536.587247468
