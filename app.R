library(shiny)
library(DT)
library(shinythemes)
library(wordcloud2)
library(ggwordcloud)
library(bslib)
library(leaflet)
library(geojsonio)
library(ggplot2)
library(dplyr)
library(lubridate)
library(sp)
library(here)

load(file = here('data/counties_geojson.RData'))
sentiment_df <- read.csv(here("data/sentiment_output.csv"), stringsAsFactors = FALSE)
sentiment_df$created_at.x <- ym(sentiment_df$created_at.x)

# Define server logic required to draw a histogram
server <- function(input, output, session){
  # --------------------------------------------------------------------------

  # Data Sources
  # --------------------------------------------------------------------------
  d1 <- reactive({
    fileOption <- input$fileOption
    if (fileOption == "Pasco"){
      file <- "non_geo_tags_RedTide_Pasco.csv"
    }
    else if (fileOption == "Tampa"){
      file <- "non_geo_tags_RedTide_Tampa.csv"
    }
    else if (fileOption == "Sarasota"){
      file <- "non_geo_tags_RedTide_Sarasota.csv"
    }
    else if (fileOption == "Pinellas"){
      file <- "non_geo_tags_RedTide_Pinellas.StPete.csv"
    }

    df <- read.csv(here(paste0('data/', file)))
    df$frequency <- as.integer(df$frequency)
    df <- df[order(-df$frequency),]
    df <- head(df, 30)

    return(df)

  })

  tweets <- reactive({
    fileOption <- input$fileOption

    if (fileOption == "Pasco"){
      file <- "RedTide_Pascotop3Tweets.csv"
    }
    else if (fileOption == "Tampa"){
      file <- "RedTide_Tampatop3Tweets.csv"
    }
    else if (fileOption == "Sarasota"){
      file <- "RedTide_Sarasotatop3Tweets.csv"
    }
    else if (fileOption == "Pinellas"){
      file <- "RedTide_Pinellas.StPetetop3Tweets.csv"
    }

    read_tweets_file <- read.csv(here(paste0('data/', file)))
    read_tweets_file$date <- ymd_hms(read_tweets_file$date)

    return(read_tweets_file)

  })

  sentiment_df <- reactive({
    fileOption <- input$fileOption
    if (fileOption == "Pasco"){
      file <- "RedTide_Pasco_sentiment_output.csv"
    }
    else if (fileOption == "Tampa"){
      file <- "RedTide_Tampa_sentiment_output.csv"
    }
    else if (fileOption == "Sarasota"){
      file <- "RedTide_Sarasota_sentiment_output.csv"
    }
    else if (fileOption == "Pinellas"){
      file <- "RedTide_Pinellas.StPete_sentiment_output.csv"
    }

    read_file <- read.csv(here(paste0('data/', file)))
    read_file$created_at.x <- ym(read_file$created_at.x)

    return(read_file)

  })

  selected_county_name <- reactive({ input$fileOption })
  selected_year <- reactive({ input$timeFrame })

  population <- reactive ({
    fileOption <- input$fileOption
    if (fileOption == "Pasco"){
      residents <- '584,067'
    }
    else if (fileOption == "Tampa"){
      residents <- '387,050'
    }
    else if (fileOption == "Sarasota"){
      residents <- '54,764'
    }
    else if (fileOption == "Pinellas"){
      residents <- '956,615'
    }

    return(residents)

  })

  # --------------------------------------------------------------------------


  # Tweets Table
  # --------------------------------------------------------------------------
  table_data <- reactive({
    year <-  input$timeFrame
    tweets_data <- tweets()
    tweets_data <- tweets_data %>% filter(year(date) == year)
    tweets_data <- tweets_data[order(tweets_data$popularity_weight, decreasing = TRUE), ]
    tweets_data$date <- format(tweets_data$date, "%Y-%m")
    tweets_data <- tweets_data[, -c(1, 3)]
    colnames(tweets_data) <- c("Popularity Weight", "Tweet Text", "Date")

    tweets_data <- tweets_data[!duplicated(tweets_data), ]

    return(tweets_data)

  })

  output$tweets_table <- renderDT({
    tab <- datatable(table_data() ,
                     caption = paste('Table 1: Popular Tweets For ', selected_county_name()),
                     options = list(
                       searchHighlight = TRUE,
                       searchCols = list(list(
                         searchRegex = TRUE,
                         searchValue = "Search Tweets"
                       ))
                     )
    ) %>%
      formatStyle(
        'Tweet Text', 'font-weight' = 'bold', 'font-size' = '14px',
        'text-align' = 'left'
      ) %>%
      formatStyle(
        'Popularity Weight', 'color' = '#17BF63', 'font-weight' = 'bold',
        'font-size' = '14px',  'text-align' = 'left'
      )%>%
      formatStyle(
        'Date', 'color' = '#17BF63', 'font-weight' = 'bold',
        'font-size' = '14px',  'text-align' = 'left'
      )

    return(tab)

  })
  # --------------------------------------------------------------------------

  # MAP:
  # --------------------------------------------------------------------------

  set.seed(1234)
  output$map <- renderLeaflet({
    COUNTY <- ifelse(input$fileOption == "Tampa", "Hillsborough", selected_county_name())
    content <- paste(sep ="<br/>",
                     "<b>County: </b>", COUNTY,
                     "<b>Residents: </b>", population()
    )

    county_poly <- subset(counties_geojson, NAME == COUNTY)
    lat <- coordinates(county_poly)[, 2]
    lon <- coordinates(county_poly)[, 1]

    m <- leaflet(counties_geojson) %>%
      addTiles() %>%
      addPolygons(fillOpacity = 0.5,
                  fillColor = ifelse(counties_geojson$NAME == COUNTY, "blue", "red"),
                  color = "#BDBDBD",
                  weight = 1
      ) %>%
      addProviderTiles(providers$CartoDB.Positron)%>%
      addPopups( lon, lat, content,
                 options = popupOptions(closeButton = TRUE)
      )

    return(m)

  })
  # --------------------------------------------------------------------------

  # Non-Geo Tags Word Cloud:
  # --------------------------------------------------------------------------
  output$myplot1 <- renderWordcloud2({
    p1 <- wordcloud2(d1(), size=0.8, minRotation = -pi/6, maxRotation = -pi/6)
    return(p1)
  })
  output$print1  = renderPrint(input$myplot1_clicked_word)
  # --------------------------------------------------------------------------

  # Word Cloud Paragraph:
  # --------------------------------------------------------------------------

  output$wordCloud_paragraph <- renderText({

    data <- d1()

    most_common_tag <- data$word[which.max(data$frequency)]

    paragraph <- paste("The word cloud represents a collection of the top 30 Non
                       Geo hashtags from Tweets about Red Tide in",
                       selected_county_name(), "during ", selected_year(),
                       ". The most common hashtag is '", most_common_tag, "', appearing",
                       max(data$frequency), "times. The word cloud provides a visual
                       representation of the relative frequencies of different
                       hashtags in the dataset.")

    return(paragraph)

  })

  # --------------------------------------------------------------------------


  # Sentiment Plot
  # --------------------------------------------------------------------------
  filteredData <- reactive({
    year <-  input$timeFrame
    result <- sentiment_df() %>% filter(year(created_at.x) == year)

    return(result)

  })

  output$sentimentPlot <- renderPlot({
    filtered_df <- filteredData()
    theme_set(theme_minimal())

    plot <- ggplot(filtered_df, aes(x = created_at.x, y = Sentiment, fill = Sentiment)) +
      geom_hline(yintercept = 0, linetype = 'dashed') +
      geom_point(color = 'darkgrey', size = 4, position = position_dodge2(width = 4), shape = 21) +
      scale_fill_gradient2(low = 'red', high = 'green', midpoint = 0, limits = c(-1, 1)) +
      scale_color_gradient2(low = 'red', high = 'green', midpoint = 0, limits = c(-1, 1)) +
      geom_smooth(aes(color = ..y..), method = "loess", se = T, linewidth = 2, alpha = 0.2) +
      scale_y_continuous(limits = c(-1, 1)) +
      labs(title = "Sentiment Distribution",
           x = NULL,
           y = "Sentiment",
           color = "Sentiment") +
      scale_x_date(date_labels = "%b", date_breaks = "month") +
      theme(
        plot.title = element_text(size = 18, face = "bold"),
        panel.grid.minor = element_blank(),
        axis.title.x = element_text(size = 14),
        axis.title.y = element_text(size = 14),
        axis.text.x = element_text(size = 12),
        axis.text.y = element_text(size = 12),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12)
      )

    return(plot)

  })

  # --------------------------------------------------------------------------


  # Sentiment Paragraph
  # --------------------------------------------------------------------------

  output$sentimentPlotDescription <- renderText({
    filtered_df <- filteredData()

    total_months <- length(unique(filtered_df$created_at.x))
    max_sentiment <- max(filtered_df$Sentiment)
    min_sentiment <- min(filtered_df$Sentiment)
    avg_sentiment <- mean(filtered_df$Sentiment)
    num_positive <- sum(filtered_df$Sentiment > 0)
    num_negative <- sum(filtered_df$Sentiment < 0)

    paragraph <- paste("The sentiment plot visualizes the distribution of
                       sentiment over time. It shows the variation in sentiment
                       scores across", total_months, "months of data.
                       The sentiment scores range from -1 to 1, where -1
                       represents negative sentiment, 0 represents neutral
                       sentiment, and 1 represents positive sentiment. The plot
                       includes a line graph that connects the sentiment scores
                       for each month, allowing us to observe trends and patterns
                       in sentiment over time. Additionally, a smooth line has
                       been added using the loess method to provide a smoothed
                       representation of the sentiment distribution.

                     Statistics:
                     - Maximum Sentiment Score: ", max_sentiment,"
                     - Minimum Sentiment Score: ", min_sentiment,"
                     - Average Sentiment Score: ", avg_sentiment,"
                     - Number of Positive Sentiments: ", num_positive,"
                     - Number of Negative Sentiments: ", num_negative,"
                     ")

    return(paragraph)

  })

}

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

shinyApp(ui, server)

