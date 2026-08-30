import json
from collections import Counter

data = json.load(open('combined_results.json'))
print('Total rows:', len(data))
print(Counter(r['model'] for r in data))
print(Counter(r['brand'] for r in data if r['brand']))