"""
Put data from multiple formats into geopandas.

Direct access OSM via API.

Compatibility issues with the read_file() method of geopandas for .shp (fiona issue), so build an external conversion method

Discussion on how to get all OSM changesets for a user (requires iteration):
https://help.openstreetmap.org/questions/23089/how-to-query-all-changes

Shapefile specification (https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf)
Shape Type Codes:
Value   Shape Type
0       Null Shape
1       Point
3       PolyLine
5       Polygon
8       MultiPoint
11      PointZ
13      PolyLineZ
15      PolygonZ
18      MultiPointZ
21      PointM
23      PolyLineM
25      PolygonM
28      MultiPointM
31      MultiPatch

"""
from osmapi import OsmApi
import geopandas as gp
import pandas as pd
import shapely as shp
import shapefile

# Initialize the OSM API
api = OsmApi()


def get_changeset(changeset_id, crs={'init':'epsg:4326'}):
    # Function to download a changeset and return it as a GeoDataFrame
    # default coordinate refrence system set to WGS84 (lon/lat).
    # OSM API data definition is at wiki.openstreetmap.org/wiki/API_v0.6
    set = api.ChangesetDownload(changeset_id)
    raw_df = pd.DataFrame(set)  # intermediate dataframe to hold the raw changeset
    flat_df = pd.concat([raw_df.drop(['data'], axis=1), raw_df['data'].apply(pd.Series)], axis=1)  # convert data dict to individual columns
    # get shapefiles for points
    # TODO: make this generic for lines/polylines and polygons (if statements?)
    geometry = [shp.geometry.Point(xy) for xy in zip(flat_df.lon, flat_df.lat)]  # convert lon/lat coordinates to shapley geometry
    df = flat_df.drop(['lon', 'lat'], axis=1)
    geo_df = gp.GeoDataFrame(df, crs=crs, geometry=geometry)
    return geo_df


def convert_shapefile(filepath, crs=None):
    # Function to read an ESRI shapefile and return a geopandas GeoDataFrame
    reader = shapefile.Reader(filepath)

    # Extract the column names for the data
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]

    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    frame = gp.GeoDataFrame.from_features(buffer, crs=crs)
    return frame
