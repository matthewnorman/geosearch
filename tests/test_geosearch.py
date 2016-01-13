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


def test_adjoining_boxes():
    """
    What are the nearest eight boxes to the Palace
    :return:
    """

    geolocator = geosearch.LatLonGeolocator()
    hashcode = 'gcpuvpjhmu89'

    with pytest.raises(ValueError):
        geolocator._get_adjoining_hashes(hashcode=hashcode,
                                         precision=15)

    result = geolocator._get_adjoining_hashes(hashcode=hashcode,
                                              precision=12)

    assert result == ['gcpuvpjhmu83', 'gcpuvpjhmu8c', 'gcpuvpjhmu88',
                      'gcpuvpjhmu82', 'gcpuvpjhmu8b', 'gcpuvpjhmu8d',
                      'gcpuvpjhmu86', 'gcpuvpjhmu8f']

    result = geolocator._get_adjoining_hashes(hashcode=hashcode,
                                              precision=6)
    assert result == ['gcpuuz', 'gcpuvr', 'gcpuvn', 'gcpuuy',
                      'gcpuvq', 'gcpvj0', 'gcpvhb', 'gcpvj2']


def test_proximity_search():
    """
    Search for something around the Palace of Westminster.
    :return:
    """

    geolocator = geosearch.LatLonGeolocator()
    geolocator.add_location(latitude=51.499168, longitude=-0.124722, ID=2)
    geolocator.add_location(latitude=51.499178, longitude=-0.124722, ID=3)
    geolocator.add_location(latitude=51.499268, longitude=-0.124722, ID=4)
    geolocator.add_location(latitude=51.500168, longitude=-0.124722, ID=5)
    geolocator.add_location(latitude=51.699168, longitude=-0.124722, ID=6)
    geolocator.add_location(latitude=52.499168, longitude=-0.124722, ID=7)
    results = geolocator.proximity_search(latitude=51.499167,
                                          longitude=-0.124722,
                                          radius=1000)

    assert results == [2, 3, 4, 5]