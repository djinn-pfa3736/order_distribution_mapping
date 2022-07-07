import pandas as pd
import numpy as np
import datetime

import matplotlib

import pdb

import folium

df = pd.read_csv('query_result_20201204.csv')

# date_vec = []
day_lat_dict = {}
day_lng_dict = {}
total_lat_vec = []
total_lng_vec = []
for i in range(len(df)):
    start_date = datetime.datetime(2020, 11, 1)
    end_date = datetime.datetime(2020, 11, 30)

    created = datetime.datetime.strptime(df.iloc[i,7], '%Y-%m-%dT%H:%M:%SZ')
    delta_start = created - start_date
    delta_end = end_date - created
    if (0 <= delta_start.days) and (0 <= delta_end.days):
        adjusted = created + datetime.timedelta(hours=9)
        created_day = adjusted.day
        if df.iloc[i,8] == df.iloc[i,8]:
            deleted = datetime.datetime.strptime(df.iloc[i,7], '%Y-%m-%dT%H:%M:%SZ')
            diff = deleted - created
            if 10 < diff.seconds:

                if created_day in day_lat_dict:
                    # date_vec.append(ajusted.strftime('%Y-%m-%dT%H:%M:%S'))
                    day_lat_dict[created_day].append(df.iloc[i,2])
                    day_lng_dict[created_day].append(df.iloc[i,3])
                    total_lat_vec.append(df.iloc[i,2])
                    total_lng_vec.append(df.iloc[i,3])
                else:
                    day_lat_dict[created_day] = [df.iloc[i,2]]
                    day_lng_dict[created_day] = [df.iloc[i,3]]
                    total_lat_vec.append(df.iloc[i,2])
                    total_lng_vec.append(df.iloc[i,3])

        else:
            if created_day in day_lat_dict:
                # date_vec.append(ajusted.strftime('%Y-%m-%dT%H:%M:%S'))
                day_lat_dict[created_day].append(df.iloc[i,2])
                day_lng_dict[created_day].append(df.iloc[i,3])
                total_lat_vec.append(df.iloc[i,2])
                total_lng_vec.append(df.iloc[i,3])
            else:
                day_lat_dict[created_day] = [df.iloc[i,2]]
                day_lng_dict[created_day] = [df.iloc[i,3]]
                total_lat_vec.append(df.iloc[i,2])
                total_lng_vec.append(df.iloc[i,3])

# result_df = pd.DataFrame({'Date': date_vec, 'Lat': lat_vec, 'Lng': lng_vec})
# result_df.to_csv('order_mapping.csv')

# print(matplotlib.colors.cnames)
values = list(matplotlib.colors.cnames.values())
# print(len(values))
keys = list(day_lat_dict.keys())
# print(len(keys))
keys = np.sort(keys)
map_dict = {}
for i in range(len(keys)):
    # print(values[i])
    key = keys[i]
    col_idx = i % 7

    if col_idx not in map_dict:
        map_dict[col_idx] = folium.Map(location=[np.median(total_lat_vec), np.median(total_lng_vec)], zoom_start=15)

    lat_vec = day_lat_dict[key]
    lng_vec = day_lng_dict[key]
    for j in range(len(lat_vec)):
        folium.Marker(location=[lat_vec[j], lng_vec[j]], popup=str(key), icon=folium.Icon(color='blue', icon_color=values[col_idx])).add_to(map_dict[col_idx])

for map_key in map_dict.keys():
    map_dict[map_key].save('order_map_' + str(map_key) + '.html')
