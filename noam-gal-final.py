#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:58:23 2024

@author: noamgal
"""

"""input - triplets of origin, destination, length of road.
    will finish accepting input when "#" is inputted.
    returns a list of tuples of all the roads in the city."""
def getCityMap():
    road = ()
    c_map = []
    # appends inputted road tuples until the # is inputted
    # all road inputs must be of format (origin (string), destination (string), length of road (integer))
    while '#' not in road:
        road = input('Enter a road triplet as a tuple: ')
        # checks if a # has been inputted
        if '#' in road:
            break
        # uses eval to convert the string input into a tuple format and appends the tuple to the map list
        c_map.append(eval(road))
    return c_map

"""2 lists of locations representing paths. returns a sorted list (by alphabet)
of all intersecting locations of the 2 paths."""
def intersections(path1, path2):
    # creates list of locations in both lists using list comprehension
    intersect = [loc for loc in path1 if loc in path2]
    # returns list of intersections sorted in alphabetical order
    return sorted(intersect)

    
"""returns a string representaion of a path a->b->c"""
def string_path(path):
    str_path = ''
    # adds every index of the path, followed by -> to a string, except the final element which will be added outside of the loop
    for n in range(len(path)-1):
        str_path += path[n]
        str_path +='->'
    # adds the final element to the string path
    str_path += path[-1]
    return str_path


"""parm - a list of tuples of roads ->
    returs a dictionary where each key is a tuple (origin, destination)
    and the value is the length of the road."""
def buildCityDict(city_map_list):
    c_dict = {}
    # iterates through the list of tuples, and converts each tuple to a key-value pair in the new dictionary
    # each key is a tuple of the origin and destination, both strings, and the value is the length, an int
    for tup in city_map_list:
        c_dict[(tup[0],tup[1])] = tup[2]
    return c_dict

"""parm - list of locations in the city, and the city dictionay.
    returns the length of a drive through the path"""
def lengthOfDrive(path, city_dict):
    length = 0
    # for each index in the list, except the last, adds the distance to the next index to path length
    for n in range(len(path)-1):
        length += city_dict[(path[n], path[n+1])]
    return length
    

"""parm - list of list of paths, and city dictionay.
    returns the shortest path (by length) of the list."""
def shortestPath(paths, city_dict):
    # initiatlizes the best length as the length of the first path
    best_length = lengthOfDrive(paths[0], city_dict)
    best_path = paths[0]
    for p in paths:
        # skips the first path because that was initialized as best
        if p == paths[0]:
            continue
        # if path is shorter than the best prior path, it becomes the best path
        if lengthOfDrive(p, city_dict) < best_length:
            best_path = p
            best_length = lengthOfDrive(p, city_dict)
        # if the path is the same length as the best prior path, if it has fewer indices, it becomes the best path
        elif lengthOfDrive(p, city_dict) == best_length:
            if len(p) < len(best_path):
                best_path = p    
    return best_path

"""parm - city dictionary.
    returns a new dictionary where every key is an origin location,
    and every value is a list of tuples of all the roads leading out of that origin."""
def buildOriginDict(city_dict):
    origin_dict = {}
    origins = set()
    # adds all origins to a set for use in constructing the origin dictionary
    for key in city_dict:
        origins.add(key[0])
    # for each location, iterates through all the paths and constructs a list of paths where it is the origin 
    # appends the paths as a list of destinations, and makes that list the origin's value in the dictionary
    for loc in sorted(origins):
        destinations = []
        for key in city_dict:
            if key[0] == loc:
                destinations.append(key)
        origin_dict[loc] = destinations
    return origin_dict


"""parm - an origin location, a destination location, and an origin dictionary.
    return a list of list of all possible paths from origin to destination."""
def getAllPaths(origin, destination, origin_dict):
    curr_path = [[origin]]
    paths = []

    while curr_path:
        path = curr_path.pop()
        current = path[-1]

        if current == destination:
            paths.append(path)

        if current not in origin_dict:
            continue

        for road in origin_dict[current]:
            if road[1] not in path:
                curr_path.append(path + [road[1]])
    return paths

#Explanation of getAllPaths():
'''The functin returns a list of all paths from the specified origin to the specified destination.
The list of paths returned is therefore a list of lists.
It creates this list with a while loop using a variable, curr_path, that is initialized as a list containing a list with only one element, the origin.

While curr_path is non-empty, the loop repeats the following steps:
    We check to see if the last list in curr_path, which we name path, is a path to the destination by checking 
    if the last element in it, whuch we name current, is the destination.
    If it is, we add it to our list of good paths called paths.
    Next, we check if there are any roads leading out of current by checking if it is in the origin_dict:
        if there aren't any, we continue the loop and pop out a new path from curr_path to check
    If there are roads with current as the origin:
        For each of those roads:
            we add the destination to our current path, 
            and add that newly elongated path to the curr_path list of potential paths.
   
Th while loop continues until every possible path from origin to destination is found, 
because it keep checking all possible roads to create all possible paths that may be good
until it runs into locations with no roads.
After the loop finds all the good paths, we return the list of good paths (paths).'''



""" parm - a string representation of a path and the length of the path.
    return a new road - a tuple: (origin, destination, new_length)
    the new length will be half the length of the path rounded down to the closest integer."""

import math
def createNewRoad(path_str, length):
    # turns the path_string into a list of locations
    path_split = path_str.split('->')
    # creates a tuple with the new road and the length divided by 2 rounded down to the nearest int
    new_path = (path_split[0],path_split[-1], math.floor(length/2))
    return new_path

city_map_list = [("A","D",5), ("A","E",2), ("A","B",1), ("B","D",2),("B","H",7),
                 ("C","G",4), ("G","A",8), ("D","C",1), ("D","F",2), ("E","G",3),
                 ("E","I",5), ("E","H",5), ("E","F",4), ("F","J",7), ("G","I", 1),
                 ("G","K",8), ("H","I",2), ("H","K",3), ("I","K",1), ("J","K",5),
                 ("K","F",10), ("K","I",3), ("F","D",4)]

city_dict = buildCityDict(city_map_list)
print("---- print city dictionry ----")
print(city_dict)
origin_dict = buildOriginDict(city_dict)
print("---- print origin dictionry ----")
print(origin_dict)
all_paths = getAllPaths("A", "K", origin_dict)
print("---- print all paths from A to K ----")
print(all_paths)
shortest_path = shortestPath(all_paths, city_dict)
print("---- print the shortest path from A to K ----")
print(shortest_path)
length = lengthOfDrive(shortest_path, city_dict)
print("---- print the length of the shortes path from A to K ----")
print(length)
print("---- print intersection of paths ----")
print(intersections(all_paths[0], all_paths[1]))
str_path = string_path(shortest_path)
print("---- print string representation of path ----")
print(str_path)
print("---- print new road ----")
print(createNewRoad(str_path, length))
