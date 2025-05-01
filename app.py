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
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from core_data_code import Bus_general_inf_dataframe, bus_df

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
        .card_Insights {
            background-color: white;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(125, 200, 125, 0.5);
            color: black !important;
        }
        .card_Explanation {
            background-color: rgb(220, 220, 220);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 250, 0, 0.1);
            color: black !important;
        }
        .card_Filters {
            background-color: rgba(255, 200, 120, 0.4);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(50, 250, 250, 0.5);
            color: black !important;
        }
        .info-gen-css {
            font-size: 16px !important; /* Adjust the size as needed */
            color: white !important;
            display: flex !important; /* Enables centering */
            align-items: center !important; /* Centers vertically */
            justify-content: center !important; /* Centers horizontally */
            text-align: center !important; /* Ensures text alignment */
            font-weight: bold !important; /* Makes the text bold */
            background-color: purple !important;
        }
        .explnation_title-css {
            font-size: 16px !important; /* Adjust the size as needed */
            color: white !important;
            display: flex !important; /* Enables centering */
            align-items: center !important; /* Centers vertically */
            justify-content: left !important; /* Centers horizontally */
            text-align: center !important; /* Ensures text alignment */
            font-weight: bold !important; /* Makes the text bold */
            background-color: black !important;
        }
        .fliter_box-css {
            font-size: 16px !important; /* Adjust the size as needed */
            color: black !important;
            display: flex !important; /* Enables centering */
            align-items: center !important; /* Centers vertically */
            justify-content: center !important; /* Centers horizontally */
            text-align: center !important; /* Ensures text alignment */
            font-weight: bold !important; /* Makes the text bold */
            background-color: lightblue !important;
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


                    with ui.card(class_="card_Insights"):
                        ui.card_header("Insights")

                        @render.data_frame  
                        def penguins_df():
                            return render.DataGrid(Bus_general_inf_dataframe, selection_mode="row")  

                    with ui.card(class_="card_Explanation"):
                        ui.card_header("Explanation", class_="explnation_title-css")


                        @render.ui
                        def dynamic_content():

                            return ui.TagList(
                                ui.tags.ul(  # Unordered list for bullet points
                                    ui.tags.li("All Delays equal to zero are removed from analys."),
                                    ui.tags.li("All Delays greater than the 995th percentile are removed."),
                                    ui.tags.li("We only hold incidents related to routes that are active in 2025."),
                                    ui.tags.li("Location features are deleted as they are not consist of coordinates."),
                                    ui.tags.li("Some direction are labeled as Unknown as they were not entered correctly."),
                                    ui.tags.li("Iformation of December 2024 is not included in the databse."),
                                    style="line-height: 3;"
                                ),
                                ui.p("For list of active routes refer to: ", 
                                    ui.a("ttc.ca/routes/bus", href="https://www.ttc.ca/routes-and-schedules/listroutes/bus", target="_blank"))
                            )

            ui.br()


            with ui.layout_columns(col_widths={"sm": (3, 9)}):

                with ui.card(class_="card_Filters", height="500px"):
                    ui.card_header("Select Filters", class_="fliter_box-css")
                    
            

                
                    with ui.accordion(id="acc",open=[]):

                        with ui.accordion_panel("Year"):
                            ui.input_select(
                                "year", "",
                                ["All"] + [str(y) for y in range(2014, 2025)],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Season"):
                            ui.input_select(
                                "season", "",
                                ["All", "Winter", "Spring", "Summer", "Fall"],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Month"):
                            ui.input_select(
                                "month", "",
                                ["All"] + [calendar.month_name[m] for m in range(1, 13)],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Day of Week"):
                            weekdays = ["All"] + list(calendar.day_name)
                            ui.input_select(
                                "day", "",
                                weekdays, selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Route"):
                            ui.input_select(
                                "route", "",
                                ["All"] + [str(y) for y in routes_number],
                                selected="All", multiple=True, size=3
                            )

                    ui.input_action_button("apply_filters", "Apply Filters", class_="btn-primary")


        

                with ui.navset_card_tab(id="tab1"):
                        with ui.nav_panel("Number of Incidents per Day"):




                                @render.plot
                                @reactive.event(input.apply_filters)
                                def plot1():

                                    c = str(input.year())

                                    if 'All' in c:
                                        bus_df1 = bus_df
                                    else:

                                        c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                        b = [int(x) for x in c_tuple if x.isdigit()] 
                                        bus_df1 = bus_df[bus_df['Year'].isin(b)]


                                    a = str(input.month())

                                    

                                    if 'All' in a:

                                        d = str(input.season())

                                        if 'All' in d:
                                            bus_df1 = bus_df1

                                        else:
                                            d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                            d = [x for x in d_tuple] 
                                            bus_df1 = bus_df1[bus_df1['Season'].isin(d)]


                                    else:
                                        a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                        b = [x for x in a_tuple] 
                                        bus_df1 = bus_df1[bus_df1['Month'].isin(b)]


                                    a = str(input.day()) 

                                    if 'All' in a:
                                        bus_df1 = bus_df1
                                    else:
                                        a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                        a = [x for x in a_tuple] 
                                        bus_df1 = bus_df1[bus_df1['Day'].isin(a)]


                                    c = str(input.route())

                                    if 'All' in c:
                                        bus_df1 = bus_df1
                                    else:

                                        c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                        b = [int(x) for x in c_tuple if x.isdigit()] 
                                        bus_df1 = bus_df1[bus_df1['Route'].isin(b)]




            
                                    incident_counts = bus_df1.groupby('Date').size()


                                    plt.figure()  # Ensure a new figure is created
                                    plt.plot(incident_counts.values, color='blue', marker='o', linestyle='-')
                                    plt.xlabel('Date')
                                    plt.ylabel('Number of Incidents per Day')
                                    plt.grid(axis='y', linestyle='--', alpha=0.7)

                                    # Handling x-ticks dynamically
                                    dates = incident_counts.index
                                    num_dates = len(dates)

                                    if num_dates <= 20:
                                        plt.xticks(range(num_dates), dates, rotation=30)
                                    else:
                                        selected_indices = [0, num_dates // 2, num_dates - 1]
                                        selected_dates = [dates[i] for i in selected_indices]
                                        plt.xticks(selected_indices, selected_dates, rotation=0)

                        with ui.nav_panel("Duration of Delays per Day"):




                                @render.plot
                                @reactive.event(input.apply_filters)
                                def plot2():

                                    c = str(input.year())

                                    if 'All' in c:
                                        bus_df1 = bus_df
                                    else:

                                        c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                        b = [int(x) for x in c_tuple if x.isdigit()] 
                                        bus_df1 = bus_df[bus_df['Year'].isin(b)]


                                    a = str(input.month())

                                    

                                    if 'All' in a:

                                        d = str(input.season())

                                        if 'All' in d:
                                            bus_df1 = bus_df1

                                        else:
                                            d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                            d = [x for x in d_tuple] 
                                            bus_df1 = bus_df1[bus_df1['Season'].isin(d)]


                                    else:
                                        a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                        b = [x for x in a_tuple] 
                                        bus_df1 = bus_df1[bus_df1['Month'].isin(b)]


                                    a = str(input.day()) 

                                    if 'All' in a:
                                        bus_df1 = bus_df1
                                    else:
                                        a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                        a = [x for x in a_tuple] 
                                        bus_df1 = bus_df1[bus_df1['Day'].isin(a)]


                                    c = str(input.route())

                                    if 'All' in c:
                                        bus_df1 = bus_df1
                                    else:

                                        c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                        b = [int(x) for x in c_tuple if x.isdigit()] 
                                        bus_df1 = bus_df1[bus_df1['Route'].isin(b)]




            
                                    incident_counts = bus_df1.groupby('Date')['Min Delay'].sum()


                                    plt.figure()  # Ensure a new figure is created
                                    plt.plot(incident_counts.values, color='purple', marker='o', linestyle='-')
                                    plt.xlabel('Date')
                                    plt.ylabel('Duration of Delays per Day (min)')
                                    plt.grid(axis='y', linestyle='--', alpha=0.7)

                                    # Handling x-ticks dynamically
                                    dates = incident_counts.index
                                    num_dates = len(dates)

                                    if num_dates <= 20:
                                        plt.xticks(range(num_dates), dates, rotation=30)
                                    else:
                                        selected_indices = [0, num_dates // 2, num_dates - 1]
                                        selected_dates = [dates[i] for i in selected_indices]
                                        plt.xticks(selected_indices, selected_dates, rotation=0)



                        with ui.nav_panel("Percentage of Incident Occurrence"):



                
                            @render.plot
                            @reactive.event(input.apply_filters)
                            def plot3():


                                c = str(input.year())

                                if 'All' in c:
                                    bus_df1 = bus_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    bus_df1 = bus_df[bus_df['Year'].isin(b)]


                                a = str(input.month())

                                

                                if 'All' in a:

                                    d = str(input.season())

                                    if 'All' in d:
                                        bus_df1 = bus_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        bus_df1 = bus_df1[bus_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    bus_df1 = bus_df1[bus_df1['Month'].isin(b)]


                                a = str(input.day()) 

                                if 'All' in a:
                                    bus_df1 = bus_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    bus_df1 = bus_df1[bus_df1['Day'].isin(a)]


                                c = str(input.route())

                                if 'All' in c:
                                    bus_df1 = bus_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    bus_df1 = bus_df1[bus_df1['Route'].isin(b)]

                                print(bus_df1)
                                # Count and calculate percentages
                                incident_counts = bus_df1['Incident'].value_counts(normalize=True) * 100
                                incident_counts = incident_counts.sort_values(ascending=False)

                                

                                # Normalize the values for colormap
                                norm = mcolors.Normalize(vmin=incident_counts.min(), vmax=incident_counts.max())
                                colors = [cm.Reds(norm(value)) for value in incident_counts.values]

                                # Plot bar chart
                                plt.figure()
                                bars = plt.bar(incident_counts.index, incident_counts.values, color=colors)

                                # Add percentage labels above each bar
                                for bar, pct in zip(bars, incident_counts.values):
                                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{pct:.1f}%', 
                                            ha='center', va='bottom', fontsize=8)

                                # Customize plot
                                plt.xticks(rotation=45, ha='right', fontsize=6)
                                plt.yticks(fontsize=8)
                                plt.ylabel('Percentage of Incident Occurrence', fontsize=9)
                                plt.tight_layout()



                        with ui.nav_panel("Time"):



                
                            @render.plot
                            @reactive.event(input.apply_filters)
                            def plot4():


                                c = str(input.year())

                                if 'All' in c:
                                    bus_df1 = bus_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    bus_df1 = bus_df[bus_df['Year'].isin(b)]


                                a = str(input.month())

                                

                                if 'All' in a:

                                    d = str(input.season())

                                    if 'All' in d:
                                        bus_df1 = bus_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        bus_df1 = bus_df1[bus_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    bus_df1 = bus_df1[bus_df1['Month'].isin(b)]


                                a = str(input.day()) 

                                if 'All' in a:
                                    bus_df1 = bus_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    bus_df1 = bus_df1[bus_df1['Day'].isin(a)]


                                c = str(input.route())

                                if 'All' in c:
                                    bus_df1 = bus_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    bus_df1 = bus_df1[bus_df1['Route'].isin(b)]

                
                                
                                incident_counts = bus_df1.groupby('Time').size().reset_index(name='Incident Count')

                                # Get the maximum incident count
                                max_value = incident_counts['Incident Count'].max()

                                # Set colors: red for all max values, skyblue for others
                                colors = ['red' if count == max_value else 'skyblue' for count in incident_counts['Incident Count']]

                                # Plotting
                                plt.figure(figsize=(8, 5))
                                plt.bar(incident_counts['Time'], incident_counts['Incident Count'], color=colors)
                                plt.xlabel('Time')
                                plt.ylabel('Number of Incidents')
                                plt.title('Number of Incidents by Time')
                                plt.xticks(incident_counts['Time'])
                                plt.grid(axis='y', linestyle='--', alpha=0.7)
                                plt.tight_layout()
        # Streetcar Tab
        with ui.nav_panel("Streetcar"):
            ui.h5("Streetcar Data Coming Soon", class_="small-font")

        # Subway Tab
        with ui.nav_panel("Subway"):
            ui.h5("Subway Data Coming Soon", class_="small-font")


