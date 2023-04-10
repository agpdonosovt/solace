from weather import Weather

weather = Weather()

Paris = weather.name_query('Paris')

if Paris[1] != 200:
    print('Valid name query failed.')
    exit(-1)
else:
    print(Paris[0])

No_name = weather.name_query('')

if No_name[1] != 400:
    print('Empty name query failed.')
    exit(-1)

Mingus1 = weather.name_query('Mingus1')

if Mingus1[1] != 404:
    print('Invalid name query failed')
    exit(-1)
else:
    print(Mingus1[0])

latitude = '48.853'
longitude = '2.348'

valid_lat_long = weather.coordinate_query(latitude, longitude)

if valid_lat_long[1] != 200:
    print('Valid coord query failed.')
    exit(-1)
else:
    print(valid_lat_long[0])

no_lat_long = weather.coordinate_query('', '')

if no_lat_long[1] != 400:
    print('Empty coord query failed.')
    exit

latitude = 'a'
longitude = '2.348'

invalid_lat = weather.coordinate_query(latitude, longitude)

if invalid_lat[1] != 400:
    print('Invalid latitude query failed')
    exit(-1)
else:
    print(invalid_lat[0])

latitude = '48.853'
longitude = 'b'

invalid_long = weather.coordinate_query(latitude, longitude)

if invalid_long[1] != 400:
    print('Invalid longitude query failed')
    exit(-1)
else:
    print(invalid_long[0])

latitude = ''
longitude = '2.349'

no_lat = weather.coordinate_query(latitude, longitude)

if no_lat[1] != 400:
    print('Missing latitude query failed')
    exit(-1)
else:
    print(no_lat[0])

latitude = '48.853'
longitude = ''

no_long = weather.coordinate_query(latitude, longitude)

if no_long[1] != 400:
    print('Missing longitude query failed')
    exit(-1)
else:
    print(no_long[0])

