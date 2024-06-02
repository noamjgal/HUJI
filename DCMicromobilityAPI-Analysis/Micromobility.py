import requests
import geopandas as gpd
from shapely.geometry import Point, LineString
import datetime
import schedule
import time
import contextily as ctx
import matplotlib.pyplot as plt

def fetch_and_save_vehicle_data(date, output_filename="vehicles.shp"):
    api_dict = {
        'Capital Bikeshare': 'https://gbfs.capitalbikeshare.com/gbfs/en/free_bike_status.json',
        'Lime Micromobility (including Jump bikes)': 'https://data.lime.bike/api/partners/v1/gbfs/washington_dc/free_bike_status.json',
        'Lyft': 'https://s3.amazonaws.com/lyft-lastmile-production-iad/lbs/dca/free_bike_status.json',
        'Helbiz': 'https://api.helbiz.com/admin/reporting/washington/gbfs/gbfs.json',
        'Spin': 'https://web.spin.pm/api/gbfs/v1/washington_dc/free_bike_status',
        
    }

    vehicle_info_list = []
    origin_destination_pairs = []

    for company, url in api_dict.items():
        print(f"Processing data from {company}:")
        try:
            response = requests.get(url)
            data = response.json()
            if 'bikes' in data['data']:
                vehicles_data = data['data']['bikes']
            elif 'vehicles' in data['data']:
                vehicles_data = data['data']['vehicles']
            else:
                print(f"No 'bikes' or 'vehicles' found in the response from {company}")
                continue

            origin = None
            for vehicle in vehicles_data:
                lon = vehicle.get('lon')
                lat = vehicle.get('lat')
                bike_id = vehicle.get('bike_id') or vehicle.get('id')
                is_reserved = vehicle.get('is_reserved')
                is_disabled = vehicle.get('is_disabled')
                vehicle_info_list.append({
                    'company': company,
                    'lon': lon,
                    'lat': lat,
                    'bike_id': bike_id,
                    'is_reserved': is_reserved,
                    'is_disabled': is_disabled
                })

                if is_reserved == 0 and origin is not None:
                    destination = (lon, lat)
                    origin_destination_pairs.append((origin, destination))
                    origin = None
                elif is_reserved == 1 and origin is None:
                    origin = (lon, lat)

            print(f"Successfully processed data from {company}")
        except Exception as e:
            print(f"Error processing data from {company}: {e}")

    geometry = [Point(vehicle['lon'], vehicle['lat']) for vehicle in vehicle_info_list]
    gdf = gpd.GeoDataFrame(vehicle_info_list, geometry=geometry, crs="EPSG:4326")

    # Create a GeoDataFrame for the routes
    route_lines = [LineString(pair) for pair in origin_destination_pairs]
    route_gdf = gpd.GeoDataFrame(geometry=route_lines, crs="EPSG:4326")

    # Save the GeoDataFrames as shapefiles
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    vehicles_filename = f"vehicles_{timestamp}.shp"
    route_filename = f"routes_{timestamp}.shp"
    gdf.to_file(vehicles_filename)
    route_gdf.to_file(route_filename)

    # Plot the GeoDataFrames on OpenStreetMap background
    fig, ax = plt.subplots(figsize=(10, 10))
    ctx.add_basemap(ax, zoom=12)  # Adjust zoom level as needed
    gdf.plot(ax=ax, marker='o', color='red', markersize=5)
    route_gdf.plot(ax=ax, color='blue', linewidth=1)
    plt.show()

def run_for_an_hour():
    current_time = datetime.datetime.now()
    next_hour = current_time.replace(second=0, microsecond=0, minute=0) + datetime.timedelta(hours=1)
    date_to_fetch = next_hour

    for i in range(60):  # 60 intervals of 1 minute each for one hour
        schedule_time = date_to_fetch + datetime.timedelta(minutes=i)
        schedule.every().day.at(schedule_time.strftime("%H:%M")).do(fetch_and_save_vehicle_data, date=date_to_fetch)

    while True:
        schedule.run_pending()
        time.sleep(0.5)

run_for_an_hour()
