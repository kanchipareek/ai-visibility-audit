import json
from collections import Counter

data = json.load(open('analyzed_perplexity.json'))
print('Total entries:', len(data))

prompts_counts = Counter(d['prompt'] for d in data)
print(prompts_counts.most_common(5))