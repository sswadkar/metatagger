from geopy.geocoders import Nominatim

def get_location_data(lat, lon):
    geolocator = Nominatim(user_agent="metatagger")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw['address']

    city = address.get('city', '')
    if not city:
        city = address.get('hamlet', '')
    if not city:
        city = address.get('town', '')
    if not city:
        city = address.get('village', '')

    state = address.get('state', '')
    country = address.get('country', '')
    return city, state, country
