import zipfile
import pandas as pd
import io

# Define the ZIP file name
zip_filename_bus = "TTC_Delay_Bus.zip"

# Open the ZIP file and read the CSV
with zipfile.ZipFile(zip_filename_bus, 'r') as zipf:
    with zipf.open("TTC_Delay_Bus.csv") as file:
        bus_df = pd.read_csv(io.TextIOWrapper(file))  # Read CSV into DataFrame


data = {
    "Title": ["Start Year", "End Year", "No. of Routes"],
    "Value": [bus_df['Year'].min(), bus_df['Year'].max(), bus_df['Route'].nunique()]  # Replace None with actual values if available
}

df1 = pd.DataFrame(data)




# Get descriptive statistics
desc = bus_df['Min Delay'].describe()

# Create a DataFrame from describe values
df2 = pd.DataFrame({
    "Title": ["No. of Incidents", "Delay-Mean", "Delay-Std", "Delay-Min", "Delay-25%", "Delay-50%", "Delay-75%", "Delay-Max"],
    "Value": [int(desc["count"]), int(desc["mean"]), int(desc["std"]), int(desc["min"]), int(desc["25%"]), int(desc["50%"]), int(desc["75%"]), int(desc["max"])]
})

# Combine df1 and df2
Bus_general_inf_dataframe = pd.concat([df1, df2], ignore_index=True)



# Define the ZIP file name
zip_filename_streetcar = "TTC_Delay_Streetcar.zip"

# Open the ZIP file and read the CSV
with zipfile.ZipFile(zip_filename_streetcar, 'r') as zipf:
    with zipf.open("TTC_Delay_Streetcar.csv") as file:
        streetcar_df = pd.read_csv(io.TextIOWrapper(file))  # Read CSV into DataFrame


data = {
    "Title": ["Start Year", "End Year", "No. of Routes"],
    "Value": [streetcar_df['Year'].min(), streetcar_df['Year'].max(), streetcar_df['Route'].nunique()]  # Replace None with actual values if available
}

df1 = pd.DataFrame(data)




# Get descriptive statistics
desc = streetcar_df['Min Delay'].describe()

# Create a DataFrame from describe values
df2 = pd.DataFrame({
    "Title": ["No. of Incidents", "Delay-Mean", "Delay-Std", "Delay-Min", "Delay-25%", "Delay-50%", "Delay-75%", "Delay-Max"],
    "Value": [int(desc["count"]), int(desc["mean"]), int(desc["std"]), int(desc["min"]), int(desc["25%"]), int(desc["50%"]), int(desc["75%"]), int(desc["max"])]
})

# Combine df1 and df2
Streetcar_general_inf_dataframe = pd.concat([df1, df2], ignore_index=True)




# Define the ZIP file name
zip_filename_streetcar = "TTC_Delay_Subway.zip"

# Open the ZIP file and read the CSV
with zipfile.ZipFile(zip_filename_streetcar, 'r') as zipf:
    with zipf.open("TTC_Delay_Subway.csv") as file:
        subway_df = pd.read_csv(io.TextIOWrapper(file))  # Read CSV into DataFrame


data = {
    "Title": ["Start Year", "End Year", "No. of Lines"],
    "Value": [subway_df['Year'].min(), subway_df['Year'].max(), subway_df['Route'].nunique()]  # Replace None with actual values if available
}

df1 = pd.DataFrame(data)




# Get descriptive statistics
desc = subway_df['Min Delay'].describe()

# Create a DataFrame from describe values
df2 = pd.DataFrame({
    "Title": ["No. of Incidents", "Delay-Mean", "Delay-Std", "Delay-Min", "Delay-25%", "Delay-50%", "Delay-75%", "Delay-Max"],
    "Value": [int(desc["count"]), int(desc["mean"]), int(desc["std"]), int(desc["min"]), int(desc["25%"]), int(desc["50%"]), int(desc["75%"]), int(desc["max"])]
})

# Combine df1 and df2
Subway_general_inf_dataframe = pd.concat([df1, df2], ignore_index=True)

