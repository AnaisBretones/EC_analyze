from shapely import geometry
from shapely.geometry import Point
from shapely.geometry import Polygon


poly = Polygon([(0, 0), (1, 1), (1, 0)])


print(poly.wkt)
