from shapely.geometry import Point
from shapely.geometry import Polygon


class RestrictedZone:

    def __init__(self, zone_id, coordinates):
        self.zone_id = zone_id
        self.polygon = Polygon(coordinates)

    def contains(self, x, y):
        point = Point(x, y)

        return self.polygon.contains(point)