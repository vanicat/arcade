import sys

shapely_exists = False

try:
    import shapely
    shapely_exists = True
except ImportError:
    pass


if shapely_exists:
    from .geometry_shapely import are_polygons_intersecting
    from .geometry_shapely import is_point_in_polygon
else:
    from .geometry_python import are_polygons_intersecting
    from .geometry_python import is_point_in_polygon
