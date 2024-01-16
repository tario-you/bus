import json
from automation_bag import bag_loop


'''lengths = {}

for k, v in data.items():
    x = str(len(v))
    if x not in lengths:
        lengths[x] = 1
    else:
        lengths[x] += 1

print(lengths)'''


def addtimes(x):
    sumtime = 0
    if type(x[0]) == type([1, 2, 3]):
        everything = [element for row in x for element in row]
    else:
        everything = x
    print(everything)

    for item in everything:
        if "分钟" in item:
            sumtime += float(item[:-2])
        if "小时" in item:
            sumtime += float(item[:-2]) * 60

    return sumtime


if __name__ == "__main__":
    with open('automated_bag_missed.json', 'r') as f:
        data = json.load(f)['dis2school']

    x = []
    yay = 0
    for i, (k, v) in enumerate(data.items()):
        if len(v) == 2:
            yay += 1
            x.append((k, addtimes(v)))

    x.sort(key=lambda a: a[1])

    x.reverse()

    for y in x:
        print(y, end='\t')
        print(data[y[0]][0][0], end=' | ')
        print(data[y[0]][1][0])

    with open('combs_output_ascii.json', 'r') as f:
        data = json.load(f)

    print(data[83])

    to_insert = [1]

    new_data = []

    for adslfjad in to_insert:
        new_data.append(data[adslfjad])

    print(yay)

    bag_loop(new_data, doReload=True, record_data=True, screenshots=True)

    '''
    Current routes:
    {
        "dis2school": {
            "bag0": [
                ["51.0分钟", "28.9公里", "47.0个红绿灯"],
                ["55.0分钟", "32.3公里", "25.0个红绿灯"]
            ]
        }
    }
    '''

    # 104 minutes = goal
