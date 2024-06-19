# This script simulates the backoff algorithm. Binary Exponential Backoff

# Initial requests and assignments
requests = {
    'A': [3, 13],
    'B': [1, 3, 9],
    'C': [2, 10],
    'D': [4, 7],
    'E': [2]
}

# Random numbers for each station
random_numbers = {
    'A': [396, 5454, 13816, 4405, 2883, 6402],
    'B': [777, 2406, 9599, 3037, 5034, 99],
    'C': [1257, 3548, 736, 677, 9234, 2488],
    'D': [945, 386, 7431, 4434, 2348, 4287],
    'E': [6502, 668, 15485, 5879, 2002, 1803]
}

# Initialize the table with '-' for inactive stations
table = [['-' for _ in range(18)] for _ in range(5)]
stations = ['A', 'B', 'C', 'D', 'E']
station_index = {s: i for i, s in enumerate(stations)}

# Track the collision count for each station
collision_count = {s: 0 for s in stations}


# Function to process the time slots
def process_time_slots():
    for time_slot in range(1, 19):
        active_stations = []
        for station in stations:
            idx = station_index[station]
            if any(req <= time_slot for req in requests[station]) and not table[idx][time_slot - 1] == 'W':
                active_stations.append(station)

        if len(active_stations) > 1:
            # Collision occurred
            for station in active_stations:
                idx = station_index[station]
                table[idx][time_slot - 1] = 'X'
                collision_count[station] += 1
                backoff_time = random_numbers[station].pop(0) % (2 ** collision_count[station])
                new_time_slot = time_slot + backoff_time + 1
                if new_time_slot <= 20:
                    for wait_time_slot in range(time_slot + 1, new_time_slot):
                        if wait_time_slot <= 20:  # Ensure we don't go beyond the table
                            table[idx][wait_time_slot - 1] = 'W'
        elif len(active_stations) == 1:
            # Successful transmission
            station = active_stations[0]
            idx = station_index[station]
            requests[station].pop(0)
            table[idx][time_slot - 1] = 'S'
            collision_count[station] = 0

        # Check for stations with backoff_time = 0
        stations_with_zero_backoff = [station for station in stations if not random_numbers[station]]
        if len(stations_with_zero_backoff) == 1:
            # Only one station has backoff_time = 0, it gets an 'S'
            station = stations_with_zero_backoff[0]
            idx = station_index[station]
            table[idx][new_time_slot - 1] = 'S'
        elif len(stations_with_zero_backoff) > 1:
            # More than one station has backoff_time = 0, they have a collision
            for station in stations_with_zero_backoff:
                idx = station_index[station]
                table[idx][new_time_slot - 1] = 'X'


# Run the simulation
process_time_slots()

# Print the table
header = ['Zeitschlitz'] + [str(i) for i in range(1, 21)]
print(f"{' | '.join(header)}")
print('-' * 103)
for i, station in enumerate(stations):
    print(f"{station.ljust(11)} | {' | '.join(table[i])}")