import json
from collections import Counter

data = json.load(open('gap_diagnosis.json'))
kustomer_losses = data['Kustomer']

categories = Counter(loss['category'] for loss in kustomer_losses)
print(categories)

# also see who Kustomer loses to most often
competitors = Counter()
for loss in kustomer_losses:
    for comp in loss['lost_to']:
        competitors[comp['brand']] += 1
print(competitors)