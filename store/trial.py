sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl']
SIZE_CHOICES = list()
for size in sizes:
    SIZE_CHOICES.insert(sizes.index(size), (f'{size.lower()}', f'{size.upper()}'))
SIZE_CHOICES = tuple(SIZE_CHOICES)
print(SIZE_CHOICES)