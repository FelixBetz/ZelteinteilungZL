"""This module parses a input CSV list and generate some maps"""
import os

import folium
from folium.plugins import MarkerCluster
from folium import plugins

import pgeocode

OUTPUT_DIR_PATH = "./output_maps/"


def calc_middle_point(arg_locations):
    """calc middle point of the marker locations"""
    # calculate 'middle_point'
    lat_min = min(arg_locations, key=lambda loc: float(loc[0]))[0]
    lat_max = max(arg_locations, key=lambda loc: float(loc[0]))[0]

    long_min = min(arg_locations, key=lambda loc: float(loc[1]))[1]
    long_max = max(arg_locations, key=lambda loc: float(loc[1]))[1]

    loc_long = (long_max + long_min) / 2
    loc_lat = (lat_max + lat_min) / 2

    return (loc_lat, loc_long)


def generate_maps(zip_codes):
    """geneartes heatmap and markermaps by zipcodes"""
    # generate output directory

    if not os.path.exists(OUTPUT_DIR_PATH):
        os.makedirs(OUTPUT_DIR_PATH)

    # Get longitude and latitude for each zipcode
    marker_locations = []
    for zip_code in zip_codes:
        zip_code_coords = pgeocode.Nominatim("de")\
            .query_postal_code(zip_code[0])
        marker_locations.append(
            [zip_code_coords["latitude"], zip_code_coords["longitude"]]
        )

    middle_point = calc_middle_point(marker_locations)

    ###########################################################################################
    # genearte makers map
    map_object = folium.Map([middle_point[0], middle_point[1]],
                            zoom_start=7, tiles="Stamen Toner")
    map_cluster = MarkerCluster(name="Zeltlager Teilnehmer").add_to(map_object)

    # create markers form PLZ coordinates array
    for i, pnt in enumerate(marker_locations):
        zipcode = zip_codes[i][0]
        location = zip_codes[i][1]

        folium.Marker(
            location=[pnt[0], pnt[1]],
            popup=f"{zipcode} {location}\r\n({pnt[0]}°| {pnt[1]}°)",
        ).add_to(map_cluster)

    minimap = plugins.MiniMap()
    map_object.add_child(minimap)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(map_object)

    # loc_map = folium.LayerControl().add_to(map_object)

    # save the map object as html
    map_object.save(OUTPUT_DIR_PATH + "markermap.html")

    ###########################################################################################
    # genearte heatmap
    heatmap = folium.Map(
        [middle_point[0], middle_point[1]], zoom_start=7, tiles="Stamen Toner"
    )  # tiles="Stamen Toner"
    plugins.HeatMap(marker_locations).add_to(heatmap)
    heatmap.save(OUTPUT_DIR_PATH + "heatmap.html")
