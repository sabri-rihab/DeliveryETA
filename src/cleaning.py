import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time

# df = pd.read_csv('data/dataset.csv')
# df.drop_duplicates()

# # ____________________<( Before Cleaning the Data)>___________________
print("Before Cleaning the Data")
clean_df = pd.read_csv('data/clean_data.csv')
# df = pd.read_csv('data/dataset.csv')

# clean_df = df[
#     ['Restaurant_latitude', 
#     'Restaurant_longitude', 
#     'Delivery_location_latitude', 
#     'Delivery_location_longitude', 
#     'Time_Orderd', 
#     'Time_Order_picked', 
#     'Order_Date',
#     'Weatherconditions',
#     'Road_traffic_density', 
#     'Type_o'
#     'f_order', 
#     'Type_of_vehicle', 
#     'multiple_deliveries', 
#     'City', 
#     'Time_taken(min)']
#     ]

# clean_df['Weatherconditions'] = clean_df['Weatherconditions'].str.replace('conditions ', '', regex=False).str.strip()
# clean_df['Time_taken(min)'] = clean_df['Time_taken(min)'].str.replace('(min) ', '', regex=False).str.strip()

str_column = clean_df.select_dtypes(include='string').columns
clean_df[str_column] = clean_df[str_column].apply(lambda col: col.str.strip())
clean_df['Time_taken(min)'] = pd.to_numeric(clean_df['Time_taken(min)'], errors='coerce')
clean_df['multiple_deliveries'] = pd.to_numeric(clean_df['multiple_deliveries'], errors='coerce').astype('Int64')
clean_df['multiple_deliveries'] = clean_df['multiple_deliveries'].astype('Int64')
clean_df['Time_Order_picked'] = pd.to_datetime(clean_df['Time_Order_picked'],errors='coerce').dt.time
clean_df['Time_Orderd'] = pd.to_datetime(clean_df['Time_Orderd'],errors='coerce').dt.time
clean_df[['Restaurant_latitude', 'Restaurant_longitude']] = clean_df[['Restaurant_latitude', 'Restaurant_longitude']].abs()
weather_numeric = pd.to_numeric(clean_df['Weatherconditions'], errors='coerce').notna()

# clean_df = clean_df[
#     ~(
#         (clean_df['Restaurant_latitude'] == 0.0) &
#         (clean_df['Restaurant_longitude'] == 0.0)    )
# ]

# false_weather = pd.to_numeric(clean_df['Weatherconditions'], errors='coerce')
# clean_df = clean_df[
#     ~(
#         (clean_df['Weatherconditions'] == 'NaN') &
#         (clean_df['Road_traffic_density'] == 'NaN')
#     )
# ]

# clean_df = clean_df.dropna(subset=['Time_Orderd'])
# clean_df = clean_df.dropna(subset=['multiple_deliveries'])

# print('')
# print('=====================================================================')
# print('')
# print(f'count the rows with weather & traffic none : {((clean_df['Weatherconditions'] == 'NaN') & (clean_df['Road_traffic_density'] == 'NaN')).value_counts()}')
# print(f'count the rows with weather none : {(clean_df['Weatherconditions'] == 'NaN').value_counts()}')
# print(f'count the rows with weather & traffic none : {((clean_df['Weatherconditions'] == 'NaN') & (clean_df['Road_traffic_density'] == 'NaN')).value_counts()}')
# print('')
# print('=====================================================================')
# print('')
# print(clean_df['Weatherconditions'].isna().value_counts())



# df_colummns = clean_df.columns
# for col in df_colummns:
#     print('')
#     print(clean_df[col].map(type).value_counts())
#     print('')


# _______________________<( General analyse )>________________________
# print(f"df shape : {df.shape}")
# print(f"df infos : {clean_df.info()}")
# print(f"df head : {df.head()}")
# print(f"null values : {df.isnull().sum()}")
# dupl_count = clean_df.duplicated().sum() # 0
# print(dupl_count)



# =========================( add distance column )==============================
# def calcule_distance(row):

#     restaurant = (
#         row['Restaurant_latitude'],
#         row['Restaurant_longitude']
#     )

#     client = (
#         row['Delivery_location_latitude'],
#         row['Delivery_location_longitude']
#     )

#     return geodesic(restaurant, client).km

# clean_df['distance'] = clean_df.apply(calcule_distance, axis=1)

# =========================( drop rows with no city_name nor cuty )==============================
# 173 rows were dropped !!!!
# clean_df = clean_df[~( 
#     clean_df['city_name'].isna() &
#     clean_df['City'].isna()
# )
# ]
# =========================( missing city values )==============================
#  filling the missing city values !!!!!!! 

# first : the cities that has both city&city_name duplicates are droped. it like a guide to fill the missing values
# city_type_map = (
#     clean_df
#     .dropna(subset=['city_name', 'City'])
#     [['city_name', 'City']]
#     .drop_duplicates()
# )

# verify each city_name has one city value
#  the result showed that each city_name have more than 1 city. so we will drop these rows o nethenaw 
# print(clean_df.groupby('city_name')['City'].nunique().sort_values(ascending=False))

# clean_df = clean_df.dropna(subset=['City'])
# clean_df = clean_df.drop(columns=['city_name'])
# =========================( count NaN values )==============================
# print(clean_df.isna().sum(axis=0)) #city: 1029 , city_name : 6715
# print(f'cities types that can not be saved : {(  # 173 can't be saved   / can be saved : 6542 
#     clean_df['city_name'].isna() &
#     clean_df['City'].isna()
# ).sum()}')
print('====================================================')
print(clean_df['Time_Order_picked'].dtype)
print('====================================================')
order_picked = pd.to_timedelta(clean_df['Time_Order_picked'].astype(str))
order_made = pd.to_timedelta(clean_df['Time_Orderd'].astype(str))

difference = (
    (order_picked - order_made).dt.total_seconds() / 60
).round().astype(int)

difference.loc[difference < 0] += 1440
clean_df['order_making(min)'] = difference

clean_df['delivery_time(min)'] = (clean_df['Time_taken(min)'] - clean_df['order_making(min)'])
clean_df.loc[clean_df['delivery_time(min)'] < 0 , 'delivery_time(min)'] = 0
# print(clean_df.groupby('city_name'))
# print(f'count the rows with multiple_deliveries none : {(clean_df['multiple_deliveries'] == 'NaN').value_counts()}')

# print(f"weather missing values count : {clean_df['Weatherconditions'].isna().value_counts()}")
# print(f"weather missing values count : {(clean_df['Weatherconditions'] == 'NaN').value_counts()}")
# print(f"traffic missing values count : {(clean_df['Road_traffic_density'] == 'NaN').value_counts()}")
# print(f'rows with lat & lag 0.0 : {((clean_df['Restaurant_latitude'] == 0.0) & (clean_df['Restaurant_longitude'] == 0.0)).sum()}')

# print(
#     clean_df.loc[
#         pd.to_datetime(
#             clean_df['Time_Orderd'],
#             format='%H:%M:%S'
#         ).isna(),
#         ['Time_Orderd', 'Time_Order_picked','Time_taken(min)']
#     ].value_counts()
# )



# __________<( city name column )>_____________________
# geolocator = Nominatim(user_agent="quelque_chose", timeout=10)
# count = 0
# def coordination_to_city(row):
#     global count 
#     count += 1
#     print(count)
#     location = geolocator.reverse(
#         (row['Restaurant_latitude'], row['Restaurant_longitude']),
#         language='en'
#     )
#     time.sleep(3)

#     if location is None: return None
#     return location.raw['address'].get('city')

# records = clean_df[['Restaurant_latitude', 'Restaurant_longitude']].drop_duplicates()
# print(f'how many restaurant we have : {len(records)}')
# records['city_name'] = records.apply(coordination_to_city, axis=1)
# print(records[['Restaurant_latitude', 'Restaurant_longitude', 'city_name']])
# clean_df = clean_df.merge(
#     records,
#     on=['Restaurant_latitude', 'Restaurant_longitude'],
#     how='left'
# )
# clean_df['city_name'] = clean_df.apply(coordination_to_city, axis=1)

# ______________________________________________________________
# ____________________<( Save clean data )>_____________________
clean_df.to_csv('data/clean_data.csv', index=False)


# _______________________________________________________________________
# ________________________ <( Graphs )>__________________________________
Q1 = clean_df['distance'].quantile(0.25)
Q3 = clean_df['distance'].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = clean_df[
    (clean_df['distance'] < lower) |
    (clean_df['distance'] > upper)
]

# plt.figure(figsize=(12, 6))

# Normal points, colored by city
# for city in clean_df['City'].unique():
#     city_df = clean_df[clean_df['City'] == city]

#     plt.scatter(
#         city_df['Time_taken(min)'],
#         city_df['distance'],
#         label=city
#     )
# __________________________________________________________________________________________________
# __________________<( order time(time_catg) vs time taken )_________________________________________
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
clean_df['time_category'] = clean_df['Time_Orderd'].apply(categorize_time)
clean_df.to_csv('data/clean_data.csv', index=False)
avg_time = clean_df.groupby('time_category')['Time_taken(min)'].mean()
plt.figure(figsize=(8, 5))
plt.bar(
    avg_time.index,
    avg_time.values
)
plt.xlabel('Time category')
plt.ylabel('Average time taken (min)')
plt.title('Average Delivery Time by Order Time Category')

# plt.show()


# __________________________________________________________________________________________________
# __________________<( Type_of_vehicle vs time taken )________________________________________
avg_time = clean_df.groupby('Type_of_vehicle')['Time_taken(min)'].mean()
plt.figure(figsize=(8, 5))
plt.bar(
    avg_time.index,
    avg_time.values
)
plt.xlabel('Type_of_vehicle')
plt.ylabel('Average time taken (min)')
plt.title('Average Delivery Time by Type of vehicle')

# plt.show()





# # __________________________________________________________________________________________________
# # __________________<( traffic vs time taken )________________________________________
avg_time = clean_df.groupby('Road_traffic_density')['Time_taken(min)'].mean()
plt.figure(figsize=(8, 5))
plt.bar(
    avg_time.index,
    avg_time.values
)
plt.xlabel('Road_traffic_density')
plt.ylabel('Average time taken (min)')
plt.title('Average Delivery Time by traffic density')

# plt.show()




# __________________________________________________________________________________________________
# __________________<( city type vs time taken )________________________________________
avg_time = clean_df.groupby('City')['Time_taken(min)'].mean()
plt.figure(figsize=(8, 5))
plt.bar(
    avg_time.index,
    avg_time.values
)
plt.xlabel('City')
plt.ylabel('Average time taken (min)')
plt.title('Average Delivery Time by City')

# plt.show()


print(clean_df.columns)


# # __________________________________________________________________________________________________
# # __________________<( Weather Conditions vs time taken )________________________________________
# avg_time = clean_df.groupby('Weatherconditions')['Time_taken(min)'].mean()
# plt.figure(figsize=(8, 5))
# plt.bar(
#     avg_time.index,
#     avg_time.values
# )
# plt.xlabel('Weather Conditions')
# plt.ylabel('Average time taken (min)')
# plt.title('Average Delivery Time by weather')

# plt.show()






# ___________________________________________________________________________
# ________________<( analyze the making order vs the order type )>___________
# print(f'types of orders : {clean_df['Type_of_order'].unique()}')
# we have for types of order : ['Snack', 'Drinks', 'Buffet', 'Meal']
orders = clean_df['Type_of_order'].unique()
for order in orders:
    data = clean_df.loc[clean_df['Type_of_order']== order]
    counts = data['order_making(min)'].value_counts().sort_index()
    plt.figure(figsize=(6, 4))
    plt.bar(counts.index, counts.values)
    plt.xlabel('Order making time (min)')
    plt.ylabel('Number of orders')
    plt.title(f'{order} orders')
    plt.xticks([5, 10, 15])

    # plt.show()
# result => order type had 0 impact on the time_taken


# ____________________________________________________________________________________
# ________________<( analyze the order type and time it takes to be made )>___________

# print(f'types of orders : {clean_df.groupby('Type_of_order')['order_making(min)'].describe()}')
# types of orders :                 count       mean       std  min  25%   50%   75%   max
# Type_of_order                                                         
# Buffet         9494.0  10.012113  4.105088  5.0  5.0  10.0  15.0  15.0
# Drinks         9621.0   9.937636  4.069467  5.0  5.0  10.0  15.0  15.0
# Meal           9680.0   9.969008  4.087845  5.0  5.0  10.0  15.0  15.0
# Snack          9674.0   9.998449  4.085752  5.0  5.0  10.0  15.0  15.0


# ___________________________________________________________________
# ______________<( time taken  vs distance )>_______________
plt.figure(figsize=(12, 6))
plt.scatter(
    clean_df['distance'],
    clean_df['Time_taken(min)'],
)
plt.xlabel('distance (km)')
plt.ylabel('Time_taken (min)')
plt.title('time taken  vs Distance')

# ___________________________________________________________________
# ______________<( time taken  vs order making )>_______________
plt.figure(figsize=(12, 6))
plt.scatter(
    clean_df['order_making(min)'],
    clean_df['Time_taken(min)'],
)
plt.xlabel('order making (min)')
plt.ylabel('Time_taken (min)')
plt.title('time taken  vs order making time')

# ___________________________________________________________________
# ______________<( time taken  vs delivery guy time )>_______________
plt.figure(figsize=(12, 6))
plt.scatter(
    clean_df['delivery_time(min)'],
    clean_df['Time_taken(min)'],
)
plt.xlabel('delivery_time(min)')
plt.ylabel('Time_taken (min)')
plt.title('time taken  vs delivery guy time')

# plt.show()