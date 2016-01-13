import pytest
from unittest import mock

import geosearch


def test_encoding_decoding():
    """
    Let's see if we can locate the Palace of Westminster.
    :return:
    """

    ID = 1
    geolocator = geosearch.LatLonGeolocator()
    geolocator._encode_and_store_(latitude=51.499167,
                                  longitude=-0.124722,
                                  ID=ID)

    result = geolocator._decode_by_hash(hash='gcpuvpjhmu89')
    assert result == ID
