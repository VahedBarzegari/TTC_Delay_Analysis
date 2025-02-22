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

# ---- Global Styles ----
ui.markdown(
    """
    <style>
        /* Reduce Button Font Size */
        .btn { font-size: 12px !important; padding: 6px 10px; }
        
        /* Reduce Input Label Font Size */
        .shiny-input-container label { font-size: 12px !important; }
        
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
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """
)

# ---- Set Page Options ----
ui.page_opts(window_title="TTC Delay Dashboard", fillable=False)


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
    with ui.navset_pill(id="tab"):
        # Bus Tab
        with ui.nav_panel("Bus"):

            with ui.card():
                ui.h6("General Information", class_="small-font")

            with ui.card():
                ui.card_header("Select Filters")
                
             
                with ui.card():
                    

                    with ui.layout_columns(col_widths={"sm": (3, 3, 3, 3)}):
                    
                        # Dropdown Selections
                        ui.input_select("year", "Select Year", ["All Years"] + [str(y) for y in range(2014, 2025)])
                        ui.input_select("season", "Select Season", ["All", "Winter", "Spring", "Summer", "Fall"])
                        ui.input_select("month", "Select Month", ["All"] + [calendar.month_name[m] for m in range(1, 13)])
                        ui.input_select("day", "Select Day", ["All"] + [str(d) for d in range(1, 32)])

                    # Filter Button
                    ui.input_action_button("apply_filters", "Apply Filters", class_="btn-primary")
                   
                        

            with ui.card():

                @render.ui  
                @reactive.event(input.apply_filters)
                def datefun():  
                    if input.year() == str(2024):
                        a = f"Year is {input.year()}, Season is {input.season()}, Month is {input.month()}, Day is {input.day()}"
                    else:
                        a = f"Year is kir, Season is {input.season()}, Month is {input.month()}, Day is {input.day()}"

                    return a
            








        # Streetcar Tab
        with ui.nav_panel("Streetcar"):
            ui.h5("Streetcar Data Coming Soon", class_="small-font")

        # Subway Tab
        with ui.nav_panel("Subway"):
            ui.h5("Subway Data Coming Soon", class_="small-font")


