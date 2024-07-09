import pandas as pd
from faker import Faker
import random
import folium

fake = Faker()

tourists_data = {
    'name': [fake.name() for _ in range(100)],
    'address': [fake.address() for _ in range(100)],
    'latitude': [fake.latitude() for _ in range(100)],
    'longitude': [fake.longitude() for _ in range(100)],
    'age': [random.randint(18, 80) for _ in range(100)]
}

tourists_df = pd.DataFrame(tourists_data)

visits_data = {
    'name': [random.choice(tourists_data['name']) for _ in range(200)],
    'visit_date': [fake.date_this_decade() for _ in range(200)],
    'latitude': [fake.latitude() for _ in range(200)],
    'longitude': [fake.longitude() for _ in range(200)]
}

visits_df = pd.DataFrame(visits_data)

merged_df = pd.merge(tourists_df, visits_df, on='name')

average_age = merged_df['age'].mean()
print(f"Average age of tourists: {average_age}")

location_counts = merged_df.groupby(['latitude_y', 'longitude_y']).size().reset_index(name='count')
top_locations = location_counts.sort_values(by='count', ascending=False).head(5)
print(top_locations)

tourist_map = folium.Map(location=[20, 0], zoom_start=2)

for _, row in top_locations.iterrows():
    folium.Marker(
        location=[row['latitude_y'], row['longitude_y']],
        popup=f"Visits: {row['count']}",
        icon=folium.Icon(color='red')
    ).add_to(tourist_map)

tourist_map.save('tourist_map.html')
