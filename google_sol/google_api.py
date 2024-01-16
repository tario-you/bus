import requests


def get_optimized_route(api_key, origin, destination, waypoints):
    base_url = "https://maps.googleapis.com/maps/api/directions/json?"

    # Convert waypoints list to string format
    waypoints_str = "|".join(waypoints)

    # Create the URL
    url = (f"{base_url}origin={origin}&destination={destination}"
           f"&waypoints=optimize:true|{waypoints_str}&key={api_key}")

    response = requests.get(url)
    data = response.json()

    # Check for errors
    if data['status'] != 'OK':
        return f"Error: {data['status']}"

    # Extract the optimized route
    optimized_route = [leg['end_address'] for leg in data['routes'][0]['legs']]

    return optimized_route


optimized_stops = get_optimized_route(api_key, origin, destination, waypoints)
print(optimized_stops)
