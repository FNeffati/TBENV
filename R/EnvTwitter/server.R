#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(ggwordcloud)
library(rsconnect)
library(wordcloud2)
library(DT)

library(leaflet)
library(geojsonio)
library(sp)

library(tidyverse)



counties_geojson <- geojson_read("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/FL-12-florida-counties.json", what = "sp")


# Define server logic required to draw a histogram
shinyServer(function(input, output) {
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
    
    df <- read.csv(file)
    df$frequency <- as.integer(df$frequency)
    df <- df[order(-df$frequency),]
    df <- head(df, 30)
    df
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
    
    read_tweets_file <- read.csv(file)
    read_tweets_file$date <- ymd_hms(read_tweets_file$date)
    read_tweets_file
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
    
    read_file <- read.csv(file)
    read_file$created_at.x <- ym(read_file$created_at.x)
    read_file
  })
  
  selected_county_name <- reactive({ input$fileOption })
  selected_year <- reactive({ input$timeFrame })
  
  population <- reactive ({ fileOption <- input$fileOption
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
    tweets_data
  })
  
  output$tweets_table <- renderDT({
    datatable(table_data() ,
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
    
    
    leaflet(counties_geojson) %>%
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
  })
  # --------------------------------------------------------------------------
  
  # Non-Geo Tags Word Cloud: 
  # --------------------------------------------------------------------------
  output$myplot1 <- renderWordcloud2({
    p1 <- wordcloud2(d1(), size=0.8, minRotation = -pi/6, maxRotation = -pi/6)
    p1
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
    paragraph
    
  })
  
  # --------------------------------------------------------------------------
  
  
  # Sentiment Plot
  # --------------------------------------------------------------------------
  filteredData <- reactive({
    year <-  input$timeFrame
    result <- sentiment_df() %>% filter(year(created_at.x) == year)
    result
  })
  
  output$sentimentPlot <- renderPlot({
    filtered_df <- filteredData()
    theme_set(theme_minimal())
    
    plot <- ggplot(filtered_df, aes(x = created_at.x, y = Sentiment, color = Sentiment)) +
      geom_smooth(method = "loess", se = FALSE) +
      labs(title = "Sentiment Distribution",
           x = "Month",
           y = "Sentiment",
           color = "Sentiment") +
      scale_x_date(date_labels = "%b", date_breaks = "month") +
      theme(
        plot.title = element_text(size = 18, face = "bold"),
        axis.title.x = element_text(size = 14),
        axis.title.y = element_text(size = 14),
        axis.text.x = element_text(size = 12),
        axis.text.y = element_text(size = 12),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12)
      )
    plot
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
    
    paragraph
  })
  
})







