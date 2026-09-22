import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/dataset.csv')
df.drop_duplicates()

# # ____________________<( Before Cleaning the Data)>___________________
print("Before Cleaning the Data")
df = pd.read_csv('data/dataset.csv')

clean_df = df[
    ['Restaurant_latitude', 
    'Restaurant_longitude', 
    'Delivery_location_latitude', 
    'Delivery_location_longitude', 
    'Time_Orderd', 
    'Time_Order_picked', 
    'Weatherconditions',
    'Road_traffic_density', 
    'Type_of_order', 
    'Type_of_vehicle', 
    'multiple_deliveries', 
    'City', 
    'Time_taken(min)']
    ]

clean_df['Weatherconditions'] = clean_df['Weatherconditions'].str.replace('conditions ', '', regex=False).str.strip()
clean_df['Time_taken(min)'] = clean_df['Time_taken(min)'].str.replace('(min) ', '', regex=False).str.strip()

str_column = clean_df.select_dtypes(include='string').columns
clean_df[str_column] = clean_df[str_column].apply(lambda col: col.str.strip())
clean_df['Time_taken(min)'] = pd.to_numeric(clean_df['Time_taken(min)'], errors='coerce')
clean_df['multiple_deliveries'] = pd.to_numeric(clean_df['multiple_deliveries'], errors='coerce')
clean_df['multiple_deliveries'] = clean_df['multiple_deliveries'].astype('Int64')
# _________
# __________<( Save clean data )>_____________________
clean_df.to_csv('data/clean_data.csv', index=False)

df_colummns = clean_df.columns
for col in df_colummns:
    print('')
    print(clean_df[col].map(type).value_counts())
    print('')


# _______________________<( General analyse )>________________________
# print(f"df shape : {df.shape}")
# print(f"df infos : {df.info()}")
# print(f"df head : {df.head()}")
# print(f"null values : {df.isnull().sum()}")
# dupl_count = df.duplicated().sum() # 0
# print(dupl_count)

# # ____________________<( After Cleaning the Data)>___________________

# print("After Cleaning the Data")


