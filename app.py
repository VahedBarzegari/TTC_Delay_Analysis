import ast
import asyncio
from datetime import datetime
from pathlib import Path

import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import calendar
from folium.plugins import HeatMap
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly, render_altair, render_widget


from core_data_code import Bus_general_inf_dataframe

# ---- Global Styles ----
ui.markdown(
    """
    <style>
        /* Reduce Button Font Size */
        .btn { font-size: 12px !important; padding: 6px 10px;}
        
        /* Reduce Input Label Font Size */
        .shiny-input-container label { font-size: 14px !important; }
        
        /* Dashboard Header Styling */
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: black;
            height: 80px;
            padding: 10px;
        }
        .logo-container {
            margin-right: 5px;
            height: 100%;
            padding: 10px;
        
        }
        .logo-container img {
            height: 50px;
        }

        .title-container h2 {
            color: white;
            font-size: 22px;
            margin: 0;
            padding-left: 10px;
        }

  

     

        /* Set Red Background */
        body {
            background-color: #FF2400;
            margin: 0;
            padding: 0;
        }

        /* Hide Plotly Toolbar */
        .modebar {
            display: none;
        }

        /* Card Styling */
        .card {
            background-color: white;
            padding: 15px;
            border-radius: 0px;
            box-shadow: 2px 2px 10px rgba(0, 250, 0, 0.1);
        }
        .info-gen-css {
            font-size: 16px !important; /* Adjust the size as needed */
            color: purple !important;
            display: flex !important; /* Enables centering */
            align-items: center !important; /* Centers vertically */
            justify-content: center !important; /* Centers horizontally */
            text-align: center !important; /* Ensures text alignment */
            font-weight: bold !important; /* Makes the text bold */
        }
    }
    </style>
    """
)

# ---- Set Page Options ----
ui.page_opts(window_title="TTC Delay Dashboard", fillable=False)


numbers = list(range(1, 136))  # Creates a list from 1 to 135
remove_list = [1, 2, 3, 4, 5, 6, 18, 27, 58, 81, 103]  
filtered_numbers = [num for num in numbers if num not in remove_list]

added_routes = [149, 154, 160, 161, 162, 165, 167, 168, 169, 171, 185, 189, 300, 302, 307, 315, 320, 322, 324, 325, 329, 332, 334, 335, 336, 337, 339, 340, 341, 343, 352, 353, 354, 363, 365, 384, 385, 395, 396, 400, 402, 403, 404, 405, 900, 902, 903, 904, 905, 924, 925, 927, 929, 935, 937, 938, 939, 941, 944, 945, 952, 954, 960, 968, 984, 985, 986, 989, 995, 996]

routes_number = filtered_numbers + added_routes


# ---- Header ----
with ui.div(class_="header-container"):
    with ui.div(class_="logo-container"):
        @render.image
        def image():
            here = Path(__file__).parent
            return {"src": str(here / "images/TTC-logo.png")}  # Ensure path correctness

    with ui.div(class_="title-container"):
        ui.h2("TTC Delay Dashboard")


# ---- Main UI ----
with ui.card():
    with ui.navset_card_tab(id="tab"):
        # Bus Tab
        with ui.nav_panel("Bus"):

            with ui.card():
                
                ui.card_header("General Information", class_="info-gen-css")

                with ui.layout_columns(col_widths={"sm": (4, 8)}):


                    with ui.card():
                        ui.card_header("Insights")

                        @render.data_frame  
                        def penguins_df():
                            return render.DataGrid(Bus_general_inf_dataframe, selection_mode="row")  

                    with ui.card():
                        ui.card_header("Explanation")


                        @render.ui
                        def dynamic_content():
                            #if input.tab() == "agency":
                            return ui.TagList(
                                ui.tags.ul(  # Unordered list for bullet points
                                    ui.tags.li("All Delays equal to zero were removed."),
                                    ui.tags.li("All Delays greater than the 995th percentile were removed."),
                                    ui.tags.li("We only hold incidents related to routes that are active in 2025."),
                                    ui.tags.li("Locatio features are deleted as they are not consist of coordinates."),
                                    ui.tags.li("Some direction are labeled as Unknown as they wer not entered correctly in database."),
                                ),
                                ui.p("For list of active routes refer to: ", 
                                    ui.a("ttc.ca/routes/bus", href="https://www.ttc.ca/routes-and-schedules/listroutes/bus", target="_blank"))
                            )

            with ui.card():
                ui.card_header("Select Filters")
                
             
                with ui.card():
                    

                    with ui.layout_columns(col_widths={"sm": (2, 2, 2, 3, 3)}):
                    
                        # Dropdown Selections
                        ui.input_select("year", "Year", ["All"] + [str(y) for y in range(2014, 2025)], selected="All", multiple=True, size = 3)
                        ui.input_select("season", "Season", ["All", "Winter", "Spring", "Summer", "Fall"], selected="All", multiple=True,size = 3)
                        ui.input_select("month", "Month", ["All"] + [calendar.month_name[m] for m in range(1, 13)], selected="All", multiple=True,size = 3)
                        # Get list of weekdays (Monday to Sunday)
                        weekdays = ["All"] + list(calendar.day_name)

                        ui.input_select("day", "Day", weekdays, selected="All", multiple=True,size = 3)

                        ui.input_select("route", "Route", ["All"] + [str(y) for y in routes_number], selected="All", multiple=True, size = 3)



                    # Filter Button
                    ui.input_action_button("apply_filters", "Apply Filters", class_="btn-primary")
                   
                        

            with ui.card():

                @render.ui  
                @reactive.event(input.apply_filters)
                def datefun():  
                    if input.year() == str(2024):
                        a = f"Year is {input.year()}, Season is {input.season()}, Month is {input.month()}, Day is {input.day()}"
                    elif str(input.day()) != 'Monday':
                        a = str(input.route())
                    else:
                        a = input.route()

                    return a
            








        # Streetcar Tab
        with ui.nav_panel("Streetcar"):
            ui.h5("Streetcar Data Coming Soon", class_="small-font")

        # Subway Tab
        with ui.nav_panel("Subway"):
            ui.h5("Subway Data Coming Soon", class_="small-font")


