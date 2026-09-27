import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time
from datetime import datetime, timedelta


#___________________<( DATA )>_______________________
df = pd.read_csv('data/dataset.csv')
print(f"df shape : {df.shape}")


#_______________<( parasite texte )>_________________
# remove 'condition_' and (min) parasite
df['Weatherconditions'] = df['Weatherconditions'].str.replace('conditions ', '', regex=False).str.strip()
df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min) ', '', regex=False).str.strip()


df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'], errors='coerce')

# correct missing age/rating/multi_delevery
df['Delivery_person_Age'] = pd.to_numeric( df['Delivery_person_Age'].str.strip(),errors='coerce' )
df['Delivery_person_Ratings'] = pd.to_numeric( df['Delivery_person_Ratings'].str.strip(),errors='coerce' )

df['multiple_deliveries'] = pd.to_numeric(df['multiple_deliveries'], errors='coerce').astype('Int64')
df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce').astype('Int64')
df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')


# time type correction
df['Time_Order_picked'] = pd.to_datetime(df['Time_Order_picked'],errors='coerce').dt.time
df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'],errors='coerce').dt.time

# lat/lag correction
df[['Restaurant_latitude', 'Restaurant_longitude']] = df[['Restaurant_latitude', 'Restaurant_longitude']].abs()

# remove lat/lag == 0
df = df[
    ~(
        (df['Restaurant_latitude'] == 0.0) &
        (df['Restaurant_longitude'] == 0.0)    )
]

# replace the Time_Orderd missing values with Time_Order_picked - 10 min
df.loc[df['Time_Orderd'].isna(), 'Time_Orderd'] = (
    df.loc[df['Time_Orderd'].isna(), 'Time_Order_picked']
    .apply(lambda x: (
        datetime.combine(datetime.today(), x) - timedelta(minutes=10)
    ).time())
)


# replace the age, rating, multi_deleveries missing values
df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].fillna(
    df['Delivery_person_Ratings'].median()
)

df['Delivery_person_Age'] = df['Delivery_person_Age'].fillna(
    df['Delivery_person_Age'].median()
)

df['multiple_deliveries'] = df['multiple_deliveries'].fillna(
    df['multiple_deliveries'].mode()[0]
)

#  remove the rows where weather condition has a numeric value
df = df[pd.to_numeric(df['Weatherconditions'], errors='coerce').isna()]

# remove the rows that has "NaN" from traffic and weather
df = df[
    ~(
        (df['Weatherconditions'] == 'NaN') &
        (df['Road_traffic_density'] == 'NaN')
    )
]

# correct Festival column 
df['Festival'] = df['Festival'].str.strip()
df.loc[~df['Festival'].isin(['Yes', 'No']), 'Festival'] = pd.NA
df['Festival'] = df['Festival'].fillna(
    df['Festival'].mode()[0]
)

#_______________<( detect none values )>_________________

# print(f'time_orderd : {df['Time_Orderd'].isna().sum()}')
# print(f'multi delivery : {df['multiple_deliveries'].isna().sum()}')
# print(f'age  : {df['Delivery_person_Age'].isna().sum()}')
# print(f'rating : {df['Delivery_person_Ratings'].isna().sum()}')
# print(f'rest lat : {df['Restaurant_latitude'].isna().sum()}')
# print(f'rest lag : {df['Restaurant_longitude'].isna().sum()}')
# print(f'delevery lag : {df['Delivery_location_latitude'].isna().sum()}')
# print(f'delevery lag : {df['Delivery_location_longitude'].isna().sum()}')


# print("age values equal to 'NaN':", 
#       (df['Delivery_person_Age'] == 'NaN ').sum())
# print("rating values equal to 'NaN':", 
#       (df['Delivery_person_Ratings'] == 'NaN ').sum())

# __________________________<( Test my cleaning )>_____________________
# print(df['Weatherconditions'].isna().value_counts())


# shape of the data :
# print(f"df shape : {df.shape}")



# __________________________<( Test the column data type )>_____________________
df_colummns = df.columns
for col in df_colummns:
    print('')
    print(df[col].map(type).value_counts())
    print('')


# avg_time = df.groupby('Type_of_order')['Time_taken(min)'].mean()
# plt.figure(figsize=(8, 5))
# plt.bar(
#     avg_time.index,
#     avg_time.values
# )
# plt.xlabel('Type_of_order')
# plt.ylabel('Average time taken (min)')
# plt.title('Average Delivery Time by Type_of_order')

# plt.show()

# ________________________<( add column )>_____________________
def categorize_time(t):
    if pd.isna(t):
        return None

    hour = t.hour

    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 22:
        return 'Evening'
    else:
        return 'Night'
df['time_category'] = df['Time_Orderd'].apply(categorize_time)


# order picked
order_picked = pd.to_timedelta(df['Time_Order_picked'].astype(str))
order_made = pd.to_timedelta(df['Time_Orderd'].astype(str))

difference = (
    (order_picked - order_made).dt.total_seconds() / 60
).round().astype(int)

difference.loc[difference < 0] += 1440
df['order_making(min)'] = difference

df['delivery_time(min)'] = (df['Time_taken(min)'] - df['order_making(min)'])
df.loc[df['delivery_time(min)'] < 0 , 'delivery_time(min)'] = 0


# add is_weekend column   ====> it has no effect, yuuuuuup 
# df['is_weekend'] = (
#     pd.to_datetime(df['Order_Date']).dt.dayofweek >= 5
# ).astype(int)

# avg_time = df.groupby('is_weekend')['Time_taken(min)'].mean()
# plt.figure(figsize=(8, 5))
# plt.bar(
#     avg_time.index,
#     avg_time.values
# )

# plt.xticks([0, 1], ['False', 'True'])
# plt.xlabel('is_weekend')
# plt.ylabel('Average time taken (min)')
# plt.title('Average Delivery Time by is_weekend')

# plt.show()
# ________________<( delete unecessary columns )>______________


df = df.drop(columns=['Delivery_person_ID', 'ID', 'Type_of_order', 'Order_Date'])



# _________________________<( save the cleane data )>______________________
df.to_csv('data/2_clean_data.csv', index=False)

# ______________________________________________________________
# ____________________<( RESULT!!!!!!!!!! )>____________________
# ================> random forest <=====================
# TRAINING SET
# MAE:  3.78 minutes
# MSE:  23.92
# RMSE: 4.89 minutes
# R²:   0.7296

# TEST SET
# MAE:  3.95 minutes
# MSE:  25.77
# RMSE: 5.08 minutes
# R²:   0.7009

# ___________________ After random search _____________________________
# TRAINING SET
# MAE:  2.51 minutes
# MSE:  10.69
# RMSE: 3.27 minutes
# R²:   0.8792

# TEST SET
# MAE:  3.75 minutes
# MSE:  23.06
# RMSE: 4.80 minutes
# R²:   0.7324

# ================> linear regression <=====================
# TRAINING SET
# MAE:  4.79 minutes
# MSE:  36.17
# RMSE: 6.01 minutes
# R²:   0.5910

# TEST SET
# MAE:  4.75 minutes
# MSE:  35.96
# RMSE: 6.00 minutes
# R²:   0.5827


# ================> decision tree <=====================
# TRAINING SET
# MAE:  3.87 minutes
# MSE:  25.54
# RMSE: 5.05 minutes
# R²:   0.7113

# TEST SET
# MAE:  4.12 minutes
# MSE:  28.17
# RMSE: 5.31 minutes
# R²:   0.6731


# ================> gradient boosting <=====================
# TRAINING SET
# MAE:  4.07 minutes
# MSE:  26.64
# RMSE: 5.16 minutes
# R²:   0.6988

# TEST SET
# MAE:  4.08 minutes
# MSE:  26.93
# RMSE: 5.19 minutes
# R²:   0.6875


# ================> gradient boosting <=====================
# TRAINING SET
# MAE:  3.90 minutes
# MSE:  25.69
# RMSE: 5.07 minutes
# R²:   0.7096

# TEST SET
# MAE:  4.06 minutes
# MSE:  27.19
# RMSE: 5.21 minutes
# R²:   0.6845