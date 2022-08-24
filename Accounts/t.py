list1 = {
    'a': 'a',
    'b': 'b',
    'c': 'c',
}
list2 = {
    'a': 1,
    'b': 2,
    'c': 'c',
}

for i in list1:
    for i1 in list2:
        if i == i1:
            print(True)
        else:
            print(False)