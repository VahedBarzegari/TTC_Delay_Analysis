import ast
import asyncio
from datetime import datetime
from faicons import icon_svg
import faicons
import folium.map
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from folium.plugins import HeatMap

from pathlib import Path


import altair as alt
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly, render_altair, render_widget



ui.tags.style(
    """
        .header-container {
        
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: black;
            height: 90px;
            padding: 0;
            margin: 0
    
        }


        .logo-container {
            margin-right: 5px;
            height: 100%;
            padding: 10px;
        
        }

        .logo-container img {
            height: 60px;
        }

        .title-container h2 {
            color: white;
            padding: 5px;
            margin: 0;
        
        }




        body {

            background-color: #FF2400;
            margin: 0;
            padding: 0;
        
        
        }


        .modebar{
            display: none;
        
        }

    """
)



ui.page_opts(window_title="TTC Delay", fillable=False)





with ui.div(class_="header-container"):
    with ui.div(class_="logo-container"):

        @render.image  
        def image():
            here = Path(__file__).parent
            img = {"src": here / "images/TTC-logo.png"}  
            return img 

    with ui.div(class_="title-container"):
        ui.h2("TTC Delay Dashboard")



with ui.card():

    with ui.navset_pill(id="tab"):  
        with ui.nav_panel("Bus"):
            "Panel A content"

            with ui.card():
                ui.p('kir')

        with ui.nav_panel("Streetcar"):
            "Panel B content"

        with ui.nav_panel("Subway"):
            "Panel C content"


