library(dplyr)
library(sp)
library(here)

# process counties geojson to include only those that are relevant
counties_geojson <- geojson_read("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/FL-12-florida-counties.json", what = "sp") %>%
  subset(NAME %in% c('Pasco', 'Hillsborough', 'Pinellas', 'Sarasota'))

save(counties_geojson, file = here('data/counties_geojson.RData'))
