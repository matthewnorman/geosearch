import pytest
import random
import geohash
from haversine import haversine
from unittest import mock

from geosearch import geolocate


def test_encoding_decoding():
    """
    Let's see if we can locate the Palace of Westminster.
    :return:
    """

    ID = 1
    geolocator = geolocate.LatLonGeolocator()
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

    geolocator = geolocate.LatLonGeolocator()
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

    geolocator = geolocate.LatLonGeolocator()
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


def test_proximity_search_long():
    """
    Create a very, very long test that runs to find things.
    :return:
    """

    generated_locations = {}
    radius = 10000

    for ID in range(1000):
        generated_locations[ID] = {
            'latitude': 51.5 + random.uniform(-0.5, 0.5),
            'longitude': 0.0 + random.uniform(-0.5, 0.5)
        }

    geolocator = geolocate.LatLonGeolocator()
    for ID, latlon in generated_locations.items():
        geolocator.add_location(latitude=latlon['latitude'],
                                longitude=latlon['longitude'],
                                ID=ID)

    results = geolocator.proximity_search(latitude=51.5,
                                          longitude=0.0,
                                          radius=radius)

    for result in results:
        location = generated_locations[result]
        dist = haversine((51.5, 0.0),
                         (location['latitude'],
                          location['longitude'])) * 1000
        assert dist <= radius

    neg_results = generated_locations.keys() - results
    for ID in neg_results:
        location = generated_locations[ID]
        point = (location['latitude'], location['longitude'])
        dist = 1000 * haversine((51.5, 0.0), point)
        assert dist > radius
