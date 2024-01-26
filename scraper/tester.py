myDict = {
    'name': 'bobby',
    'age': 26,
    'height': {
        'value': 6.4,
        'unit': 'feet'
    },
    'paidSubscriber': True
}
partial_key = 'subscriber'
complete_key = next((key for key in myDict if partial_key in key), -1)
print(complete_key)