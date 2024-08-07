import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from pymongo import MongoClient
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Connect to the MongoDB client
client = MongoClient('mongodb+srv://CE:project1@mzuceproject.kyvn8sq.mongodb.net/')
db = client['Data']
collection = db['Fin']

# Fetch the data from MongoDB
data = list(collection.find())


# Convert the fetched data to a DataFrame
df = pd.DataFrame(data)

# Print the columns and first few rows to debug
print("Columns in the DataFrame:", df.columns)
print("First few rows of the DataFrame:\n", df.head())


# Rename columns to fit Prophet's requirements
df.rename(columns={'DATE': 'ds', 'PRICE': 'y'}, inplace=True)


# Print the first few rows after renaming and date conversion
print("First few rows after renaming and date conversion:\n", df.head())

# Initialize the Prophet model
model = Prophet()

# Add holidays for India
model.add_country_holidays(country_name='IN')

# Exclude the time between 9 PM to 6 AM
df2 = df[df['ds'].dt.hour > 6]
df3 = df2[df2['ds'].dt.hour < 19]

# Print the first few rows after filtering
print("First few rows after filtering:\n", df3.head(7))

# Fit the model on the dataset
model.fit(df3)

# Print the summary statistics
df3_description = df3.describe()
print("Summary statistics of df3:\n", df3_description)

# Create a dataframe with future dates for forecasting
future = model.make_future_dataframe(periods=150, freq='D')

# Filter out the specific times in the future dataframe
future = future[(future['ds'].dt.hour > 7) & (future['ds'].dt.hour < 19)]

# Make the forecast
forecast = model.predict(future)

# Display the forecast
print("Forecast tail:\n", forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Plot the forecast
fig = model.plot(forecast)
fig2 = model.plot_components(forecast)

# Adjust the x-axis format to include time
fig.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S'))
fig.autofmt_xdate()

plt.show()
