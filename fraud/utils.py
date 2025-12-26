from django.contrib.gis.geoip2 import GeoIP2

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")

# def get_client_ip(request):
#     return "8.8.8.8" 


def get_geo_location(ip):
    try:
        geo = GeoIP2()
        data = geo.city(ip)

        return {
            "country": data.get("country_name"),
            "city": data.get("city"),
            "lat": data.get("latitude"),
            "lon": data.get("longitude"),
        }
    except Exception:
        return None
