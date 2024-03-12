test = "Spring 105, 1805"

season = test.split(' ', 1)[0]
test = test.split(' ', 1)[1]
day = test.split(',', 1)[0]
year = test.split(',', 1)[1]

seasons = ('Spring', 'Summer', 'Fall', 'Autumn', 'Winter')
if season.casefold() in (s.casefold() for s in seasons):
    print('yes')
el