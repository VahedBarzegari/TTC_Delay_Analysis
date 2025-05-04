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


from core_data_code import Bus_general_inf_dataframe, bus_df, streetcar_df, Streetcar_general_inf_dataframe, subway_df, Subway_general_inf_dataframe

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
        .insight_title-css {
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

added_routes = [149, 154, 160, 161, 162, 165, 167, 168, 169, 171, 185, 189, 300, 302, 307, 315, 320, 322, 324, 325, 329, 332, 334, 335, 336, 337, 339, 340, 341, 343, 352, 353, 354, 363, 365, 384, 385, 395, 396, 400, 900, 902, 903, 904, 905, 924, 925, 927, 929, 935, 937, 938, 939, 941, 944, 945, 952, 954, 960, 968, 984, 985, 986, 989, 995, 996]

busroutes_number = filtered_numbers + added_routes


streetcarroutes_number = [500, 501, 503, 504, 505, 506, 509, 510, 511, 512, 507, 301, 303, 304, 305, 306, 310, 312]

subway_line_numbers = [1, 2, 4]

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

            with ui.card(height="600px"):
                
                ui.card_header("General Information", class_="info-gen-css")

                with ui.layout_columns(col_widths={"sm": (4, 8)}):

                    
                    with ui.card(class_="card_Insights"):
                        ui.card_header("Insights", class_="insight_title-css")

                        @render.data_frame  
                        def insights_df():
                            return render.DataGrid(Bus_general_inf_dataframe, selection_mode="row")  

                    with ui.card():
                        with ui.navset_pill(id="tab2"): 

                            with ui.nav_panel("Explanation"):

                                @render.ui
                                def dynamic_content():
                                    total_incidents = len(bus_df)

                                    return ui.TagList(
                                        ui.div(  # Add border wrapper
                                            ui.tags.ul(
                                                [
                                                    ui.tags.li(ui.HTML("Data from <span style='text-decoration: underline; color:blue;'>2014</span> to the end of <span style='text-decoration: underline;color:blue;'>2024</span> are assessed.")),
                                                    ui.tags.li("All delays equal to zero are removed from analysis."),
                                                    ui.tags.li(ui.HTML("All delays greater than the <span style='text-decoration: underline;color: blue;'>995th</span> percentile are removed.")),
                                                    ui.tags.li(ui.HTML(f"Total number of assessed incidents is <span style='text-decoration: underline; color:blue;'>{total_incidents}</span>.")),
                                                    ui.tags.li("Location features are deleted as they are not consist of coordinates."),
                                                    ui.tags.li(ui.HTML("Some direction were not entered correctly and labeled as <b><i><span style='color:red;'>Unknown</span></i></b>.")),
                                                    ui.tags.li(ui.HTML("We only hold incidents related to routes that are active in <span style='color: blue; text-decoration: underline;'>2025</span>.")),
                                                    ui.tags.li([
                                                        "For list of active routes refer to: ",
                                                        ui.a("ttc.ca/routes/bus", href="https://www.ttc.ca/routes-and-schedules/listroutes/bus", target="_blank")
                                                    ])
                                                ],
                                                style="line-height: 2.5;"
                                            ),
                                            style="border: 2px solid #ccc; padding: 0px !important; border-radius: 30px; margin-top: 0px !important;"
                                        )
                                    )

                            with ui.nav_panel("Worst Bus Routes"):

                                # Minimal space between slider and plot
                                ui.div(
                                    ui.input_slider("year_selected_bus", "Year", 2014, 2024, 2018, width="25%"),
                                    style="margin: 0px !important; padding: 0px !important; font-size: 6px"  # You can reduce or increase this value
                                )
                                with ui.card(height="320px"):



                                    @render.plot
                                    def worst__bus_routes_df():
                                        year_filter = int(input.year_selected_bus())
                                        bus_df3 = bus_df[bus_df['Year'] == year_filter]

                                        route_delay_sum = bus_df3.groupby('Route')['Min Delay'].sum().sort_values(ascending=False)
                                        top_10_routes = route_delay_sum.head(10)

                                        plt.figure()
                                        sns.barplot(x=top_10_routes.index.astype(str), y=top_10_routes.values, palette='Reds_r')

                                        # Adjusting font size for all elements
                                        plt.title(f'Top Worst Bus Routes in {year_filter}', fontdict={'fontsize': 9})
                                        plt.ylabel('Total Delay (minutes)', fontsize=9)
                                        plt.xlabel('Route', fontsize=9)
                                        
                                        route_labels = [f'Route {r}' for r in top_10_routes.index]
                                        plt.xticks(ticks=range(len(route_labels)), labels=route_labels, rotation=20, fontsize=8)
                                        plt.yticks(fontsize=9)

                                        plt.tight_layout()



                                        

                            with ui.nav_panel("Year Comparasion"):

                                @render.plot

                                def yearplot_com():

                                    # Set Seaborn style
                                    sns.set(style="whitegrid")

                                    # Group and prepare data
                                    delay_per_year = bus_df.groupby('Year')['Min Delay'].sum().reset_index()

                                    # Plot
                                    plt.figure(figsize=(8, 4))
                                    line = plt.plot(delay_per_year['Year'], delay_per_year['Min Delay'],
                                                    marker='o', color='#1f77b4', linewidth=2.5, label='Total Min Delay')

                                
                                    # Titles and labels
                                    
                                    plt.xlabel('Year', fontsize=10)
                                    plt.ylabel('Total Duration of Delays (minutes)', fontsize=10)
                                    plt.xticks(delay_per_year['Year'])  # Ensure all years are shown
                                    plt.grid(alpha=0.3)

                                 

                                    plt.tight_layout()

                             

            ui.br()

            

            with ui.layout_columns(col_widths={"sm": (3, 9)}):

                with ui.card(height="200px", class_="card_Filters"):
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
                                ["All"] + [str(y) for y in busroutes_number],
                                selected="All", multiple=True, size=3
                            )

                    ui.input_action_button("apply_filters", "Apply Filters", class_="btn-primary")

                    ui.input_radio_buttons(  
                        "incident_tupe",  
                        "",  
                        {"1": "By the number of incidents", "2": "By the duration of incidents"}, selected="") 

        

                with ui.navset_card_tab(id="tab1"):
                        with ui.nav_panel("Date"):




                                @render.plot
                                @reactive.event(input.apply_filters, input.incident_tupe)
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



                                    if not input.incident_tupe() or input.incident_tupe() == "":
                                        return 
                                    
                                    else:

                                        input_date_index = int(input.incident_tupe())

                                        if input_date_index == 1:
                
                                            incident_counts = bus_df1.groupby('Date').size()


                                            plt.figure()  # Ensure a new figure is created
                                            plt.plot(incident_counts.values, color='blue', marker='o', linestyle='')
                                            plt.xlabel('Date')
                                            plt.ylabel('Number of Delay Incidents per Date')
                                            plt.title('Total Number of Incidents')
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


                                        elif input_date_index == 2:

                                            incident_counts = bus_df1.groupby('Date')['Min Delay'].sum()


                                            plt.figure()  # Ensure a new figure is created
                                            plt.plot(incident_counts.values, color='purple', marker='o', linestyle='')
                                            plt.xlabel('Date')
                                            plt.ylabel('Duration of Incidents per Date (min)')
                                            plt.title('Total Duration of Incidents')
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





                        with ui.nav_panel("Time of Day"):



                            
                            @render.plot
                            @reactive.event(input.apply_filters, input.incident_tupe)
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


                                if not input.incident_tupe() or input.incident_tupe() == "":
                                    return 
                                
                                else:

                                    input_time_index = int(input.incident_tupe())



                                    if input_time_index == 1:
                                        incident_counts = bus_df1.groupby('Time').size().reset_index(name='Incident Count')
                                        labels = incident_counts['Time'].astype(str).tolist()
                                        values = incident_counts['Incident Count'].tolist()

                                        # Close the loop
                                        values += values[:1]
                                        labels += labels[:1]

                                        # Angles
                                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=True)

                                        # Set up figure and axis
                                        fig, ax = plt.subplots( subplot_kw=dict(polar=True))
                                        # Plot and fill
                                        ax.plot(angles, values, color='navy', linewidth=2)
                                        ax.fill(angles, values, color='skyblue', alpha=0.4)

                                        # Set x-axis (time) labels
                                        ax.set_xticks(angles[:-1])
                                        ax.set_xticklabels([''] * len(labels[:-1]))  # Hide default labels

                                        # Custom label positioning
                                        label_distance = max(values) * 1.1  # adjust 1.1 to increase/decrease distance
                                        for angle, label in zip(angles[:-1], labels[:-1]):
                                            ax.text(angle, label_distance, label, ha='center', va='center', fontsize=8)

                                        
                                        # Create custom radial grid lines
                                        max_val = max(values)
                                        num_rings = 4
                                        ring_vals = np.linspace(0, max_val, num_rings + 1)[1:]

                                        ring_colors = ['#77f571', '#28ded8', '#ed921a', '#ed1e1a']  # light to dark blue
                                        for r_val, color in zip(ring_vals, ring_colors):
                                            ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100, linestyle='--', color=color, linewidth=0.8)

                                        # Hide default y-tick labels
                                        ax.set_yticklabels([])

                                        # Add custom legend for circle levels
                                        from matplotlib.lines import Line2D
                                        legend_handles = [Line2D([0], [0], color=color, lw=1.5, linestyle='--', label=f"{int(r_val)}") 
                                                        for r_val, color in zip(ring_vals, ring_colors)]
                                        ax.legend(handles=legend_handles, title="Circle Values", loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title_fontsize=9)

                                        # Title




                                       # Title and layout
                                        ax.set_title('Total Number of Incidents per Time', fontsize=9, fontweight='bold', pad=15)
                                        # Show only radial grid lines (concentric circles)
                                        ax.yaxis.grid(False)
                                        ax.xaxis.grid(True)
                                        plt.tight_layout()

                                    elif input_time_index == 2:
                                        incident_duration = bus_df1.groupby('Time')['Min Delay'].sum().reset_index(name='Total Duration')
                                        labels = incident_duration['Time'].astype(str).tolist()
                                        values = incident_duration['Total Duration'].tolist()


                                        # Close the loop
                                        values += values[:1]
                                        labels += labels[:1]

                                        # Angles
                                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=True)

                                        # Set up figure and axis
                                        fig, ax = plt.subplots( subplot_kw=dict(polar=True))
                                        # Plot and fill
                                        ax.plot(angles, values, color='navy', linewidth=2)
                                        ax.fill(angles, values, color='skyblue', alpha=0.4)

                                        # Set x-axis (time) labels
                                        ax.set_xticks(angles[:-1])
                                        ax.set_xticklabels([''] * len(labels[:-1]))  # Hide default labels

                                        # Custom label positioning
                                        label_distance = max(values) * 1.1  # adjust 1.1 to increase/decrease distance
                                        for angle, label in zip(angles[:-1], labels[:-1]):
                                            ax.text(angle, label_distance, label, ha='center', va='center', fontsize=8)

                                        
                                        # Create custom radial grid lines
                                        max_val = max(values)
                                        num_rings = 4
                                        ring_vals = np.linspace(0, max_val, num_rings + 1)[1:]

                                        ring_colors = ['#77f571', '#28ded8', '#ed921a', '#ed1e1a']  # light to dark blue
                                        for r_val, color in zip(ring_vals, ring_colors):
                                            ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100, linestyle='--', color=color, linewidth=0.8)

                                        # Hide default y-tick labels
                                        ax.set_yticklabels([])

                                        # Add custom legend for circle levels
                                        from matplotlib.lines import Line2D
                                        legend_handles = [Line2D([0], [0], color=color, lw=1.5, linestyle='--', label=f"{int(r_val)}") 
                                                        for r_val, color in zip(ring_vals, ring_colors)]
                                        ax.legend(handles=legend_handles, title="Circle Values", loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title_fontsize=9)

                                        # Title


                                       # Title and layout
                                        ax.set_title('Total Duration of Incidents per Time', fontsize=9, fontweight='bold', pad=15)
                                        # Show only radial grid lines (concentric circles)
                                        ax.yaxis.grid(False)
                                        ax.xaxis.grid(True)
                                        plt.tight_layout()
    


                        with ui.nav_panel("Day of Week"):



                            
                            @render.plot
                            @reactive.event(input.apply_filters, input.incident_tupe)
                            def plot5():


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


                                if not input.incident_tupe() or input.incident_tupe() == "":
                                    return 
                                
                                else:

                                    input_day_index = int(input.incident_tupe())


                                    if input_day_index == 1:


                                        
                                        # Group by Day and count incidents
                                        incident_counts = bus_df1.groupby('Day').size().reset_index(name='Incident Count')

                                        # Define the correct weekday order
                                        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                                        # Convert 'Day' to an ordered categorical type and sort
                                        incident_counts['Day'] = pd.Categorical(incident_counts['Day'], categories=weekday_order, ordered=True)
                                        incident_counts = incident_counts.sort_values('Day')

                                        # Get the maximum incident count
                                        max_value = incident_counts['Incident Count'].max()

                                        # Set colors: red for max values, skyblue for others
                                        colors = ['red' if count == max_value else 'skyblue' for count in incident_counts['Incident Count']]

                                        # Plotting
                                        plt.figure(figsize=(8, 5))
                                        plt.bar(incident_counts['Day'], incident_counts['Incident Count'], color=colors)
                                        plt.xlabel('Day')
                                        plt.ylabel('Total Number of Incidents')
                                        plt.title('Total Number of Incidents per Day')
                                        plt.xticks(rotation=0)
                                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                                        plt.tight_layout()


                                    elif input_day_index==2:


                                        # Group by Time and sum the durations
                                        incident_duration = bus_df1.groupby('Day')['Min Delay'].sum().reset_index(name='Total Duration')
                                        # Define correct weekday order
                                        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                                        # Convert Day to ordered categorical and sort
                                        incident_duration['Day'] = pd.Categorical(incident_duration['Day'], categories=weekday_order, ordered=True)
                                        incident_duration = incident_duration.sort_values('Day')

                                        # Get the maximum total duration *after sorting*
                                        max_duration = incident_duration['Total Duration'].max()

                                        # Set colors based on sorted data
                                        colors = ['red' if dur == max_duration else 'skyblue' for dur in incident_duration['Total Duration']]

                                        # Plot
                                        plt.figure(figsize=(8, 5))
                                        plt.bar(incident_duration['Day'], incident_duration['Total Duration'], color=colors)
                                        plt.xlabel('Day')
                                        plt.ylabel('Total Duration of Incidents')
                                        plt.title('Total Duration of Incidents per Day')
                                        plt.xticks(rotation=0)
                                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                                        plt.tight_layout()
                                



                        with ui.nav_panel("Incident Type"):



                
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

                                                                

                                # Count and calculate percentages
                                incident_counts = bus_df1['Incident'].value_counts(normalize=True) * 100
                                incident_counts = incident_counts.sort_values(ascending=False)

                                # Normalize for colormap
                                norm = mcolors.Normalize(vmin=incident_counts.min(), vmax=incident_counts.max())
                                colors = [cm.Reds(norm(value)) for value in incident_counts.values]

                                # Plot
                                fig, ax = plt.subplots()
                                bars = ax.bar(
                                    incident_counts.index, 
                                    incident_counts.values, 
                                    color=colors, 
                                    edgecolor='black',
                                    linewidth=0.5
                                )

                                # Add percentage labels
                                for bar, pct in zip(bars, incident_counts.values):
                                    ax.text(
                                        bar.get_x() + bar.get_width() / 2, 
                                        bar.get_height() + 0.1, 
                                        f'{pct:.2f}', 
                                        ha='center', va='bottom', fontsize=9, fontweight='medium'
                                    )

                                # Customization
                                ax.set_title('Percentage Distribution of Incident Types', fontsize=10, fontweight='bold', pad=5)
                                ax.set_ylabel('Percentage of Incidents', fontsize=12)
                                ax.set_xticklabels(incident_counts.index, rotation=30, ha='right', fontsize=9)
                                ax.tick_params(axis='y', labelsize=9)
                                ax.grid(axis='y', linestyle='--', alpha=0.4)
                                fig.patch.set_facecolor('white')
                                ax.set_facecolor('white')

                                plt.tight_layout()
             


                        with ui.nav_panel("Direction"):



                
                            @render.plot
                            @reactive.event(input.apply_filters)
                            def plot_direction():


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

                                # Count occurrences of each direction
                                direction_counts = bus_df1['Direction'].value_counts()

                                percentages = 100 * direction_counts / direction_counts.sum()
                                labels = direction_counts.index
                                sizes = direction_counts.values

                                # Format labels with percentages
                                legend_labels = [f"{label}: {pct:.1f}%" for label, pct in zip(labels, percentages)]

                                # Colors (custom pastel palette)
                                colors = plt.cm.Paired.colors[:len(labels)]

                                # Explode slightly for all slices
                                explode = [0.05] * len(labels)

                                # Plot
                                fig, ax = plt.subplots()
                                wedges, texts = ax.pie(
                                    sizes,
                                    labels=None,
                                    startangle=90,
                                    wedgeprops=dict(width=0.4, edgecolor='w'),
                                    explode=explode,
                                    colors=colors,
                                    shadow=True
                                )

                                # Equal aspect ratio
                                ax.axis('equal')

                                # Legend at bottom
                                ax.legend(
                                    wedges, legend_labels,
                                    
                                    loc='lower center',
                                    bbox_to_anchor=(0.5, -0.25),
                                    ncol=3,
                                    fontsize='medium',
                                    title_fontsize='large',
                                    frameon=False
                                )

                                # Title
                                plt.title("Distribution of Incident Directions", fontsize=16, fontweight='bold')
                                plt.tight_layout()
        # Streetcar Tab
        with ui.nav_panel("Streetcar"):


            with ui.card(height="600px"):
                
                ui.card_header("General Information", class_="info-gen-css")

                with ui.layout_columns(col_widths={"sm": (4, 8)}):

                    
                    with ui.card(class_="card_Insights"):
                        ui.card_header("Insights", class_="insight_title-css")

                        @render.data_frame  
                        def insights_streetcar_df():
                            return render.DataGrid(Streetcar_general_inf_dataframe, selection_mode="row")  

                    with ui.card():
                        with ui.navset_pill(id="tab5"): 

                            with ui.nav_panel("Explanation"):

                                @render.ui
                                def dynamic_content_streetcar():
                                    total_incidents = len(streetcar_df)

                                    return ui.TagList(
                                        ui.div(  # Add border wrapper
                                            ui.tags.ul(
                                                [
                                                    ui.tags.li(ui.HTML("Data from <span style='text-decoration: underline; color:blue;'>2014</span> to the end of <span style='text-decoration: underline;color:blue;'>2024</span> are assessed.")),
                                                    ui.tags.li("All delays equal to zero are removed from analysis."),
                                                    ui.tags.li(ui.HTML("All delays greater than the <span style='text-decoration: underline;color: blue;'>995th</span> percentile are removed.")),
                                                    ui.tags.li(ui.HTML(f"Total number of assessed incidents is <span style='text-decoration: underline; color:blue;'>{total_incidents}</span>.")),
                                                    ui.tags.li("Location features are deleted as they are not consist of coordinates."),
                                                    ui.tags.li(ui.HTML("Some direction were not entered correctly and labeled as <b><i><span style='color:red;'>Unknown</span></i></b>.")),
                                                    ui.tags.li(ui.HTML("We only hold incidents related to routes that are active in <span style='color: blue; text-decoration: underline;'>2025</span>.")),
                                                    ui.tags.li([
                                                        "For list of active routes refer to: ",
                                                        ui.a("ttc.ca/routes/streetcar", href="https://www.ttc.ca/routes-and-schedules/listroutes/streetcar", target="_blank")
                                                    ])
                                                ],
                                                style="line-height: 2.5;"
                                            ),
                                            style="border: 2px solid #ccc; padding: 0px !important; border-radius: 30px; margin-top: 0px !important;"
                                        )
                                    )

                            with ui.nav_panel("Worst Streetcar Routes"):
                             


                                # Minimal space between slider and plot
                                ui.div(
                                    ui.input_slider("year_selected_street", "Year", 2014, 2024, 2018, width="25%"),
                                    style="margin: 0px !important; padding: 0px !important; font-size: 6px"  # You can reduce or increase this value
                                )
                                with ui.card(height="320px"):



                                    @render.plot
                                    def worst__street_routes_df():
                                        year_filter = int(input.year_selected_street())
                                        streetcar_df3 = streetcar_df[streetcar_df['Year'] == year_filter]

                                        route_delay_sum = streetcar_df3.groupby('Route')['Min Delay'].sum().sort_values(ascending=False)
                                        top_10_routes = route_delay_sum.head(10)

                                        plt.figure()
                                        sns.barplot(x=top_10_routes.index.astype(str), y=top_10_routes.values, palette='Reds_r')

                                        # Adjusting font size for all elements
                                        plt.title(f'Top Worst Streetcar Routes in {year_filter}', fontdict={'fontsize': 9})
                                        plt.ylabel('Total Delay (minutes)', fontsize=9)
                                        plt.xlabel('Route', fontsize=9)
                                        
                                        route_labels = [f'Route {r}' for r in top_10_routes.index]
                                        plt.xticks(ticks=range(len(route_labels)), labels=route_labels, rotation=20, fontsize=8)
                                        plt.yticks(fontsize=9)

                                        plt.tight_layout()


                            with ui.nav_panel("Year Comparasion"):

                                @render.plot

                                def yearplot_com_streetcar():

                                    # Set Seaborn style
                                    sns.set(style="whitegrid")

                                    # Group and prepare data
                                    delay_per_year = streetcar_df.groupby('Year')['Min Delay'].sum().reset_index()

                                    # Plot
                                    plt.figure(figsize=(8, 4))
                                    line = plt.plot(delay_per_year['Year'], delay_per_year['Min Delay'],
                                                    marker='o', color='#d98314', linewidth=2.5, label='Total Min Delay')

                                
                                    # Titles and labels
                                    
                                    plt.xlabel('Year', fontsize=10)
                                    plt.ylabel('Total Duration of Delays (minutes)', fontsize=10)
                                    plt.xticks(delay_per_year['Year'])  # Ensure all years are shown
                                    plt.grid(alpha=0.3)

                                 

                                    plt.tight_layout()



            ui.br()



           

            with ui.layout_columns(col_widths={"sm": (3, 9)}):

                with ui.card(height="200px", class_="card_Filters"):
                    ui.card_header("Select Filters", class_="fliter_box-css")
                    
            

                
                    with ui.accordion(id="acc_street",open=[]):

                        with ui.accordion_panel("Year"):
                            ui.input_select(
                                "year_stre", "",
                                ["All"] + [str(y) for y in range(2014, 2025)],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Season"):
                            ui.input_select(
                                "season_stre", "",
                                ["All", "Winter", "Spring", "Summer", "Fall"],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Month"):
                            ui.input_select(
                                "month_stre", "",
                                ["All"] + [calendar.month_name[m] for m in range(1, 13)],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Day of Week"):
                            weekdays = ["All"] + list(calendar.day_name)
                            ui.input_select(
                                "day_stre", "",
                                weekdays, selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Route"):
                            ui.input_select(
                                "route_stre", "",
                                ["All"] + [str(y) for y in streetcarroutes_number],
                                selected="All", multiple=True, size=3
                            )

                    ui.input_action_button("apply_filters_stre", "Apply Filters", class_="btn-primary")

                    ui.input_radio_buttons(  
                        "incident_tupe_streetcar",  
                        "",  
                        {"1": "By the number of incidents", "2": "By the duration of incidents"}, selected="") 


        

                with ui.navset_card_tab(id="tab1_stree"):
                        with ui.nav_panel("Date"):




                            @render.plot
                            @reactive.event(input.apply_filters_stre, input.incident_tupe_streetcar)
                            def plot1_street():

                                c = str(input.year_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df[streetcar_df['Year'].isin(b)]


                                a = str(input.month_stre())

                                

                                if 'All' in a:

                                    d = str(input.season_stre())

                                    if 'All' in d:
                                        streetcar_df1 = streetcar_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        streetcar_df1 = streetcar_df1[streetcar_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Month'].isin(b)]


                                a = str(input.day_stre()) 

                                if 'All' in a:
                                    streetcar_df1 = streetcar_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Day'].isin(a)]


                                c = str(input.route_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Route'].isin(b)]



                                if not input.incident_tupe_streetcar() or input.incident_tupe_streetcar() == "":
                                    return 
                                
                                else:

                                    input_date_index = int(input.incident_tupe_streetcar())

                                    if input_date_index == 1:
            
                                        incident_counts = streetcar_df1.groupby('Date').size()


                                        plt.figure()  # Ensure a new figure is created
                                        plt.plot(incident_counts.values, color='blue', marker='o', linestyle='')
                                        plt.xlabel('Date')
                                        plt.ylabel('Number of Delay Incidents per Date')
                                        plt.title('Total Number of Incidents')
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


                                    elif input_date_index == 2:

                                        incident_counts = streetcar_df1.groupby('Date')['Min Delay'].sum()


                                        plt.figure()  # Ensure a new figure is created
                                        plt.plot(incident_counts.values, color='purple', marker='o', linestyle='')
                                        plt.xlabel('Date')
                                        plt.ylabel('Duration of Incidents per Date (min)')
                                        plt.title('Total Duration of Incidents')
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





                        with ui.nav_panel("Time of Day"):



                            
                            @render.plot
                            @reactive.event(input.apply_filters_stre, input.incident_tupe_streetcar)
                            def plot4_street():



                                c = str(input.year_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df[streetcar_df['Year'].isin(b)]


                                a = str(input.month_stre())

                                

                                if 'All' in a:

                                    d = str(input.season_stre())

                                    if 'All' in d:
                                        streetcar_df1 = streetcar_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        streetcar_df1 = streetcar_df1[streetcar_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Month'].isin(b)]


                                a = str(input.day_stre()) 

                                if 'All' in a:
                                    streetcar_df1 = streetcar_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Day'].isin(a)]


                                c = str(input.route_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Route'].isin(b)]



                                if not input.incident_tupe_streetcar() or input.incident_tupe_streetcar() == "":
                                    return 
                                
                                else:

                                    input_time_index = int(input.incident_tupe_streetcar())



                                    if input_time_index == 1:
                                        incident_counts = streetcar_df1.groupby('Time').size().reset_index(name='Incident Count')
                                        labels = incident_counts['Time'].astype(str).tolist()
                                        values = incident_counts['Incident Count'].tolist()

                                        # Close the loop
                                        values += values[:1]
                                        labels += labels[:1]

                                        # Angles
                                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=True)

                                        # Set up figure and axis
                                        fig, ax = plt.subplots( subplot_kw=dict(polar=True))
                                        # Plot and fill
                                        ax.plot(angles, values, color='navy', linewidth=2)
                                        ax.fill(angles, values, color='skyblue', alpha=0.4)

                                        # Set x-axis (time) labels
                                        ax.set_xticks(angles[:-1])
                                        ax.set_xticklabels([''] * len(labels[:-1]))  # Hide default labels

                                        # Custom label positioning
                                        label_distance = max(values) * 1.1  # adjust 1.1 to increase/decrease distance
                                        for angle, label in zip(angles[:-1], labels[:-1]):
                                            ax.text(angle, label_distance, label, ha='center', va='center', fontsize=8)

                                        
                                        # Create custom radial grid lines
                                        max_val = max(values)
                                        num_rings = 4
                                        ring_vals = np.linspace(0, max_val, num_rings + 1)[1:]

                                        ring_colors = ['#77f571', '#28ded8', '#ed921a', '#ed1e1a']  # light to dark blue
                                        for r_val, color in zip(ring_vals, ring_colors):
                                            ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100, linestyle='--', color=color, linewidth=0.8)

                                        # Hide default y-tick labels
                                        ax.set_yticklabels([])

                                        # Add custom legend for circle levels
                                        from matplotlib.lines import Line2D
                                        legend_handles = [Line2D([0], [0], color=color, lw=1.5, linestyle='--', label=f"{int(r_val)}") 
                                                        for r_val, color in zip(ring_vals, ring_colors)]
                                        ax.legend(handles=legend_handles, title="Circle Values", loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title_fontsize=9)

                                        # Title




                                       # Title and layout
                                        ax.set_title('Total Number of Incidents per Time', fontsize=9, fontweight='bold', pad=15)
                                        # Show only radial grid lines (concentric circles)
                                        ax.yaxis.grid(False)
                                        ax.xaxis.grid(True)
                                        plt.tight_layout()

                                    elif input_time_index == 2:
                                        incident_duration = streetcar_df1.groupby('Time')['Min Delay'].sum().reset_index(name='Total Duration')
                                        labels = incident_duration['Time'].astype(str).tolist()
                                        values = incident_duration['Total Duration'].tolist()


                                        # Close the loop
                                        values += values[:1]
                                        labels += labels[:1]

                                        # Angles
                                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=True)

                                        # Set up figure and axis
                                        fig, ax = plt.subplots( subplot_kw=dict(polar=True))
                                        # Plot and fill
                                        ax.plot(angles, values, color='navy', linewidth=2)
                                        ax.fill(angles, values, color='skyblue', alpha=0.4)

                                        # Set x-axis (time) labels
                                        ax.set_xticks(angles[:-1])
                                        ax.set_xticklabels([''] * len(labels[:-1]))  # Hide default labels

                                        # Custom label positioning
                                        label_distance = max(values) * 1.1  # adjust 1.1 to increase/decrease distance
                                        for angle, label in zip(angles[:-1], labels[:-1]):
                                            ax.text(angle, label_distance, label, ha='center', va='center', fontsize=8)

                                        
                                        # Create custom radial grid lines
                                        max_val = max(values)
                                        num_rings = 4
                                        ring_vals = np.linspace(0, max_val, num_rings + 1)[1:]

                                        ring_colors = ['#77f571', '#28ded8', '#ed921a', '#ed1e1a']  # light to dark blue
                                        for r_val, color in zip(ring_vals, ring_colors):
                                            ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100, linestyle='--', color=color, linewidth=0.8)

                                        # Hide default y-tick labels
                                        ax.set_yticklabels([])

                                        # Add custom legend for circle levels
                                        from matplotlib.lines import Line2D
                                        legend_handles = [Line2D([0], [0], color=color, lw=1.5, linestyle='--', label=f"{int(r_val)}") 
                                                        for r_val, color in zip(ring_vals, ring_colors)]
                                        ax.legend(handles=legend_handles, title="Circle Values", loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title_fontsize=9)

                                        # Title


                                       # Title and layout
                                        ax.set_title('Total Duration of Incidents per Time', fontsize=9, fontweight='bold', pad=15)
                                        # Show only radial grid lines (concentric circles)
                                        ax.yaxis.grid(False)
                                        ax.xaxis.grid(True)
                                        plt.tight_layout()
    



                        with ui.nav_panel("Day of Week"):



                            
                            @render.plot
                            @reactive.event(input.apply_filters_stre, input.incident_tupe_streetcar)
                            def plot5_steet():




                                c = str(input.year_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df[streetcar_df['Year'].isin(b)]


                                a = str(input.month_stre())

                                

                                if 'All' in a:

                                    d = str(input.season_stre())

                                    if 'All' in d:
                                        streetcar_df1 = streetcar_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        streetcar_df1 = streetcar_df1[streetcar_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Month'].isin(b)]


                                a = str(input.day_stre()) 

                                if 'All' in a:
                                    streetcar_df1 = streetcar_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Day'].isin(a)]


                                c = str(input.route_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Route'].isin(b)]



                                if not input.incident_tupe_streetcar() or input.incident_tupe_streetcar() == "":
                                    return 
                                
                                else:

                                    
                                    input_day_index = int(input.incident_tupe_streetcar())



                                    if input_day_index == 1:


                                        
                                        # Group by Day and count incidents
                                        incident_counts = streetcar_df1.groupby('Day').size().reset_index(name='Incident Count')

                                        # Define the correct weekday order
                                        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                                        # Convert 'Day' to an ordered categorical type and sort
                                        incident_counts['Day'] = pd.Categorical(incident_counts['Day'], categories=weekday_order, ordered=True)
                                        incident_counts = incident_counts.sort_values('Day')

                                        # Get the maximum incident count
                                        max_value = incident_counts['Incident Count'].max()

                                        # Set colors: red for max values, skyblue for others
                                        colors = ['red' if count == max_value else 'skyblue' for count in incident_counts['Incident Count']]

                                        # Plotting
                                        plt.figure(figsize=(8, 5))
                                        plt.bar(incident_counts['Day'], incident_counts['Incident Count'], color=colors)
                                        plt.xlabel('Day')
                                        plt.ylabel('Total Number of Incidents')
                                        plt.title('Total Number of Incidents per Day')
                                        plt.xticks(rotation=0)
                                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                                        plt.tight_layout()


                                    elif input_day_index==2:


                                        # Group by Time and sum the durations
                                        incident_duration = streetcar_df1.groupby('Day')['Min Delay'].sum().reset_index(name='Total Duration')
                                        # Define correct weekday order
                                        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                                        # Convert Day to ordered categorical and sort
                                        incident_duration['Day'] = pd.Categorical(incident_duration['Day'], categories=weekday_order, ordered=True)
                                        incident_duration = incident_duration.sort_values('Day')

                                        # Get the maximum total duration *after sorting*
                                        max_duration = incident_duration['Total Duration'].max()

                                        # Set colors based on sorted data
                                        colors = ['red' if dur == max_duration else 'skyblue' for dur in incident_duration['Total Duration']]

                                        # Plot
                                        plt.figure(figsize=(8, 5))
                                        plt.bar(incident_duration['Day'], incident_duration['Total Duration'], color=colors)
                                        plt.xlabel('Day')
                                        plt.ylabel('Total Duration of Incidents')
                                        plt.title('Total Duration of Incidents per Day')
                                        plt.xticks(rotation=0)
                                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                                        plt.tight_layout()
                                




                        with ui.nav_panel("Incident Type"):


                
                            @render.plot
                            @reactive.event(input.apply_filters_stre)
                            def plot3_street():




                                c = str(input.year_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df[streetcar_df['Year'].isin(b)]


                                a = str(input.month_stre())

                                

                                if 'All' in a:

                                    d = str(input.season_stre())

                                    if 'All' in d:
                                        streetcar_df1 = streetcar_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        streetcar_df1 = streetcar_df1[streetcar_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Month'].isin(b)]


                                a = str(input.day_stre()) 

                                if 'All' in a:
                                    streetcar_df1 = streetcar_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Day'].isin(a)]


                                c = str(input.route_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Route'].isin(b)]




                                                                

                                # Count and calculate percentages
                                incident_counts = streetcar_df1['Incident'].value_counts(normalize=True) * 100
                                incident_counts = incident_counts.sort_values(ascending=False)

                                # Normalize for colormap
                                norm = mcolors.Normalize(vmin=incident_counts.min(), vmax=incident_counts.max())
                                colors = [cm.Reds(norm(value)) for value in incident_counts.values]

                                # Plot
                                fig, ax = plt.subplots()
                                bars = ax.bar(
                                    incident_counts.index, 
                                    incident_counts.values, 
                                    color=colors, 
                                    edgecolor='black',
                                    linewidth=0.5
                                )

                                # Add percentage labels
                                for bar, pct in zip(bars, incident_counts.values):
                                    ax.text(
                                        bar.get_x() + bar.get_width() / 2, 
                                        bar.get_height() + 0.1, 
                                        f'{pct:.2f}', 
                                        ha='center', va='bottom', fontsize=9, fontweight='medium'
                                    )

                                # Customization
                                ax.set_title('Percentage Distribution of Incident Types', fontsize=10, fontweight='bold', pad=5)
                                ax.set_ylabel('Percentage of Incidents', fontsize=12)
                                ax.set_xticklabels(incident_counts.index, rotation=30, ha='right', fontsize=9)
                                ax.tick_params(axis='y', labelsize=9)
                                ax.grid(axis='y', linestyle='--', alpha=0.4)
                                fig.patch.set_facecolor('white')
                                ax.set_facecolor('white')

                                plt.tight_layout()
             



                        with ui.nav_panel("Direction"):



                
                            @render.plot
                            @reactive.event(input.apply_filters_stre)
                            def plot_direction_street():




                                c = str(input.year_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df[streetcar_df['Year'].isin(b)]


                                a = str(input.month_stre())

                                

                                if 'All' in a:

                                    d = str(input.season_stre())

                                    if 'All' in d:
                                        streetcar_df1 = streetcar_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        streetcar_df1 = streetcar_df1[streetcar_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Month'].isin(b)]


                                a = str(input.day_stre()) 

                                if 'All' in a:
                                    streetcar_df1 = streetcar_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Day'].isin(a)]


                                c = str(input.route_stre())

                                if 'All' in c:
                                    streetcar_df1 = streetcar_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    streetcar_df1 = streetcar_df1[streetcar_df1['Route'].isin(b)]





                                # Count occurrences of each direction
                                direction_counts = streetcar_df1['Direction'].value_counts()

                                percentages = 100 * direction_counts / direction_counts.sum()
                                labels = direction_counts.index
                                sizes = direction_counts.values

                                # Format labels with percentages
                                legend_labels = [f"{label}: {pct:.1f}%" for label, pct in zip(labels, percentages)]

                                # Colors (custom pastel palette)
                                colors = plt.cm.Paired.colors[:len(labels)]

                                # Explode slightly for all slices
                                explode = [0.05] * len(labels)

                                # Plot
                                fig, ax = plt.subplots()
                                wedges, texts = ax.pie(
                                    sizes,
                                    labels=None,
                                    startangle=90,
                                    wedgeprops=dict(width=0.4, edgecolor='w'),
                                    explode=explode,
                                    colors=colors,
                                    shadow=True
                                )

                                # Equal aspect ratio
                                ax.axis('equal')

                                # Legend at bottom
                                ax.legend(
                                    wedges, legend_labels,
                                    
                                    loc='lower center',
                                    bbox_to_anchor=(0.5, -0.25),
                                    ncol=3,
                                    fontsize='medium',
                                    title_fontsize='large',
                                    frameon=False
                                )

                                # Title
                                plt.title("Distribution of Incident Directions", fontsize=16, fontweight='bold')
                                plt.tight_layout()







        # Subway Tab
        with ui.nav_panel("Subway"):


            with ui.card(height="600px"):
                
                ui.card_header("General Information", class_="info-gen-css")

                with ui.layout_columns(col_widths={"sm": (4, 8)}):

                    
                    with ui.card(class_="card_Insights"):
                        ui.card_header("Insights", class_="insight_title-css")

                        @render.data_frame  
                        def insights_df_subway():
                            return render.DataGrid(Subway_general_inf_dataframe, selection_mode="row")  

                    with ui.card():
                        with ui.navset_pill(id="tab21"): 

                            with ui.nav_panel("Explanation"):

                                @render.ui
                                def dynamic_content_subway():
                                    total_incidents = len(subway_df)

                                    return ui.TagList(
                                        ui.div(  # Add border wrapper
                                            ui.tags.ul(
                                                [
                                                    ui.tags.li(ui.HTML("Data from <span style='text-decoration: underline; color:blue;'>2014</span> to the end of <span style='text-decoration: underline;color:blue;'>2024</span> are assessed.")),
                                                    ui.tags.li("All delays equal to zero are removed from analysis."),
                                                    ui.tags.li(ui.HTML("All delays greater than the <span style='text-decoration: underline;color: blue;'>995th</span> percentile are removed.")),
                                                    ui.tags.li(ui.HTML(f"Total number of assessed incidents is <span style='text-decoration: underline; color:blue;'>{total_incidents}</span>.")),
                                                    ui.tags.li("Station features are deleted as they are not consist of coordinates."),
                                                    ui.tags.li(ui.HTML("Some direction were not entered correctly and labeled as <b><i><span style='color:red;'>Unknown</span></i></b>.")),
                                                    ui.tags.li(ui.HTML("We only hold incidents related to routes that are active in <span style='color: blue; text-decoration: underline;'>2025</span>.")),
                                                    ui.tags.li([
                                                        "For list of active subway lines refer to: ",
                                                        ui.a("ttc.ca/routes/subway", href="https://www.ttc.ca/routes-and-schedules", target="_blank")
                                                    ])
                                                ],
                                                style="line-height: 2.5;"
                                            ),
                                            style="border: 2px solid #ccc; padding: 0px !important; border-radius: 30px; margin-top: 0px !important;"
                                        )
                                    )

                            with ui.nav_panel("Worst Subway Lines"):
                             

                                # Minimal space between slider and plot
                                ui.div(
                                    ui.input_slider("year_selected_sub", "Year", 2014, 2024, 2018, width="25%"),
                                    style="margin: 0px !important; padding: 0px !important; font-size: 6px"  # You can reduce or increase this value
                                )
                                with ui.card(height="320px"):



                                    @render.plot
                                    def worst__subway_routes_df():
                                        year_filter = int(input.year_selected_sub())
                                        subway_df3 = subway_df[subway_df['Year'] == year_filter]
                                        print(subway_df)

                                        route_delay_sum = subway_df3.groupby('Route')['Min Delay'].sum().sort_values(ascending=False)
                                        top_10_routes = route_delay_sum.head(10)

                                        plt.figure()
                                        sns.barplot(x=top_10_routes.index.astype(str), y=top_10_routes.values, palette='Reds_r')

                                        # Adjusting font size for all elements
                                        plt.title(f'Top Worst Subway Lines in {year_filter}', fontdict={'fontsize': 9})
                                        plt.ylabel('Total Delay (minutes)', fontsize=9)
                                        plt.xlabel('Route', fontsize=9)
                                        
                                        route_labels = [f'Line {r}' for r in top_10_routes.index]
                                        plt.xticks(ticks=range(len(route_labels)), labels=route_labels, rotation=20, fontsize=8)
                                        plt.yticks(fontsize=9)

                                        plt.tight_layout()

                            with ui.nav_panel("Year Comparasion"):

                                @render.plot

                                def yearplot_com_subway():

                                    # Set Seaborn style
                                    sns.set(style="whitegrid")

                                    # Group and prepare data
                                    delay_per_year = subway_df.groupby('Year')['Min Delay'].sum().reset_index()

                                    # Plot
                                    plt.figure(figsize=(8, 4))
                                    line = plt.plot(delay_per_year['Year'], delay_per_year['Min Delay'],
                                                    marker='o', color='#1f77b4', linewidth=2.5, label='Total Min Delay')

                                
                                    # Titles and labels
                                    
                                    plt.xlabel('Year', fontsize=10)
                                    plt.ylabel('Total Duration of Delays (minutes)', fontsize=10)
                                    plt.xticks(delay_per_year['Year'])  # Ensure all years are shown
                                    plt.grid(alpha=0.3)

                                 

                                    plt.tight_layout()

                             

            ui.br()




           

            with ui.layout_columns(col_widths={"sm": (3, 9)}):

                with ui.card(height="200px", class_="card_Filters"):
                    ui.card_header("Select Filters", class_="fliter_box-css")
                    
            

                
                    with ui.accordion(id="acc_subway",open=[]):

                        with ui.accordion_panel("Year"):
                            ui.input_select(
                                "year_sub", "",
                                ["All"] + [str(y) for y in range(2014, 2025)],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Season"):
                            ui.input_select(
                                "season_sub", "",
                                ["All", "Winter", "Spring", "Summer", "Fall"],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Month"):
                            ui.input_select(
                                "month_sub", "",
                                ["All"] + [calendar.month_name[m] for m in range(1, 13)],
                                selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Day of Week"):
                            weekdays = ["All"] + list(calendar.day_name)
                            ui.input_select(
                                "day_sub", "",
                                weekdays, selected="All", multiple=True, size=3
                            )

                        with ui.accordion_panel("Line"):
                            ui.input_select(
                                "route_sub", "",
                                ["All"] + [str(y) for y in subway_line_numbers],
                                selected="All", multiple=True, size=3
                            )

                    ui.input_action_button("apply_filters_sub", "Apply Filters", class_="btn-primary")

                    ui.input_radio_buttons(  
                        "incident_tupe_sub",  
                        "",  
                        {"1": "By the number of incidents", "2": "By the duration of incidents"}, selected="") 



        

                with ui.navset_card_tab(id="tab13"):
                        with ui.nav_panel("Date"):




                                @render.plot
                                @reactive.event(input.apply_filters_sub, input.incident_tupe_sub)
                                def plot1_sub():

                                    c = str(input.year_sub())

                                    if 'All' in c:
                                        subway_df1 = subway_df
                                    else:

                                        c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                        b = [int(x) for x in c_tuple if x.isdigit()] 
                                        subway_df1 = subway_df[subway_df['Year'].isin(b)]


                                    a = str(input.month_sub())

                                    

                                    if 'All' in a:

                                        d = str(input.season_sub())

                                        if 'All' in d:
                                            subway_df1 = subway_df1

                                        else:
                                            d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                            d = [x for x in d_tuple] 
                                            subway_df1 = subway_df1[subway_df1['Season'].isin(d)]


                                    else:
                                        a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                        b = [x for x in a_tuple] 
                                        subway_df1 = subway_df1[subway_df1['Month'].isin(b)]


                                    a = str(input.day_sub()) 

                                    if 'All' in a:
                                        subway_df1 = subway_df1
                                    else:
                                        a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                        a = [x for x in a_tuple] 
                                        subway_df1 = subway_df1[subway_df1['Day'].isin(a)]


                                    c = str(input.route_sub())

                                    if 'All' in c:
                                        subway_df1 = subway_df1
                                    else:

                                        c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                        b = [int(x) for x in c_tuple if x.isdigit()] 
                                        subway_df1 = subway_df1[subway_df1['Route'].isin(b)]



                                    if not input.incident_tupe_sub() or input.incident_tupe_sub() == "":
                                        return 
                                    
                                    else:

                                        input_date_index = int(input.incident_tupe_sub())

                                        if input_date_index == 1:
                
                                            incident_counts = subway_df1.groupby('Date').size()


                                            plt.figure()  # Ensure a new figure is created
                                            plt.plot(incident_counts.values, color='blue', marker='o', linestyle='')
                                            plt.xlabel('Date')
                                            plt.ylabel('Number of Delay Incidents per Date')
                                            plt.title('Total Number of Incidents')
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


                                        elif input_date_index == 2:

                                            incident_counts = subway_df1.groupby('Date')['Min Delay'].sum()


                                            plt.figure()  # Ensure a new figure is created
                                            plt.plot(incident_counts.values, color='purple', marker='o', linestyle='')
                                            plt.xlabel('Date')
                                            plt.ylabel('Duration of Incidents per Date (min)')
                                            plt.title('Total Duration of Incidents')
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







                        with ui.nav_panel("Time of Day"):



                            
                            @render.plot
                            @reactive.event(input.apply_filters_sub, input.incident_tupe_sub)
                            def plot4_sub():


                                c = str(input.year_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df[subway_df['Year'].isin(b)]


                                a = str(input.month_sub())

                                

                                if 'All' in a:

                                    d = str(input.season_sub())

                                    if 'All' in d:
                                        subway_df1 = subway_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        subway_df1 = subway_df1[subway_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Month'].isin(b)]


                                a = str(input.day_sub()) 

                                if 'All' in a:
                                    subway_df1 = subway_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Day'].isin(a)]


                                c = str(input.route_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df1[subway_df1['Route'].isin(b)]



                                if not input.incident_tupe_sub() or input.incident_tupe_sub() == "":
                                    return 
                                
                                else:

                                    input_time_index = int(input.incident_tupe_sub())



                                    if input_time_index == 1:
                                        incident_counts = subway_df1.groupby('Time').size().reset_index(name='Incident Count')
                                        labels = incident_counts['Time'].astype(str).tolist()
                                        values = incident_counts['Incident Count'].tolist()

                                        # Close the loop
                                        values += values[:1]
                                        labels += labels[:1]

                                        # Angles
                                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=True)

                                        # Set up figure and axis
                                        fig, ax = plt.subplots( subplot_kw=dict(polar=True))
                                        # Plot and fill
                                        ax.plot(angles, values, color='navy', linewidth=2)
                                        ax.fill(angles, values, color='skyblue', alpha=0.4)

                                        # Set x-axis (time) labels
                                        ax.set_xticks(angles[:-1])
                                        ax.set_xticklabels([''] * len(labels[:-1]))  # Hide default labels

                                        # Custom label positioning
                                        label_distance = max(values) * 1.1  # adjust 1.1 to increase/decrease distance
                                        for angle, label in zip(angles[:-1], labels[:-1]):
                                            ax.text(angle, label_distance, label, ha='center', va='center', fontsize=8)

                                        
                                        # Create custom radial grid lines
                                        max_val = max(values)
                                        num_rings = 4
                                        ring_vals = np.linspace(0, max_val, num_rings + 1)[1:]

                                        ring_colors = ['#77f571', '#28ded8', '#ed921a', '#ed1e1a']  # light to dark blue
                                        for r_val, color in zip(ring_vals, ring_colors):
                                            ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100, linestyle='--', color=color, linewidth=0.8)

                                        # Hide default y-tick labels
                                        ax.set_yticklabels([])

                                        # Add custom legend for circle levels
                                        from matplotlib.lines import Line2D
                                        legend_handles = [Line2D([0], [0], color=color, lw=1.5, linestyle='--', label=f"{int(r_val)}") 
                                                        for r_val, color in zip(ring_vals, ring_colors)]
                                        ax.legend(handles=legend_handles, title="Circle Values", loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title_fontsize=9)

                                        # Title




                                       # Title and layout
                                        ax.set_title('Total Number of Incidents per Time', fontsize=9, fontweight='bold', pad=15)
                                        # Show only radial grid lines (concentric circles)
                                        ax.yaxis.grid(False)
                                        ax.xaxis.grid(True)
                                        plt.tight_layout()

                                    elif input_time_index == 2:
                                        incident_duration = subway_df1.groupby('Time')['Min Delay'].sum().reset_index(name='Total Duration')
                                        labels = incident_duration['Time'].astype(str).tolist()
                                        values = incident_duration['Total Duration'].tolist()


                                        # Close the loop
                                        values += values[:1]
                                        labels += labels[:1]

                                        # Angles
                                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=True)

                                        # Set up figure and axis
                                        fig, ax = plt.subplots( subplot_kw=dict(polar=True))
                                        # Plot and fill
                                        ax.plot(angles, values, color='navy', linewidth=2)
                                        ax.fill(angles, values, color='skyblue', alpha=0.4)

                                        # Set x-axis (time) labels
                                        ax.set_xticks(angles[:-1])
                                        ax.set_xticklabels([''] * len(labels[:-1]))  # Hide default labels

                                        # Custom label positioning
                                        label_distance = max(values) * 1.1  # adjust 1.1 to increase/decrease distance
                                        for angle, label in zip(angles[:-1], labels[:-1]):
                                            ax.text(angle, label_distance, label, ha='center', va='center', fontsize=8)

                                        
                                        # Create custom radial grid lines
                                        max_val = max(values)
                                        num_rings = 4
                                        ring_vals = np.linspace(0, max_val, num_rings + 1)[1:]

                                        ring_colors = ['#77f571', '#28ded8', '#ed921a', '#ed1e1a']  # light to dark blue
                                        for r_val, color in zip(ring_vals, ring_colors):
                                            ax.plot(np.linspace(0, 2 * np.pi, 100), [r_val] * 100, linestyle='--', color=color, linewidth=0.8)

                                        # Hide default y-tick labels
                                        ax.set_yticklabels([])

                                        # Add custom legend for circle levels
                                        from matplotlib.lines import Line2D
                                        legend_handles = [Line2D([0], [0], color=color, lw=1.5, linestyle='--', label=f"{int(r_val)}") 
                                                        for r_val, color in zip(ring_vals, ring_colors)]
                                        ax.legend(handles=legend_handles, title="Circle Values", loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title_fontsize=9)

                                        # Title


                                       # Title and layout
                                        ax.set_title('Total Duration of Incidents per Time', fontsize=9, fontweight='bold', pad=15)
                                        # Show only radial grid lines (concentric circles)
                                        ax.yaxis.grid(False)
                                        ax.xaxis.grid(True)
                                        plt.tight_layout()
    




                        with ui.nav_panel("Day of Week"):



                            
                            @render.plot
                            @reactive.event(input.apply_filters_sub, input.incident_tupe_sub)
                            def plot5_sub():



                                c = str(input.year_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df[subway_df['Year'].isin(b)]


                                a = str(input.month_sub())

                                

                                if 'All' in a:

                                    d = str(input.season_sub())

                                    if 'All' in d:
                                        subway_df1 = subway_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        subway_df1 = subway_df1[subway_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Month'].isin(b)]


                                a = str(input.day_sub()) 

                                if 'All' in a:
                                    subway_df1 = subway_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Day'].isin(a)]


                                c = str(input.route_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df1[subway_df1['Route'].isin(b)]





                                if not input.incident_tupe_sub() or input.incident_tupe_sub() == "":
                                    return 
                                
                                else:

                                    
                                    input_day_index = int(input.incident_tupe_sub())



                                    if input_day_index == 1:


                                        
                                        # Group by Day and count incidents
                                        incident_counts = subway_df1.groupby('Day').size().reset_index(name='Incident Count')

                                        # Define the correct weekday order
                                        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                                        # Convert 'Day' to an ordered categorical type and sort
                                        incident_counts['Day'] = pd.Categorical(incident_counts['Day'], categories=weekday_order, ordered=True)
                                        incident_counts = incident_counts.sort_values('Day')

                                        # Get the maximum incident count
                                        max_value = incident_counts['Incident Count'].max()

                                        # Set colors: red for max values, skyblue for others
                                        colors = ['red' if count == max_value else 'skyblue' for count in incident_counts['Incident Count']]

                                        # Plotting
                                        plt.figure(figsize=(8, 5))
                                        plt.bar(incident_counts['Day'], incident_counts['Incident Count'], color=colors)
                                        plt.xlabel('Day')
                                        plt.ylabel('Total Number of Incidents')
                                        plt.title('Total Number of Incidents per Day')
                                        plt.xticks(rotation=0)
                                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                                        plt.tight_layout()


                                    elif input_day_index==2:


                                        # Group by Time and sum the durations
                                        incident_duration = subway_df1.groupby('Day')['Min Delay'].sum().reset_index(name='Total Duration')
                                        # Define correct weekday order
                                        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                                        # Convert Day to ordered categorical and sort
                                        incident_duration['Day'] = pd.Categorical(incident_duration['Day'], categories=weekday_order, ordered=True)
                                        incident_duration = incident_duration.sort_values('Day')

                                        # Get the maximum total duration *after sorting*
                                        max_duration = incident_duration['Total Duration'].max()

                                        # Set colors based on sorted data
                                        colors = ['red' if dur == max_duration else 'skyblue' for dur in incident_duration['Total Duration']]

                                        # Plot
                                        plt.figure(figsize=(8, 5))
                                        plt.bar(incident_duration['Day'], incident_duration['Total Duration'], color=colors)
                                        plt.xlabel('Day')
                                        plt.ylabel('Total Duration of Incidents')
                                        plt.title('Total Duration of Incidents per Day')
                                        plt.xticks(rotation=0)
                                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                                        plt.tight_layout()
                                





                        with ui.nav_panel("Incident Type"):


                
                            @render.plot
                            @reactive.event(input.apply_filters_sub)
                            def plot3_subway():





                                c = str(input.year_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df[subway_df['Year'].isin(b)]


                                a = str(input.month_sub())

                                

                                if 'All' in a:

                                    d = str(input.season_sub())

                                    if 'All' in d:
                                        subway_df1 = subway_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        subway_df1 = subway_df1[subway_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Month'].isin(b)]


                                a = str(input.day_sub()) 

                                if 'All' in a:
                                    subway_df1 = subway_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Day'].isin(a)]


                                c = str(input.route_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df1[subway_df1['Route'].isin(b)]





                                                                

                                # Count and calculate percentages
                                incident_counts = subway_df1['Incident'].value_counts(normalize=True) * 100
                                incident_counts = incident_counts.sort_values(ascending=False)

                                # Normalize for colormap
                                norm = mcolors.Normalize(vmin=incident_counts.min(), vmax=incident_counts.max())
                                colors = [cm.Reds(norm(value)) for value in incident_counts.values]

                                # Plot
                                fig, ax = plt.subplots()
                                bars = ax.bar(
                                    incident_counts.index, 
                                    incident_counts.values, 
                                    color=colors, 
                                    edgecolor='black',
                                    linewidth=0.5
                                )

                                # Add percentage labels
                                for bar, pct in zip(bars, incident_counts.values):
                                    ax.text(
                                        bar.get_x() + bar.get_width() / 2, 
                                        bar.get_height() + 0.1, 
                                        f'{pct:.2f}', 
                                        ha='center', va='bottom', fontsize=9, fontweight='medium'
                                    )

                                # Customization
                                ax.set_title('Percentage Distribution of Incident Types', fontsize=10, fontweight='bold', pad=5)
                                ax.set_ylabel('Percentage of Incidents', fontsize=12)
                                ax.set_xticklabels(incident_counts.index, rotation=30, ha='right', fontsize=9)
                                ax.tick_params(axis='y', labelsize=9)
                                ax.grid(axis='y', linestyle='--', alpha=0.4)
                                fig.patch.set_facecolor('white')
                                ax.set_facecolor('white')

                                plt.tight_layout()
             





                        with ui.nav_panel("Direction"):



                
                            @render.plot
                            @reactive.event(input.apply_filters_sub)
                            def plot_direction_sub():





                                c = str(input.year_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df[subway_df['Year'].isin(b)]


                                a = str(input.month_sub())

                                

                                if 'All' in a:

                                    d = str(input.season_sub())

                                    if 'All' in d:
                                        subway_df1 = subway_df1

                                    else:
                                        d_tuple = ast.literal_eval(d)  # Convert string to tuple
                                        d = [x for x in d_tuple] 
                                        subway_df1 = subway_df1[subway_df1['Season'].isin(d)]


                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    b = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Month'].isin(b)]


                                a = str(input.day_sub()) 

                                if 'All' in a:
                                    subway_df1 = subway_df1
                                else:
                                    a_tuple = ast.literal_eval(a)  # Convert string to tuple
                                    a = [x for x in a_tuple] 
                                    subway_df1 = subway_df1[subway_df1['Day'].isin(a)]


                                c = str(input.route_sub())

                                if 'All' in c:
                                    subway_df1 = subway_df1
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    subway_df1 = subway_df1[subway_df1['Route'].isin(b)]





                                # Count occurrences of each direction
                                direction_counts = subway_df1['Direction'].value_counts()

                                percentages = 100 * direction_counts / direction_counts.sum()
                                labels = direction_counts.index
                                sizes = direction_counts.values

                                # Format labels with percentages
                                legend_labels = [f"{label}: {pct:.1f}%" for label, pct in zip(labels, percentages)]

                                # Colors (custom pastel palette)
                                colors = plt.cm.Paired.colors[:len(labels)]

                                # Explode slightly for all slices
                                explode = [0.05] * len(labels)

                                # Plot
                                fig, ax = plt.subplots()
                                wedges, texts = ax.pie(
                                    sizes,
                                    labels=None,
                                    startangle=90,
                                    wedgeprops=dict(width=0.4, edgecolor='w'),
                                    explode=explode,
                                    colors=colors,
                                    shadow=True
                                )

                                # Equal aspect ratio
                                ax.axis('equal')

                                # Legend at bottom
                                ax.legend(
                                    wedges, legend_labels,
                                    
                                    loc='lower center',
                                    bbox_to_anchor=(0.5, -0.25),
                                    ncol=3,
                                    fontsize='medium',
                                    title_fontsize='large',
                                    frameon=False
                                )

                                # Title
                                plt.title("Distribution of Incident Directions", fontsize=16, fontweight='bold')
                                plt.tight_layout()




