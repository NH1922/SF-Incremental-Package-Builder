def parse_meta():
    keys = []
    values = []
    metadata = {}

    with open(r'C:\Users\nitish_yadav\Desktop\SF-Incremental-Package-Builder\meta.txt') as fp:
        for line in fp:
            if 'XMLName' in line:
                values.append(line.split(':')[1].strip())
            if 'DirName' in line:
                keys.append(line.split(':')[1].strip())

    for i in range(len(keys)):
        metadata[keys[i]] = values[i]
    return metadata

