from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myapp")


def get_coordinates(cur_point):
    location = geolocator.geocode(cur_point)
    ans = [location]
    if location is not None:
        ans.append(location.latitude)
        ans.append(location.longitude)
    return ans
