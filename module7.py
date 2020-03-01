from datetime import datetime, timedelta
import locale


def register(data):
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        print("{0}\t{1}".format(item, cost))
        # Or, with slightly more readability in the output:
        locale.setlocale(locale.LC_ALL, locale='en_US')
        print(f'\nItem: {item}\nCost: {locale.currency(cost, grouping=True)}')


data = [datetime.now().date(), datetime.now().time(), 'Mellanox', 'MSB7780-ES2R', 29520.00, 'Debit']
register(data)

print()


def delta_tester(dt):
    td = timedelta(seconds=-60, days=730)
    return dt + td


print(delta_tester(datetime.now()).strftime('%A, %B %d %Y at %I:%M:%S %p'))
print()

td = timedelta(minutes=13, hours=10, days=100)
print(td)


def get_types(feet, inches):
    print(f'feet: {type(feet)}, inches: {type(inches)}')
    if isinstance(feet, (int, float)) and isinstance(inches, (int, float)):
        easter_egg(feet, inches)


def easter_egg(feet, inches):
    distance = feet + (inches // 12)
    speed = (distance // 3281) // (td.total_seconds() // 3600)
    print(f'{int(speed)} km/h')


get_types(10572890220, 12)
