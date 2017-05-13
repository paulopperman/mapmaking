"""
Get data from OSM and represent it with geopandas objects.

Types of things to get from OSM:

* Changesets
* Elements

Filter by actions:
create
modify
delete

"""
from osmapi import OsmApi
import geopandas as gp

api = OsmApi()