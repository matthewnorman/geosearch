import pytrie
import geohash
from haversine import haversine


class LatLonGeolocator():
    """
    Given a list of lat/lon coordinates, enable a returned list of
    local points.
    """

    def __init__(self):
        self.storage = pytrie.StringTrie()
        self.points_by_id = {}

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
        self.points_by_id[ID] = (latitude, longitude)

    def _decode_by_hash(self, hash):
        """
        Given a hash, return the results stored in the Storage Engine
        :param hash:
        :return:
        """

        return self.storage[hash]

    def _get_adjoining_hashes(self, hashcode, precision):
        """
        Given a hash, find the nearest eight boxes (four adjacent,
        four diagonal) to the box.

        :param hashcode: Initial full geohash
        :param precision: Level of precision, integer
        :return:
        """
        if precision > len(hashcode):
            raise ValueError('Precision greater than hashcode size.')
        reduced_hash = hashcode[:precision]

        return geohash.neighbors(reduced_hash)

    def add_location(self, latitude, longitude, ID):
        """
        Accessor to add IDs
        :param latitude: Floating point
        :param longitude: Floating point
        :param id: Global ID
        :return:
        """

        self._encode_and_store_(latitude=latitude, longitude=longitude,
                                ID=ID)

    def proximity_search(self, latitude, longitude, radius):
        """
        Given a centerpoint, find everything within a radius around
        that latitude and longitude, returned in order.

        :param latitude: floating point latitude
        :param longitude: floating point longitude
        :param radius: radius in meters.
        :return:
        """

        hashcode = geohash.encode(latitude=latitude, longitude=longitude)
        centerpoint = (latitude, longitude)

        tmp_hashcode = ''
        for x in hashcode:
            # Go through the hashcode character by character
            tmp_hashcode += x
            lat, lng, delta_lat, delta_lng = geohash.decode(tmp_hashcode,
                                                            delta=True)
            overall_lat = 2 * 1000 * haversine(
                point1=(latitude - delta_lat, longitude),
                point2=(latitude + delta_lat, longitude)
            )
            overall_lng = 2 * 1000 * haversine(
                point1=(latitude, longitude-delta_lng),
                point2=(latitude, longitude+delta_lng)
            )

            dist = min(overall_lng, overall_lat)
            if dist < radius:
                break

        if tmp_hashcode == '':
            raise ValueError('Radius larger than earth')

        precision = len(tmp_hashcode)

        search_hashes = self._get_adjoining_hashes(hashcode=hashcode,
                                                   precision=precision)
        search_hashes.append(tmp_hashcode)

        possible_points = []
        result_values = []

        for search_hash in search_hashes:
            possible_points.extend(self.storage.values(prefix=search_hash))

        for point_id in possible_points:
            point = self.points_by_id[point_id]
            dist = haversine(centerpoint, point)
            if dist <= radius:
                result_values.append((point_id, dist))

        sorted_results = sorted(result_values, key = lambda x: x[1])
        final_results = [x[0] for x in sorted_results]
        return final_results