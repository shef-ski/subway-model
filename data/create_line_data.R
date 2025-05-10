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
  mutate(sortorder = row_number()) %>%
  filter(route_id==selected_route_id)

lines_cleaned <- lines %>%
  mutate(gtfs_stop_id = paste(`GTFS Stop ID`, "S", sep="")) %>%
  select(Line, gtfs_stop_id, complex_id=`Complex ID`)

complex_stations <- ordered_stops  %>%
  left_join(lines_cleaned, by="gtfs_stop_id") %>%
  filter(Line==selected_line_name)

line_metadata <- complex_stations %>%
  mutate(sortorder = sortorder - min(sortorder, na.rm = TRUE)) %>%
  select(stop_name,Line, sortorder, complex_id)

dir.create("line_outputs")
dir.create(paste("line_outputs",selected_line_name, sep="/"))

filename <- paste0("line_outputs/", selected_line_name, "/line_metadata.csv")
write_csv(line_metadata, filename)

# direction_estimates

direction_estimates <- read_delim(DIRECTION_ESTIMATES_PATH, skip = 0, col_names = TRUE) %>%
  select(Year, Month, day_of_week = "Day of Week", hour_of_day = "Hour of Day", origin="Origin Station Complex ID", destination="Destination Station Complex ID", estimated_ridership="Estimated Average Ridership", origin_name="Origin Station Complex Name")

filtered_df <- direction_estimates %>%
  filter(
    origin %in% complex_stations$complex_id |
      destination %in% complex_stations$complex_id
  ) %>%
  select(Year,Month,day_of_week,hour_of_day,origin_complex=origin,destination_complex=destination, estimated_ridership)

filename <- paste0("line_outputs/", selected_line_name, "/direction_estimates.csv")
write_csv(filtered_df, filename)