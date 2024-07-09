
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:38:51 2024

@author: noamgal
"""

#!/usr/bin/env python3
import requests
import geopandas as gpd
from shapely.geometry import Point
import datetime
import matplotlib.pyplot as plt
import schedule
import time

def fetch_and_save_vehicle_data():
    api_dict = {
        'Capital Bikeshare': 'https://gbfs.capitalbikeshare.com/gbfs/en/free_bike_status.json',
        'Lime Micromobility (including Jump bikes)': 'https://data.lime.bike/api/partners/v1/gbfs/washington_dc/free_bike_status.json',
        'Spin': 'https://web.spin.pm/api/gbfs/v1/washington_dc/free_bike_status'
    }
    vehicle_info_list = []

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

            for vehicle in vehicles_data:
                lon = vehicle.get('lon')
                lat = vehicle.get('lat')
                bike_id = vehicle.get('bike_id') or vehicle.get('id')
                is_reserved = vehicle.get('is_reserved')
                is_disabled = vehicle.get('is_disabled')
                
                # Check for valid coordinates
                if lon is None or lat is None or not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
                    print(f"Invalid coordinates for vehicle {bike_id} from {company}: lon={lon}, lat={lat}")
                    continue
                
                vehicle_info_list.append({
                    'company': company,
                    'lon': lon,
                    'lat': lat,
                    'bike_id': bike_id,
                    'is_reserved': is_reserved,
                    'is_disabled': is_disabled
                })
            print(f"Successfully processed data from {company}")
        except Exception as e:
            print(f"Error processing data from {company}: {e}")

    if vehicle_info_list:
        geometry = [Point(vehicle['lon'], vehicle['lat']) for vehicle in vehicle_info_list]
        gdf = gpd.GeoDataFrame(vehicle_info_list, geometry=geometry, crs="EPSG:4326")
        #print(len(gdf))
        # Generate unique filename with date and time
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        vehicles_filename = f"C:/Users/Owner/Desktop/Noam-Gal/Locs-only/vehicles_{timestamp}.shp"
        # Save the GeoDataFrame as shapefile
        gdf.to_file(vehicles_filename)

        # Plot the GeoDataFrame on OpenStreetMap background
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        ax = world.plot(color='white', edgecolor='black')
        gdf.plot(ax=ax, marker='o', color='red', markersize=5)
        plt.show()
    else:
        print("No valid vehicle data to plot.")


def run_scheduled_task():
    print(f"Running task at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_and_save_vehicle_data()

def schedule_tasks():
    start_date = datetime.date.today()
    current_time = datetime.datetime.now().time()

    for day in range(4):  # 0, 1, 2, 3 (4 days)
        for hour in range(24):
            # For the current day, only schedule future tasks
            if day == 0 and datetime.time(hour, 0) <= current_time:
                continue
            
            schedule.every().day.at(f"{hour:02d}:00").do(run_scheduled_task).tag(f'day_{day}')

    end_time = start_date + datetime.timedelta(days=4)
    while datetime.date.today() < end_time:
        schedule.run_pending()
        time.sleep(60)
        
        now = datetime.datetime.now()
        if now.time() > datetime.time(23, 1):
            day_number = (now.date() - start_date).days
            schedule.clear(f'day_{day_number}')
        
    print("All scheduled tasks for 4 days completed.")
    
if __name__ == "__main__":
    schedule_tasks()
     
