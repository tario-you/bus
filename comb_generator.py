from itertools import combinations
import json

with open('combs_input.txt', 'r') as f:
    x = f.read()

elements = x.split('\n')

# Generate all combinations of bag 1 elements (4 to 7 elements)
combinations_bag1 = []
for r in range(4, 8):
    combinations_bag1.extend(combinations(elements, r))

# Generate all combinations of bag 2 elements (11 - number of elements in bag 1)
combinations_bag2 = []
for bag1_combination in combinations_bag1:
    bag2_combination = tuple(e for e in elements if e not in bag1_combination)
    combinations_bag2.append(bag2_combination)

print(len(combinations_bag2))

all_combs = []

with open('combs_output.txt', 'w') as f:
    for i, (bag1, bag2) in enumerate(zip(combinations_bag1, combinations_bag2), start=1):
        if i == len(combinations_bag2)/2:
            break
        all_combs.append([bag1, bag2])
        f.write(f"Combination {i} - Bag 1: {bag1}, Bag 2: {bag2}\n")

with open('combs_output_ascii.json', 'w') as f:
    f.write(json.dumps(all_combs, indent=4, ensure_ascii=False))

with open('combs_output.json', 'w') as f:
    f.write(json.dumps(all_combs, indent=4))
