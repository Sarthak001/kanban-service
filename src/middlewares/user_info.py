from flask import Flask, request, jsonify
from datetime import datetime
import jwt


# User information capturing middleware
def capture_user_info(route_function):
    def wrapper(*args, **kwargs):
        # Get the real IP address considering proxies
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        user_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.remote_addr

        # Get current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get user location (Note: This is a dummy example, replace with actual location retrieval logic)
        user_location = get_user_location(user_ip)

        # Get User-Agent
        user_agent = request.headers.get('User-Agent', 'Unknown')

        # Add captured information to request object for easy access in routes
        request.user_info = {
            'ip_address': user_ip,
            'timestamp': current_time,
            'location': user_location,
            'user_agent': user_agent
        }

        return route_function(*args, **kwargs)

    return wrapper

# Dummy function to simulate user location retrieval (replace with actual logic)
def get_user_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data