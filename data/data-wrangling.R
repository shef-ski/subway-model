library(dplyr)
library(stringr)
library(readr)
library(lubridate)
library(ggplot2)
library(purrr)
library(fs) 

INPUT_FILE_RIDERSHIP <- "./MTA_Subway_Hourly_Ridership__Beginning_2025.csv"
INPUT_FILE_LINES <- "./MTA_Subway_Stations.csv"
DIRECTION_ESTIMATES <- "MTA_Subway_Origin-Destination_Ridership_Estimate__Beginning_2025.csv"

lines <- read_delim(INPUT_FILE_LINES, skip = 0, col_names = TRUE)

raw_data <- read_delim(INPUT_FILE_RIDERSHIP, skip = 0, col_names = TRUE)

# Aggregate by hour and sum up ticket types (does not matter for our model)
agg_ridership <- raw_data %>%
  group_by(transit_timestamp, station_complex) %>%
  summarise(ridership = sum(ridership, na.rm = TRUE), .groups = "drop") %>%
  select(transit_timestamp, station_complex, ridership)

# Parse timestamp
data_timestamp_parsed <- agg_ridership %>%
  mutate(
    transit_timestamp_parsed = mdy_hms(transit_timestamp), 
    month = month(transit_timestamp_parsed, label = TRUE),
    weekday = wday(transit_timestamp_parsed, label = TRUE),
    hour = hour(transit_timestamp_parsed)
  ) %>%
  filter(as.numeric(month) < 5)

# select example station
example_station <- data_timestamp_parsed %>%
  filter(station_complex=="Grand Central-42 St (S,4,5,6,7)")

# Plots to check for nomal distribution
subset_data <- example_station %>%
  filter(hour %in% c(17)) 

ggplot(subset_data, aes(sample = ridership)) +
  stat_qq() +
  stat_qq_line(color = "red") +
  facet_grid(weekday ~ hour, labeller = label_both) +
  labs(
    title = "QQ Plots of Ridership by Month, Weekday, and Hour",
    x = "Theoretical Quantiles",
    y = "Sample Quantiles"
  ) +
  theme_minimal(base_size = 10)

# export lookup table for mean and stdev
lookup_table_month_day <- data_timestamp_parsed %>%
  group_by(station_complex, month, weekday, hour) %>%
  summarise(
    mean_ridership = mean(ridership, na.rm = TRUE),
    sd_ridership = sd(ridership, na.rm = TRUE),
    .groups = "drop"
  )

lookup_table_day <- data_timestamp_parsed %>%
  group_by(station_complex, weekday, hour) %>%
  summarise(
    mean_ridership = mean(ridership, na.rm = TRUE),
    sd_ridership = sd(ridership, na.rm = TRUE),
    .groups = "drop"
  )