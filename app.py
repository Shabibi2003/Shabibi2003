import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar

df = pd.read_csv('final.csv', parse_dates=['date'], index_col='date')  # Adjust path if needed

features = ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']

daily_data = df.resample('D').mean()

# Streamlit UI components
st.title("Calendar Heatmaps of Environmental Features")
st.text("Only May data is Stored in Dataset")
selected_feature = st.selectbox("Select a feature", features)

# Filter data for the selected feature
feature_data = daily_data[[selected_feature]]

# Get unique months and years from the dataset
months = sorted(daily_data.index.month.unique())
selected_month = st.selectbox("Select a month", months)

# Prepare data for the selected month
month_data = feature_data[feature_data.index.month == selected_month]

# Get the number of days in the selected month and year
num_days = calendar.monthrange(month_data.index.year.min(), selected_month)[1]

# Create a calendar-like structure (5 or 6 rows with 7 columns)
calendar_data = np.full((5, 7), np.nan)  # 6 weeks for months with up to 31 days

# Populate the calendar grid with feature values
for day in range(1, num_days + 1):
    day_data = month_data[month_data.index.day == day]
    # Get the corresponding row and column in the calendar grid
    row = (day + calendar.monthrange(month_data.index.year.min(), selected_month)[0] - 1) // 7
    col = (day + calendar.monthrange(month_data.index.year.min(), selected_month)[0] - 1) % 7
    calendar_data[row, col] = day_data[selected_feature].values[0] if not day_data.empty else np.nan

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the calendar with the feature values
sns.heatmap(calendar_data, cmap='paired', annot=True, fmt=".1f", 
            cbar_kws={'label': f'Average {selected_feature}'}, ax=ax, 
            xticklabels=[ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat','Sun'],
            yticklabels=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            square=True)

# Title and labels
ax.set_title(f'Calendar Heatmap of {selected_feature} for {calendar.month_name[selected_month]} {month_data.index.year.min()}')
ax.set_xlabel('Weekday')
ax.set_ylabel('Week')

# Render the plot in Streamlit
st.pyplot(fig)
