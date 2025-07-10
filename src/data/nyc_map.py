import geopandas as gpd
from shapely.geometry import box

from src.subway.nyc_subway.nyc_subway_line import NycSubwayLine


class NycMap:
    """
    A class which holds a NYC Map and the coordinates of the relevant stations.

    The geo_df is geopandas dataframe which is an extension to a regular pandas df but
    with geographical information.
    """

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
        """Handle the coordinate reference system."""

        self.geo_df = self.geo_df.set_crs(epsg=2263, allow_override=True)
        self.geo_df = self.geo_df.to_crs(epsg=4326)

    def trim_map_to_stations_square(self, buffer=0.005):
        """
        Trims a GeoDataFrame to a square area encompassing station coordinates.

        Args:
            geo_df (gpd.GeoDataFrame): The input map GeoDataFrame
                (assumed to be in EPSG:4326).
            buffer (float): Buffer to add around the station extents
                (in decimal degrees).

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
        clipping_box_geom = box(
            square_min_lon, square_min_lat, square_max_lon, square_max_lat
        )

        try:
            self.geo_df = gpd.clip(self.geo_df, clipping_box_geom)
        except Exception as e:
            print(f"Error during clipping: {e}")
            print("Ensure the GeoDataFrame and clipping box are valid and overlap.")

        # Store the bounds for potential use in set_xlim/set_ylim
        square_bounds = (square_min_lon, square_max_lon, square_min_lat, square_max_lat)

        self.square_bounds = square_bounds
