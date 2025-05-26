import pandas as pd
import geopandas as gpd
from shapely.geometry import box

from src.subway.nyc_subway.nyc_subway_line import NycSubwayLine


def get_station_coords(target_station_name, stops_path):
    """
    Reads a stops.txt (CSV) file, finds a station by its name, and returns 
    its longitude and latitude as a pair of floats.

    It prioritizes entries with location_type=1 (typically representing a station)
    if multiple matches for the name exist.

    Args:
        target_station_name (str): The name of the station to search for.
        stops_path (str): The path to the stops.txt file.

    Returns:
        tuple: A tuple (longitude, latitude) as floats if the station is found 
               and coordinates are valid.
               Returns None if the station is not found, the file is not found,
               or if coordinates are missing/invalid.
    """

    # terrible hard coded fix because there are 2 stations named "Fulton St"
    if target_station_name == "Fulton St":
        print("Warning: hardcoded fix being applied")
        return -73.975375, 40.687119 

    # Read the CSV file.
    # We specify dtype for 'location_type' as str to handle empty values consistently.
    # Pandas might otherwise try to infer numeric types which can be tricky with mixed data.
    df = pd.read_csv(stops_path, dtype={'location_type': str,
                                             'stop_lat': str, 
                                             'stop_lon': str})

    # Filter by station name. This comparison is case-sensitive.
    # If case-insensitivity is needed, you could use:
    # matched_stations = df[df['stop_name'].str.lower() == target_station_name.lower()]
    matched_stations = df[df['stop_name'] == target_station_name]

    if matched_stations.empty:
        print(f"Station '{target_station_name}' not found in the file.")
        return None

    selected_station_row = None

    # Prioritize entries where location_type is '1' (typically a station)
    stations_with_type_1 = matched_stations[matched_stations['location_type'] == '1']

    if not stations_with_type_1.empty:
        selected_station_row = stations_with_type_1.iloc[0]  # Take the first match with location_type '1'
    else:
        # If no entry with location_type '1' is found for that name,
        # take the first match found, regardless of location_type.
        # This covers cases where a name might only be associated with platforms/stops.
        selected_station_row = matched_stations.iloc[0]

    # Extract latitude and longitude
    stop_lon_str = selected_station_row['stop_lon']
    stop_lat_str = selected_station_row['stop_lat']

    # Convert to float. Handle potential empty strings or non-numeric values.
    if pd.isna(stop_lon_str) or str(stop_lon_str).strip() == "":
        raise ValueError("Longitude is missing or empty.")
    if pd.isna(stop_lat_str) or str(stop_lat_str).strip() == "":
        raise ValueError("Latitude is missing or empty.")
        
    stop_lon = float(stop_lon_str)
    stop_lat = float(stop_lat_str)
    
    return stop_lon, stop_lat
 

class NycMap:
 
    square_bounds: tuple
    stations_lon: list
    stations_lat: list

    def __init__(self, shape_path: str, line: NycSubwayLine):
        self.geo_df = gpd.read_file(shape_path)
        self._handle_crs()

        self.line = line
        self._extract_lon_lat_list()

    def _extract_lon_lat_list(self):
        """Extract station lon lat values for better access."""

        self.stations_lon = []
        self.stations_lat = []

        for station in self.line.stations:
            self.stations_lon.append(station.lon)
            self.stations_lat.append(station.lat)

    def _handle_crs(self):
        # Handle the coordinate reference system
        self.geo_df = self.geo_df.set_crs(epsg=2263, allow_override=True) 
        self.geo_df = self.geo_df.to_crs(epsg=4326)

    def trim_map_to_stations_square(self,
                                    buffer=0.005):
        """
        Trims a GeoDataFrame to a square area encompassing station coordinates plus a buffer.

        Args:
            geo_df (gpd.GeoDataFrame): The input map GeoDataFrame (assumed to be in EPSG:4326).
            buffer (float): Buffer to add around the station extents (in decimal degrees).

        Returns:
            tuple: (gpd.GeoDataFrame, tuple)
                - The clipped GeoDataFrame.
                - A tuple (min_lon, max_lon, min_lat, max_lat) representing the
                bounds of the square clipping box.
                Returns (original_geo_df, None) if station lists are empty.
        """

        # 1. Determine the extent of stations
        min_lon_stations = min(self.stations_lon)
        max_lon_stations = max(self.stations_lon)
        min_lat_stations = min(self.stations_lat)
        max_lat_stations = max(self.stations_lat)

        # 2. Apply buffer
        min_lon_buffered = min_lon_stations - buffer
        max_lon_buffered = max_lon_stations + buffer
        min_lat_buffered = min_lat_stations - buffer
        max_lat_buffered = max_lat_stations + buffer

        # 3. Calculate the range (width and height) of the buffered extent
        lon_range = max_lon_buffered - min_lon_buffered
        lat_range = max_lat_buffered - min_lat_buffered

        # 4. Determine the side length of the square
        #    The square side will be the larger of the two ranges
        square_side_length = max(lon_range, lat_range)

        # 5. Calculate the center of the buffered station extent
        center_lon = (min_lon_buffered + max_lon_buffered) / 2
        center_lat = (min_lat_buffered + max_lat_buffered) / 2

        # 6. Calculate the coordinates for the square bounding box
        square_min_lon = center_lon - (square_side_length / 2)
        square_max_lon = center_lon + (square_side_length / 2)
        square_min_lat = center_lat - (square_side_length / 2)
        square_max_lat = center_lat + (square_side_length / 2)

        # 7. Create a bounding box polygon using Shapely
        #    The order is (minx, miny, maxx, maxy)
        clipping_box_geom = box(square_min_lon, square_min_lat, square_max_lon, square_max_lat)
        
        try:
            self.geo_df = gpd.clip(self.geo_df, clipping_box_geom)
        except Exception as e:
            print(f"Error during clipping: {e}")
            print("Ensure the GeoDataFrame and clipping box are valid and overlap.")

        # Store the bounds for potential use in set_xlim/set_ylim
        square_bounds = (square_min_lon, square_max_lon,
                         square_min_lat, square_max_lat)
        
        self.square_bounds = square_bounds
    