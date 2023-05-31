library(shiny)
library(readr)
library(DT)
library(shinythemes)
library(wordcloud2)
library(bslib)
library(leaflet)
library(geojsonio)
library(ggplot2)
library(dplyr)
library(lubridate)
library(here)

# Load county data
counties_geojson <- geojson_read("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/FL-12-florida-counties.json", what = "sp")
sentiment_df <- read.csv(here("data/sentiment_output.csv"), stringsAsFactors = FALSE)
sentiment_df$created_at.x <- ym(sentiment_df$created_at.x)



# Define UI
ui <- fluidPage(

  theme = bs_theme(version = 4, bootswatch = "minty"),
  tags$style(HTML("hr {border-top: 5px solid #000000;}"),
             type="text/css",
             ".hr  { margin-top: 10px; margin-bottom: 10px; }"
             ),
  tags$style(type="text/css",
             ".my-row  { margin-top: 200px; margin-bottom: 150px; padding-right: 45px }
              .my-row2 { margin-bottom: 200px; }
              .wordCloud_paragraph, .map {margin-top: 200px;}
              .wordcloud, .sentiPlot {margin-top: 100px;}
              .wordCloud_paragraph, .sentimentPlotDescription {font-size: 25px; margin-top: 200px; margin-bottom: 150px;}
             "),


  #Navbar structure for UI
  navbarPage("The Environmentalist", theme = shinytheme("lumen"),
             tabPanel("Home", fluid = TRUE,
                      # ------------------------------------------------------
                      fluidRow(class = "my-row",
                        tags$head(
                          tags$style(
                            HTML(
                                "
                                  h1 {
                                    font-size: 100px;
                                    text-align: center;
                                    padding-top: 100px;
                                  }
                                  h3 {
                                    padding-right: 450px;
                                    text-align: center;
                                  }
                                "
                                )
                              )
                            ),
                        column(12,
                               column(8, h1("The Environmentalist"), h3("Where you get your latest Red Tide news")),
                               column(4,
                                 img(src="marine.png", align = "left",height='600px',width='600px')
                                      )
                        )
                      # ------------------------------------------------------
                      ),
                      fluidRow(class = "my-row1",
                        column(12,
                               hr(),
                          column(3, offset=1,

                              selectInput("fileOption", "Select Location", choices = c("Pasco", "Tampa", "Sarasota", "Pinellas"))

                          ),
                          column(3, offset=1,

                              selectInput("accountType", "Select Account Type", choices = c("Everyone", "Celebrity", "Government Officials", "Verified"))


                          ),
                          column(3, offset=1,

                                 selectInput("timeFrame", "Select Time Frame", choices = c(unique(year(sentiment_df$created_at.x)))),
                                )
                            )
                        ),
                      # ------------------------------------------------------
                      fluidRow(class = "my-row2",
                        column(12,
                               hr(),
                          column(5,
                                 class = "map",
                                 leafletOutput("map")
                                 ),
                          column(7,
                                 DTOutput("tweets_table")

                          )
                        )
                      ),
                      # ------------------------------------------------------
                      fluidRow(class = "my-row2",
                        column(12,
                               hr(),
                          column(5,
                                 class = "wordCloud_paragraph",
                                 textOutput("wordCloud_paragraph")

                                ),
                          column(7,
                                 class = "wordcloud",
                                 wordcloud2Output("myplot1"),
                                 verbatimTextOutput("print1")
                          )
                        )
                      ),
                      # ------------------------------------------------------
                      fluidRow(
                        column(12,
                          hr(),
                          column(5,
                                 class="sentiPlot",
                                 plotOutput("sentimentPlot")),
                          column(7,
                                 class="sentimentPlotDescription",
                                 textOutput("sentimentPlotDescription")
                                 )
                        )
                      )
                   )
               )
        )

