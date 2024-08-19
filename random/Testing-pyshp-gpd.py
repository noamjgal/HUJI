#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:21:49 2024

@author: noamgal
"""

import time
import shapefile
import geopandas as gpd

def time_pyshp_read(file_path):
    start_time = time.time()
    with shapefile.Reader(file_path) as sf:
        for shape in sf.iterShapes():
            pass  # Just iterate through shapes
    end_time = time.time()
    return end_time - start_time

def time_geopandas_read(file_path):
    start_time = time.time()
    gdf = gpd.read_file(file_path)
    end_time = time.time()
    return end_time - start_time

file_path = '/Users/noamgal/Downloads/NUR/celular1819_v1.3/Shape_files/1270_02.09.2021.shp'

pyshp_time = time_pyshp_read(file_path)
geopandas_time = time_geopandas_read(file_path)

print(f"PyShp time: {pyshp_time:.2f} seconds")
print(f"GeoPandas time: {geopandas_time:.2f} seconds")
print(f"PyShp is {geopandas_time / pyshp_time:.2f}x faster")