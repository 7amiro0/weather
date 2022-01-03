"""Func class."""

import table

def create_con():
    """Create connection and cursor."""
    con = table.sqlite3.connect('exempl.db')
    cursor = con.cursor()
    return con, cursor

def city_name():
    """Get list name city from date base."""
    list_city_db = ()
    connection, cursor = create_con()

    for name in cursor.execute('''
SELECT 
    name_city
FROM
    weather
'''):
        list_city_db += name
    connection.close()
    return tuple(set(list_city_db))

def midle(data, args):
    """Calculate the arithmetic mean."""
    result = 0
    for city in data:
        result += int(city[args["value_type"]])
    result = int(result / 7)
    return result

def params(args):
    """Get value city in date base."""
    connection, cursor = create_con()
    sql = '''
SELECT 
    *
FROM 
    weather
WHERE 
    name_city = ?
'''
    try:
        cursor.execute(sql, [args['city']])
        data = parse_columns(cursor.fetchall())
        data = 'Invalid request'
        connection.close()
        args['value_type'] = midle(data, args)
    except:
        args['value_type'] = 'Invalid request'
    return args

def date(data, args):
    """Obsess data in a period of days."""
    point_dt = False
    pariud_dt = []

    for info_db in data:
        if args['start_dt'] == args['end_dt'] or\
           info_db['date'] == args['end_dt']:
            pariud_dt.append(info_db)
            break
        if info_db['date'] == args['start_dt']:
            point_dt = True
        if info_db['date'] != args['end_dt'] and point_dt:
            pariud_dt.append(info_db)
    return pariud_dt

def record(args):
    """Get value city on any days from date base."""
    connection, cursor = create_con()
    sql = '''
SELECT 
    *
FROM 
    weather
WHERE 
    name_city = ?
'''
    try:
        cursor.execute(sql, [args['city']])
        data = parse_columns(cursor.fetchall())
        connection.close()
        result = date(data, args)
    except:
        result = 'Invalid request'
    return result

def moving_average(args):
    """Get value city midle value from date base."""
    connection, cursor = create_con()
    sql = '''
SELECT 
    *
FROM 
    weather
WHERE 
    name_city = ?
'''
    try:
        cursor.execute(sql, [args['city']])
        data = parse_columns(cursor.fetchall())
        connection.close()
        result = midle(data, args)
    except:
        result = 'Invalid request'
    return midle(data, args)

def parse_columns(data):
    """Create dict."""
    result = []

    for rows in data:
        tmp = {}
        tmp["date"] = rows[0]
        tmp["temp"] = rows[1]
        tmp["pcp"] = rows[2]
        tmp["clounds"] = rows[3]
        tmp["pressure"] = rows[4]
        tmp["humidity"] = rows[5]
        tmp["wind_speed"] = rows[6]
        tmp["name_cite"] = rows[7]
        result.append(tmp)
    return result
