import zipfile
import codecs

with zipfile.ZipFile('./zipcode/ken_all.zip') as z:
    z.extractall('./zipcode/')

def strip_dq(data):
    if data[0] == '"' and data[-1] == '"':
        return data[1:-1]
    return data

with open('./zipcode/KEN_ALL.CSV', 'r') as f:
    zips = [d.strip().split(',') for d in f.readlines()]
    zips = [(strip_dq(p[2]), strip_dq(p[6]), strip_dq(p[7]), strip_dq(p[8])) for p in zips]

# zips[0]: zip_code
# zips[1]: 都道府県
# zips[2]: 市
# zips[3]: 区・町

latlng_zfiles = ['./latlng/{:02}000-17.0a.zip'.format(i) for i in range(1, 48)]
latlng_files = ['./latlng/{0:02}000-17.0a/{0:02}_2018.csv'.format(i) for i in range(1, 48)]

for zf in latlng_zfiles:
    with zipfile.ZipFile(zf) as z:
        z.extractall('./latlng/')

latlngs = {}
for path in latlng_files:
    print(path)
    with open(path, 'r') as f:
        lllist = [d.strip().split(',') for d in f.readlines()[1:]]
        lllist = [(strip_dq(d[0]), strip_dq(d[1]), float(strip_dq(d[8])), float(strip_dq(d[9]))) for d in lllist if len(d) > 9]
        for l in lllist:
            latlngs[l[0]+l[1]] = (l[2], l[3])

# latlngs: 都道府県・市 -> (lat, lng)

zip2latlng = {}
notfound = {}
for p in zips:
    zip = p[0]
    city = p[1] + p[2]
    if city in latlngs:
        zip2latlng[zip] = (city, latlngs[city])
    else:
        if not city in notfound:
            notfound[city] = []
        notfound[city].append(zip)

with codecs.open('zip2latlng.csv', 'w', 'utf-8') as f:
    f.write('zip\tcity\tlat\tlng\n')
    for zip in zip2latlng:
        f.write('{}\t{}\t{}\t{}\n'.format(zip, zip2latlng[zip][0], zip2latlng[zip][1][0], zip2latlng[zip][1][1]))

with codecs.open('zip_notfound.csv', 'w', 'utf-8') as f:
    f.write('zip\tcity\n')
    for p in zips:
        zip = p[0]
        city = p[1] + p[2]
        f.write('{}\t{}\n'.format(zip, city))

