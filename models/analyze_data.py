import pandas as pd
import matplotlib.pyplot as plt

# # ____________________<( Before Cleaning the Data)>___________________
print("Before Cleaning the Data")
df = pd.read_csv('data/dataset.csv')
dupl_count = df.duplicated().sum()

df_colummns = df.columns
for col in df_colummns:
    print(df[col].map(type).value_counts())
    print('')

print(f"Duplicated data : {dupl_count}")

print('*****************************')
print(f"df shape : {df.shape}")

print('*****************************')
print(f"df infos : {df.info()}")

print('*****************************')
print(f"df head : {df.head()}")

print('*****************************')
print(f"null values : {df.isnull().sum()}")

# # ____________________<( After Cleaning the Data)>___________________
# print("After Cleaning the Data")

sorted_df = df.sort_values(by='Distance_km')
# plt.boxplot(df['Preparation_Time_min'])
df = df.dropna()

sorted_df = df.sort_values(by='Delivery_Time_min')

fig, ax = plt.subplots(figsize=(20, 6))

ax.scatter(
    df['Delivery_Time_min'],
    df['Distance_km']
)

ax.set_xlabel('Delivery Time (min)')
ax.set_ylabel('Distance (km)')

plt.show()