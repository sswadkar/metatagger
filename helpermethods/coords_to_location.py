import reverse_geocoder as rg

def get_location_data(lat, lon):
    coordinates = (lat, lon)
    result = rg.search(coordinates)
    return result[0]['name'], result[0]['admin1'], result[0]['cc']
