%matplotlib inline
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# File to Load (Remember to change these)
city_data_to_load = pd.read_csv("data/city_data.csv")
ride_data_to_load = pd.read_csv("data/ride_data.csv")

# Read the City and Ride Data
# Combine the data into a single dataset
merged_df = pd.merge(city_data_to_load, ride_data_to_load, how='inner')
groupedCity_df = merged_df.groupby("city")

#glance at the grouped data...
groupedCity_df.head()

totalFare = groupedCity_df["fare"].sum()
countFare = groupedCity_df["fare"].count()
totalRides = groupedCity_df["city"].count()
totalDrivers = groupedCity_df["driver_count"].sum()
averageFare = groupedCity_df["fare"].mean()

# Display the data table for preview
city_df = merged_df.drop_duplicates(subset="city")
city_df.drop(["driver_count", "date", "fare", "ride_id"], axis=1, inplace=True)
city_df.head()

countFare_df = pd.DataFrame(countFare)
totalRides_df = pd.DataFrame(totalRides)
totalDrivers_df = pd.DataFrame(totalDrivers)
averageFare_df = pd.DataFrame(averageFare)
totalRides_df.rename(columns={"city":"Total_Rides"}, inplace=True)
countFare_df.reset_index(inplace = True)
totalRides_df.reset_index(inplace = True)
totalDrivers_df.reset_index(inplace = True)
averageFare_df.reset_index(inplace = True)
groupedCityStats = pd.merge(pd.merge(pd.merge(pd.merge(city_df, countFare_df, on="city"), totalRides_df, on="city"), totalDrivers_df, on="city"), averageFare_df, on="city")
groupedCityStats_replace = groupedCityStats.rename(columns={"fare_y":"Average_Fare"})
groupedCityStats_replace.drop(["fare_x"], axis = 1, inplace=True)
groupedCityStats_replace.head()
urbanCities = groupedCityStats_replace.loc[(groupedCityStats["type"] == "Urban")]
suburbanCities = groupedCityStats_replace.loc[(groupedCityStats["type"] == "Suburban")]
ruralCities = groupedCityStats_replace.loc[(groupedCityStats["type"] == "Rural")]

# Obtain the x and y coordinates for each of the three city types
# Build the scatter plots for each city types
ax = urbanCities.plot(kind='scatter', x="Total_Rides", y="Average_Fare", edgecolors = "Black", linewidths = 0.4, color="LightCoral", s=urbanCities["driver_count"]/4, alpha=0.8, label="Urban")
suburbanCities.plot(kind='scatter', x="Total_Rides", y="Average_Fare", edgecolors = "Black", linewidths = 0.4, color="LightSkyBlue", s=suburbanCities["driver_count"]/4, alpha=0.8, label="Suburban", ax=ax)
ruralCities.plot(kind='scatter', x="Total_Rides", y="Average_Fare", edgecolors = "Black", linewidths = 0.4, color="Gold", s=ruralCities["driver_count"]/4, alpha=0.8, label="Rural", ax=ax)

# Incorporate the other graph properties
plt.title("Pyber Ride Sharing Data (2016)")
plt.ylabel("Average Fare ($)")
plt.xlabel("Total Number of Rides (Per City)")
plt.grid()

# Create a legend
lgnd = plt.legend(loc="upper right", scatterpoints=1, title="City Types")

# Incorporate a text label regarding circle size
lgnd.legendHandles[0]._sizes = [20]
lgnd.legendHandles[1]._sizes = [20]
lgnd.legendHandles[2]._sizes = [20]

# Save Figure
plt.savefig("../Images/BubblePlot.png")
plt.show()

# Calculate Type Percents
colorTypes = ["gold", "lightskyblue", "lightcoral"]
cityTotalFare = merged_df["fare"].sum()
groupType_df = merged_df.groupby("type")
groupTypeFare = groupType_df["fare"].sum()
groupTypeFare_df = pd.DataFrame(groupTypeFare)

# Build Pie Chart
percentFare = groupTypeFare_df["fare"]/cityTotalFare
groupTypeFare_df["% Total Fares"] = percentFare
groupTypeFare_df.reset_index(inplace=True)
groupTypeFare_df.rename(columns={"type":"City Type"}, inplace=True)
farePieChart = groupTypeFare_df.plot(kind="pie", y="% Total Fares", title="% of Total Fares by City Type", labels=["Rural", "Suburban", "Urban"],
                             colors=colorTypes, autopct="%2.1f%%", explode = [0, 0, 0.1], shadow=True, startangle=145, legend=False)
farePieChart.set_ylabel('')
plt.axis('equal')

# Save Figure
plt.savefig("../Images/GroupCityTypeFare.png")

# Calculate Ride Percents
cityTotalRide = merged_df["ride_id"].count()
groupTypeRides = groupType_df["ride_id"].count()
groupTypeRides_df = pd.DataFrame(groupTypeRides)
percentRides = groupTypeRides_df["ride_id"]/cityTotalRide
groupTypeRides_df["% Total Rides"] = percentRides
groupTypeRides_df.head()

# Build Pie Chart
ridesPieChart = groupTypeRides_df.plot(kind="pie", y="% Total Rides", title="% of Total Rides by City Type", labels=["Rural", "Suburban", "Urban"],
                             colors=colorTypes, autopct="%2.1f%%", explode = [0, 0, 0.1], shadow=True, startangle=145, legend=False)
ridesPieChart.set_ylabel('')
plt.axis('equal')

# Save Figure
plt.savefig("../Images/GroupCityTypeRides.png")
plt.show()

# Calculate Driver Percents
cityTotalDrivers = merged_df["driver_count"].sum()
groupTypeDrivers = groupType_df["driver_count"].sum()
groupTypeDrivers_df = pd.DataFrame(groupTypeDrivers)
percentDrivers = groupTypeDrivers_df["driver_count"]/cityTotalDrivers
groupTypeDrivers_df["% Total Drivers"] = percentDrivers

# Build Pie Charts
driversPieChart = groupTypeDrivers_df.plot(kind="pie", y="% Total Drivers", title="% of Total Drivers by City Type", labels=["Rural", "Suburban", "Urban"],
                             colors=colorTypes, autopct="%2.1f%%", explode = [0, 0, 0.1], shadow=True, startangle=145, legend=False)
driversPieChart.set_ylabel('')
plt.axis('equal')

# Save Figure
plt.savefig("../Images/GroupCityTypeDrivers.png")
plt.show()