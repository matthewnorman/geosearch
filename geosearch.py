import pytrie
import geohash


class LatLonGeolocator():
    """
    Given a list of lat/lon coordinates, enable a returned list of
    local points.
    """

    def __init__(self):
        self.storage = pytrie.StringTrie()

    def _encode_and_store_(self, latitude, longitude, ID):
        """
        Take a latitude/longitude pair and store it in your engine
        :param latitude: floating point latitude
        :param longitude: floating point longitude
        :param ID: Your unique ID
        :return:
        """
        hash = geohash.encode(latitude=latitude, longitude=longitude)
        self.storage[hash] = ID

    def _decode_by_hash(self, hash):
        """
        Given a hash, return the results stored in the Storage Engine
        :param hash:
        :return:
        """

        return self.storage[hash]

