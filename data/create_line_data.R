library(dplyr)
library(stringr)
library(readr)
library(lubridate)
library(ggplot2)
library(purrr)
library(fs) 

INPUT_FILE_LINES <- "./MTA_Subway_Stations.csv"
DIRECTION_ESTIMATES_PATH <- "MTA_Subway_Origin-Destination_Ridership_Estimate__Beginning_2025.csv"
args <- commandArgs(trailingOnly = TRUE)

selected_route_id = "G"
selected_line_name = "Crosstown"

if(is.null(selected_line_name)){
  stop("Script not called with a line name")
}

lines <- read_delim(INPUT_FILE_LINES, skip = 0, col_names = TRUE)

if (!(selected_line_name %in% lines$Line)) {
  stop(paste("Line name", line_name, "not found in file"))
}

gtfs_path <- "./line_data"

stops <- read_csv(file.path(gtfs_path, "stops.txt"))
routes <- read_csv(file.path(gtfs_path, "routes.txt"))
trips <- read_csv(file.path(gtfs_path, "trips.txt"))
stop_times <- read_csv(file.path(gtfs_path, "stop_times.txt"))

trip_routes <- trips %>%
  inner_join(routes, by = "route_id")

trips_for_selected_route <- trip_routes %>%
  filter(route_id == selected_route_id)

# Pick one representative trip per route_id to avoid duplicates
representative_trips <- trip_routes %>%
  group_by(route_id) %>%
  slice(1) %>%
  ungroup()

# Get stop sequences for each route
ordered_stops <- representative_trips %>%
  select(route_id, trip_id, route_short_name) %>%
  inner_join(stop_times, by = "trip_id") %>%
  inner_join(stops, by = "stop_id") %>%
  arrange(route_id, trip_id, stop_sequence) %>%
  rename(gtfs_stop_id = stop_id) %>%
  mutate(
    gtfs_stop_id = substr(gtfs_stop_id, 1, nchar(gtfs_stop_id) - 1),
    sortorder = row_number()
  ) %>%
  filter(route_id == selected_route_id)

direction_along_sortorder=1
direction_against_sortorder=0

stops_for_selected_route <- stop_times %>%
  filter(trip_id %in% trips_for_selected_route$trip_id) %>%
  left_join(trips, by="trip_id") %>%
  mutate(stop_id = substr(stop_id, 1, nchar(stop_id) - 1)) %>%
  select(stop_id, service_id, direction_id, arrival_time, departure_time)

lines_cleaned <- lines %>%
  mutate(gtfs_stop_id = `GTFS Stop ID`) %>%
  select(Line, gtfs_stop_id, complex_id=`Complex ID`)

complex_stations <- ordered_stops  %>%
  left_join(lines_cleaned, by="gtfs_stop_id") %>%
  filter(Line==selected_line_name)

line_metadata <- complex_stations %>%
  mutate(sortorder = sortorder - min(sortorder, na.rm = TRUE)) %>%
  select(stop_name,Line, sortorder, complex_id, gtfs_stop_id)

sortorder_complex_lookup <- line_metadata %>%
  select(sortorder, complex_id, stop_id = gtfs_stop_id)

dir.create("line_outputs")
dir.create(paste("line_outputs",selected_line_name, sep="/"))

filename <- paste0("line_outputs/", selected_line_name, "/line_metadata.csv")
write_csv(line_metadata %>% select(stop_name,Line, sortorder), filename)

train_arrival_lookup_table <- stops_for_selected_route %>%
  left_join(sortorder_complex_lookup, by="stop_id") %>%
  mutate(direction_id = if_else(direction_id == 0, -1, direction_id)) %>%
  filter(!is.na(sortorder)) %>%
  select(service_id, direction=direction_id, arrival_time, departure_time, station_id=sortorder)

filename <- paste0("line_outputs/", selected_line_name, "/train_arrival_lookup_table.csv")
write_csv(train_arrival_lookup_table, filename)

# direction_estimates

direction_estimates <- read_delim(DIRECTION_ESTIMATES_PATH, skip = 0, col_names = TRUE) %>%
  select(Year, Month, day_of_week = "Day of Week", hour_of_day = "Hour of Day", origin="Origin Station Complex ID", destination="Destination Station Complex ID", estimated_ridership="Estimated Average Ridership", origin_name="Origin Station Complex Name")

filtered_df <- direction_estimates %>%
  filter(
    origin %in% complex_stations$complex_id &
      destination %in% complex_stations$complex_id
  ) %>%
  select(Year,Month,day_of_week,hour_of_day,origin_complex=origin,destination_complex=destination, estimated_ridership) %>%
  left_join(sortorder_complex_lookup, by = c("origin_complex" = "complex_id")) %>%
  rename(origin_sortorder = sortorder) %>%
  left_join(sortorder_complex_lookup, by = c("destination_complex" = "complex_id")) %>%
  rename(destination_sortorder = sortorder) %>%
  select(Year,Month,day_of_week,hour_of_day,origin=origin_sortorder, destination=destination_sortorder, estimated_ridership)

filename <- paste0("line_outputs/", selected_line_name, "/direction_estimates.csv")
write_csv(filtered_df, filename)