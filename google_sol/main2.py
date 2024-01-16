
from itertools import combinations
from itertools import permutations
import heapq
import pandas as pd
import json
from tqdm import tqdm
import re

global_shortest_path = float('infinity')

LOWER_BOUND = 1
UPPER_BOUND = 8

combinations_bag1 = []

for r in range(LOWER_BOUND, UPPER_BOUND + 1):  # +1 to include the upper bound
    combinations_bag1.extend(combinations(elements_left, r))

data_left = []

# Generate combinations of bag 2 and bag 3 elements based on bag 1 combinations
for i in tqdm(range(len(combinations_bag1))):
    bag1_combination = combinations_bag1[i]
    remaining_elements = [
        e for e in elements_left if e not in bag1_combination]

    # +1 to include the upper bound
    for r in range(LOWER_BOUND, min(len(remaining_elements), UPPER_BOUND + 1)):
        for bag2_combination in combinations(remaining_elements, r):
            bag3_combination = tuple(
                e for e in remaining_elements if e not in bag2_combination)
            # Ensure bag3 has between LOWER_BOUND and UPPER_BOUND stops
            if LOWER_BOUND <= len(bag3_combination) <= UPPER_BOUND:
                data_left.append(
                    [bag1_combination+('school',), bag2_combination+('school',), bag3_combination+('school',)])


print(f"left combos = {len(data_left)}")
# data_left = list(set(data_left))
# print(int(len(data_left)/2))
# quit()

# calculate data right ==============================================================================================================================
# Generate all combinations of bag 1 elements (4 to 7 elements)
combinations_bag1 = []
for r in range(4, 8):
    combinations_bag1.extend(combinations(elements_right, r))

# Generate all combinations of bag 2 elements (11 - number of elements in bag 1)
combinations_bag2 = []
for bag1_combination in combinations_bag1:
    bag2_combination = tuple(
        e for e in elements_right if e not in bag1_combination)
    combinations_bag2.append(bag2_combination)

data_right = []

for i, (bag1, bag2) in enumerate(zip(combinations_bag1, combinations_bag2), start=1):
    # if i == len(combinations_bag2)/2:
    #     break
    data_right.append([bag1+('school',), bag2+('school',)])

# with open('assets/combs_output_ascii_right.json', 'r') as f:
#     data_right = json.load(f)


def turn_to_list(s):

    def add_lists(list1):
        order = ['小时', '分钟', '公里', '个红绿灯']
        result = []
        groups = {}

        for item in list1:
            match = re.match(r'([\d.]+)(\D+)', item)
            if match:
                num, unit = match.groups()
                num = float(num)
                if unit not in groups:
                    groups[unit] = 0
                groups[unit] += num

        for unit in order:
            if unit in groups:
                result.append(f'{groups[unit]}{unit[:2]}')

        return result

    s = list(s)
    s.reverse()

    result = []
    cur = []
    for i in range(len(s)):
        cur.append(s[i])
        if i == len(s)-1 or not ((not s[i].isdigit()) or (s[i].isdigit() and (s[i+1].isdigit()) or s[i+1] == '.')) and s[i] != '.':
            cur.reverse()
            result.append(''.join(cur))
            cur = []

    result.reverse()

    result = add_lists(result)

    return result


def evaluate_comb(comb):
    sum_times = 0
    for c in comb:
        sum_times += c[0]
    return sum_times


def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        # The node with the shortest distance from start
        current_distance, current_node = heapq.heappop(queue)

        # Ensure not to process a node more than once
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            # Only update if the new path is shorter
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct the shortest path
    path = []
    while current_node:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path = path[::-1]

    return distances[end], path

    # Test the dijkstra function for one pair of nodes
    # dijkstra(graph, test_start, test_end)


def find_shortest_path_for_group(graph, group):
    """
    Find the shortest path that connects all nodes in the group.
    Returns the shortest path and its length.
    """
    global global_shortest_path

    # Compute all pair shortest paths for nodes in the group
    pair_shortest_paths = {}
    for i in range(len(group)):
        for j in range(len(group)):
            if i != j:
                distance, _ = dijkstra(graph, group[i], group[j])
                pair_shortest_paths[(group[i], group[j])] = distance

    # Brute-force approach to solve TSP for the group
    shortest_path_length = float('infinity')
    shortest_path = []

    # Iterate over all possible permutations of nodes in the group
    for perm in permutations(group):
        current_path_length = sum(pair_shortest_paths[(
            perm[i], perm[i+1])] for i in range(len(perm)-1))
        # Check if current path exceeds the global shortest path
        if current_path_length < shortest_path_length:
            shortest_path_length = current_path_length
            shortest_path = perm

    # Update the global shortest path if needed
    if shortest_path_length < global_shortest_path:
        global_shortest_path = shortest_path_length

    return shortest_path_length, shortest_path


def main_func(time, left, school, extra=None):
    dist = not time
    right = not left

    # Convert the dataframe into a dictionary representing the graph

    print()
    print(f'{time = }\t{dist = }\t{left = }\t{right = }\t{school = }\t')

    results = []

    if left:
        df = df_left_time
    # elif left and dist:
        # df = df_left_dist
    elif right:
        df = df_right_time
        print('righting')
    # elif right and dist:
        # df = df_right_dist
    else:
        print("???")
        quit()

    if left and school:
        data = school_left_clustered
    elif left and not school:
        data = data_left
    elif right and school:
        data = school_right
    elif right and not school:
        data = data_right
    else:
        print("???")
        quit()

    graph = {}
    x = 0
    choice = ['time', 'dist'][1]
    for i, row in df.iterrows():
        node = row[0]
        graph[node] = {}
        for col, weight in row[1:].items():
            if not pd.isna(weight):
                if not time:
                    time_val = turn_to_list(weight)
                    km_found = any('公里' in item for item in time_val)
                    if km_found:
                        time_val = float(
                            [x for x in time_val if '公里' in x][0][:-2])
                    else:
                        print(str(i)+'??'+weight)
                else:
                    time_val = turn_to_list(weight)
                    min_found = any('分钟' in item for item in time_val)
                    hour_found = any('小时' in item for item in time_val)

                    if min_found and not hour_found:
                        time_val = float(
                            [x for x in time_val if '分钟' in x][0][:-2])
                    elif min_found and hour_found:
                        time_val = float([x for x in time_val if '分钟' in x][0][:-2]) + \
                            float([x for x in time_val if '小时' in x][0][:-2]) * 60
                    elif not min_found and hour_found:
                        time_val = float(
                            [x for x in time_val if '小时' in x][0][:-2]) * 60
                    else:
                        print('?????')
                        quit()

                graph[node][col] = time_val

    if school:
        result = []

        sum_ttls = 0

        for i, bus in enumerate(data[0]):
            # print(f'\nevaluating bus {bus}')
            ttl = 0
            for j in range(len(bus)-1):
                # print(f'adding {graph[bus[j]][bus[j+1]]}')
                ttl += graph[bus[j]][bus[j+1]]
            result.append([ttl, bus])
            sum_ttls += ttl

        print(result)
        print(f'{sum_ttls=}')
        return result

    for i in tqdm(range(len(data))):
        group_set = data[i]
        result_set = []
        for group in group_set:
            path_length, path = find_shortest_path_for_group(graph, group)

            # [0] for time ; [1] for km
            # min_to_school_time = min(float(dis_2_school[path[-1]][selection_index][:-2]), float(dis_2_school[path[0]][selection_index][:-2]))
            # if len(data) == 1:
            #     min_to_school_time = float(dis_2_school[path[-1]][selection_index][:-2])
            # result_set.append((path_length, min_to_school_time, i, path))
            result_set.append((path_length, i, path))
        results.append(result_set)

    sorted_results = sorted(results, key=evaluate_comb)
    min_time = evaluate_comb(sorted_results[0])

    # for s in sorted_results[:10]:
    #     print(evaluate_comb(s))

    print(sorted_results[0])
    print(f'{min_time=}')
    print()

    return min_time

# graph = {}
# for i, row in df_left_time.iterrows():
#     node = row[0]
#     graph[node] = {}
#     for col, weight in row[1:].items():
#         if not pd.isna(weight):
#             graph[node][col] = weight

# print(find_shortest_path_for_group(graph, abbrv1))
# print(find_shortest_path_for_group(graph, abbrv2))

# graph = {}
# for i, row in df_left_dist.iterrows():
#     node = row[0]
#     graph[node] = {}
#     for col, weight in row[1:].items():
#         if not pd.isna(weight):
#             graph[node][col] = weight

# print(find_shortest_path_for_group(graph, abbrv1))
# print(find_shortest_path_for_group(graph, abbrv2))

# quit()


for x in [False]:
    for y in [True]:
        for z in [True, False]:
            if z:
                res = main_func(x, y, z)
            else:
                res = main_func(x, y, z)
            # compiled["left" if y else "right"]["school" if y else "code"]["time" if x else "dist"] = res

# print(x)

# output = ""
# for side, side_data in compiled.items():
#     output += f"{side}:\n"
#     for key, data in side_data.items():
#         time = data["time"]
#         dist = data["dist"]
#         output += f"{key}: {time} min, {dist} km\n"
#     output += "\n"

# print(output)

# quit()
