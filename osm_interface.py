"""
Code to get and process data from OpenStreetMap
"""
from osmapi import OsmApi
import geopandas as gp

api = OsmApi()

# In the future, get info for a group of users
users = ['paulopp', 'Sneakytiki', 'TheLazerClap']

for my_username in users:
    # Get user changesets
    # Can limit area with min/max lat/lon, and by timeframe
    sets = api.ChangesetsGet(username=my_username)
    changeset_list = list(sets.keys())

    # Get and process changesets
    total = 0
    for id in changeset_list:
        my_changeset = api.ChangesetDownload(id)
        total = total + len(my_changeset)

    print(my_username + ': ' + str(total))
