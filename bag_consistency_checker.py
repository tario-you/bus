import json
from bag_analysis import addtimes

with open('automated_bag_bag420.json', 'r') as f:
    data1 = json.load(f)['dis2school']

with open('automated_bag_oct5.json', 'r') as f:
    data2 = json.load(f)['dis2school']

consistent = []

# for k in data1:
#     for l in range(len(data1[k])):
#         if len(data1[k]) == len(data2[k]):
#             x = addtimes(data1[k][l])
#             y = addtimes(data2[k][l])
#             if abs(x-y) < 5 and x != 0:
#                 consistent.append((x+y)/2)

for k in data1:
    if len(data1[k]) == 2 and len(data2[k]) == 2:
        x = addtimes(data1[k])
        y = addtimes(data2[k])
        if abs(x-y) < 5:
            # consistent.append((x+y)/2)
            consistent.append(k)

print(consistent)

print(f'{len(consistent)=}')
# consistent.sort()
# print(consistent[:10])
