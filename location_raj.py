from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_geopy_app")


def reverse_location(lat,long):
    location = geolocator.reverse(f"{lat},{long}")
    return location.raw