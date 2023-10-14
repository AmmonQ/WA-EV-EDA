import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.title("Exploratory Data Analysis for Electric Vehicle Registration in Washington State Counties")
st.title("Retrieved data from https://catalog.data.gov/dataset/electric-vehicle-population-size-history-by-county")

# data pulled from https://catalog.data.gov/dataset/electric-vehicle-population-size-history-by-county
dataframe = pd.read_csv("Electric_Vehicle_Population_Size_History_By_County.csv")
dataframe['Date'] = pd.to_datetime(dataframe['Date'])

# electric passenger vehicles
passenger_vehicles = dataframe[dataframe['Vehicle Primary Use'] == 'Passenger']

# electric struck vehicles
truck_vehicles = dataframe[dataframe['Vehicle Primary Use'] == 'Truck']

passenger_vehicles[passenger_vehicles['County'] == 'King'].sort_values('Date')
passenger_vehicles_physically_located_in_wa = passenger_vehicles[passenger_vehicles['State'] == 'WA']
st.write("EVs Registered in WA physically located in WA")
# st.write(passenger_vehicles_physically_located_in_wa)

graph1 = sns.lineplot(data=passenger_vehicles_physically_located_in_wa.groupby(['Date'])['Electric Vehicle (EV) Total'].sum().reset_index(name = 'Total EVs Registered'), y="Total EVs Registered", x="Date")
graph1.set_title("Electric Vehicle (EV) Registration by Date in Entire WA State")
graph1.set_xticklabels(graph1.get_xticklabels(), rotation=90, fontsize = 10)
st.pyplot(graph1.figure)

st.write("Total EVs Registered in WA physically located in WA by date")
st.write(passenger_vehicles_physically_located_in_wa.groupby(['Date'])['Electric Vehicle (EV) Total'].sum().reset_index(name = 'Total EVs Registered'))

# which counties in WA have the most electic vehicles registered in them and physically located in them?
total_registrations_by_county = passenger_vehicles_physically_located_in_wa.groupby(['County'])['Electric Vehicle (EV) Total'].sum().reset_index(name = 'Total EVs Registered')
total_registrations_by_county.sort_values('Total EVs Registered', ascending=False)

# top 3 counties by EVs registered
st.write("Top 3 WA Counties Sorted by Registered EVs")
top_3 = total_registrations_by_county.sort_values('Total EVs Registered', ascending=False).head(3)
top_3.style.set_caption("Washington State Counties with Highest Amount of EVs Registered")
st.write(top_3)

# lowest 3 counties by EVs registered
st.write("Bottom 3 WA Counties Sorted by Registered EVs")
lowest_3 = total_registrations_by_county.sort_values('Total EVs Registered', ascending=True).head(3)
lowest_3.style.set_caption("Washington State Counties with Lowest Amount of EVs Registered")
st.write(lowest_3)

# top 3 dates (months) EVs were registered in King county
st.write("Top 3 dates (months) EVs were registered in King county")
result_king = passenger_vehicles_physically_located_in_wa[passenger_vehicles_physically_located_in_wa['County'] == 'King'].nlargest(3, 'Electric Vehicle (EV) Total')
st.write(result_king)

# top 3 dates (months) EVs were registered in Snohomish county
st.write("Top 3 dates (months) EVs were registered in Snohomish county")
result_snohomish = passenger_vehicles_physically_located_in_wa[passenger_vehicles_physically_located_in_wa['County'] == 'Snohomish'].nlargest(3, 'Electric Vehicle (EV) Total')
st.write(result_snohomish)

# top 3 dates (months) EVs were registered in Pierce county
st.write("Top 3 dates (months) EVs were registered in Pierce county")
result_pierce = passenger_vehicles_physically_located_in_wa[passenger_vehicles_physically_located_in_wa['County'] == 'Pierce'].nlargest(3, 'Electric Vehicle (EV) Total')
st.write(result_pierce)

st.write("EVs Registered in County and Date")
select_county = st.selectbox(
    'Select a county',
    passenger_vehicles_physically_located_in_wa['County'].sort_values().unique()
)
select_date = st.selectbox(
    'Select a date',
    passenger_vehicles_physically_located_in_wa['Date'].sort_values().unique()
)

user_query = passenger_vehicles_physically_located_in_wa[(passenger_vehicles_physically_located_in_wa['County'] == select_county)
         & (passenger_vehicles_physically_located_in_wa['Date'] == select_date)]
st.write(user_query)

user_query2 = passenger_vehicles_physically_located_in_wa[(passenger_vehicles_physically_located_in_wa['County'] == select_county)]
total_ev_sum = user_query2['Electric Vehicle (EV) Total'].sum()
st.write("Total EVs Registered in County: ", total_ev_sum)


st.write("Predict how many EVs in WA State will be registered by projected date (use the format YYYY-MM-31 00:00:00)")

# predict how many EVs will be registered. Relevant columns are Date, County, and Electric Vehicle (EV) Total
# use linear regression to predict the number of EVs registered in the future
from sklearn.linear_model import LinearRegression

# Independent variables: Date, County
# Dependent variable: Electric Vehicle (EV) Total
X = passenger_vehicles_physically_located_in_wa[['Date', 'County']]
y = passenger_vehicles_physically_located_in_wa['Electric Vehicle (EV) Total']

# convert Date and County to numerical values
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X['Date'] = le.fit_transform(X['Date'])
X['County'] = le.fit_transform(X['County'])

model = LinearRegression().fit(X, y)
r_sq = model.score(X, y)

month_input = st.text_input("Enter a projected date")
county_input = st.selectbox(
    'County',
    passenger_vehicles_physically_located_in_wa['County'].sort_values().unique()
)

X_new = pd.DataFrame({'Date': [month_input, '2025-10-31 00:00:00', '2026-10-31 00:00:00', '2027-09-31 00:00:00', '2028-11-31 00:00:00'], 'County': [county_input, 'Garfield', 'King', 'Pierce', 'Snohomish']})

# st.write(X_new)

X_new['Date'] = le.fit_transform(X_new['Date'])
X_new['County'] = le.fit_transform(X_new['County'])

# st.write(X_new)

y_pred_new = model.predict(X_new)
st.write(y_pred_new[0])