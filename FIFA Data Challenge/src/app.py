import math
import pandas as pd

tracking_data = pd.read_csv('../data/tracking.csv')
events_data = pd.read_csv('../data/events.csv')

#print(tracking_data)
#print(events_data)

# EXERCISE 1
print("------------------------------------")
print("EXERCISE 1")

tracking_data['time'] = tracking_data['t']/1000 
init_time = events_data.loc[events_data['event'] == 'Kick Off']['time'][0]
events_data['reset_time'] = events_data['time'] - init_time

events_data.player_id.fillna(-1, inplace=True)
events_data.player_id = events_data.player_id.astype('int64')

join = pd.merge_asof(events_data, tracking_data, left_on=['reset_time'], right_on=['time'], left_by='player_id', right_by='id_actor')

result = join[['event_id','half_time', 'reset_time', 'player_id', 'team_id', 'event', 'x', 'y']]
print(result)

# EXERCISE 2
print("------------------------------------")
print("EXERCISE 2")

ball = tracking_data.loc[(tracking_data['id_actor'] == -1)]

grouped = events_data.groupby(events_data.event)

out_of_play = grouped.get_group("Ball Out of Play")

first_ball_out_of_play_time = out_of_play.iloc[0]['reset_time']

ball_trajectory = ball[ball['time'] < first_ball_out_of_play_time]

total_distance = 0

last_x = ball_trajectory.iloc[0]['x']
last_y = ball_trajectory.iloc[0]['y']
        
for row in ball_trajectory.itertuples():

    x = row[5]
    y = row[6]

    distance = math.dist([last_x, last_y], [x, y])
    total_distance += distance
    
    last_x = x
    last_y = y
    
print(total_distance/100)

# EXERCISE 3
print("------------------------------------")
print("EXERCISE 3")

status = []

for index, row in events_data.iterrows():
    if row['event'] == 'Pass' or row['event'] == 'Cross':
        if row['team_id'] == events_data.iloc[index + 1]['team_id']:
            status.append(1)
        else:
            status.append(0)
    else:
        status.append(None)

events_data['status'] = status

print(events_data)

# EXERCISE 4
print("------------------------------------")
print("EXERCISE 4")

passes = events_data[(events_data["event"]=='Pass') | (events_data["event"]=='Cross')]

player_passes = passes.groupby(['player_id']).size().reset_index(name='total_passes').sort_values('total_passes', ascending=False)
print(player_passes.iloc[0])


accurate_passes = passes[passes["status"]==1].groupby(['player_id']).size().reset_index(name='accurate_passes').sort_values('accurate_passes', ascending=False)

passes_ratio = pd.merge(player_passes, accurate_passes, left_on='player_id', right_on='player_id')

passes_ratio['ratio'] = passes_ratio['accurate_passes'] * 100 / passes_ratio['total_passes']

print(passes_ratio.iloc[passes_ratio['ratio'].idxmax()])