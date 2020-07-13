import re
import sys
import json

lines = sys.stdin.readlines()

ITEMS = []
count = 0
current_item = []
for line in lines:
    if line.strip() == "":
        continue
    if line.startswith('APPROVED') and current_item != []:
        ITEMS.append("".join(current_item))
        current_item = []
        continue
    current_item.append(line)

PATTERNS = [('location', '^Location: (.*?)'),
            ('department', '^Administering Department: (.*?)'),
            ('source', '^Funding Source: (.*?)'),
            ('amount', '^Amount: (.*?)'),
            ('hires', '^Projected Section 3 Hires: (.*?)$'),
        #    ('awardee', '\n.*?responsible bidder, (.*? (?:Corporation|Corp\.|LLC|Inc|L\.L\.C))')
         ]
FIELDS = [k[0] for k in PATTERNS]
REGEX = "".join([k[1] for k in PATTERNS])

JSON_DATA = []
ERRORS_1 = []
ERRORS_2 = []


for item in ITEMS:
    match = re.search(REGEX, item, re.MULTILINE|re.DOTALL)
    if match is None:
        ERRORS_1.append(item)
        continue
    data = {}
    for index, field in enumerate(FIELDS):
        data[field] = match.group(index+1).strip().replace('\n', ' ')

    # We try to extract the awardee.
    
    match = re.search(".*?(?:[aA]warded to|award of this agreement to|greement with|bidder,) (.*? (?:Company|Co|Corporation|Corp|P\.C\.|LLC|LLP|Inc|L\.L\.C))", item.replace('\n', ' '), re.MULTILINE|re.DOTALL)
    if match:
        data['awardee'] = match.group(1)
    if 'awardee' not in data:
        ERRORS_2.append(item)
        continue
    JSON_DATA.append(data)

print("SUCCESS: %d." % len(JSON_DATA))
print("ERRORS for structured data: %d." % len(ERRORS_1))
print("ERRORS for un_structured data: %d." % len(ERRORS_2))

print('=' * 20)
print('TO REVIEW')
print('=' * 20)

print('Items to review')
for item in ERRORS_1+ERRORS_2:
    print('[[', item, ']]')

print('=' * 20)
print('Extracted data')
print(json.dumps(JSON_DATA, sort_keys=True, indent=2))