import shapely
import geopandas as gpd
import numpy as np

g = gpd.read_file("lcsd000b16a_e.shp")
g = g.to_crs("EPSG:4326")

def get_coordinates(city):
    cities = list(g["CSDNAME"])
    if city not in cities:
        return None
    idxs = [x[0] for x in enumerate(cities) if x[1] == city]
    cities = []
    for idx in idxs:
        all_points = []
        if type(g["geometry"][idx]) == shapely.geometry.multipolygon.MultiPolygon:
            total_area = 0
            for i in list(g["geometry"][idx]):
                x, y = i.exterior.coords.xy
                all_points.append(list(zip(list(x), list(y))))
                total_area += i.area
        else:
            x, y = g["geometry"][idx].exterior.coords.xy
            all_points.append(list(zip(list(x), list(y))))
            total_area = g["geometry"][idx].area
        cities.append((all_points, total_area))
    return max(cities, key=lambda x: x[1])[0]

def get_centroid(city_data):
    return np.array(max(city_data, key=lambda x: len(x))).mean(axis=0)

toronto_coords = get_coordinates("Toronto")
print(toronto_coords)
print(get_centroid(toronto_coords))
