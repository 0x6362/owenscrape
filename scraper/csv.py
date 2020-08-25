from owenscrape import codes
import itertools

def parse_codes_from_file(path):
    items = []
    with open(path, 'r') as s:
        for line in s:
            try:
                item = codes.NewCode(line)
                items.append(item)
            except codes.ParseCodeFailedException as e:
                print(e.raw_code, e.component) 
    return items

succeeded = parse_codes_from_file('succeeded.txt')
failed  = parse_codes_from_file('failed.txt')


# {k: len(list(v)) for k,v in itertools.groupby(sorted(s, key = lambda x: x.line), lambda x: x.line)}

def to_csv(columns):
    return ','.join([*map(lambda s: "'%s'" % s, columns)]) + '\n'

def item_to_csv(item):
    return to_csv([ item.raw_code, item.line, item.gender, item.collection.season,
        item.collection.year, item.item_code, item.fabric_code,
        item.colour_code])

with open('items.csv', 'w') as f:
    headers = ('raw_code', 'item_line', 'item_gender', 'item_season', 'item_year', 'item_code', 'item_fabric', 'item_colour')
    f.write(to_csv(headers))
    for item in (succeeded + failed):
        f.write(item_to_csv(item))
