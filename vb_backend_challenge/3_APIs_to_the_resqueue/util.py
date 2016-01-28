import requests

## 3: APIs to the rescue asks for 'a function'... which makes me think of something simple like:

PAYMENT_HISTORY_API = [
    {
        'url': 'https://api1.example.com/v1/payments',
        'remote_payment_id': 'id',
        'total': 'amount',
        'last_4': 'last_4',
        'details': 'memo'
    },
    {
        'url': 'https://api1.example.com/v6/order/history',
        'remote_payment_id': 'orderID',
        'total': 'total',
        'last_4': 'last_4',
        'details': 'description'
    }
]
        
def get_payment_history():
    history = []
    for api_spec in PAYMENT_HISTORY_API:
        history.extend(
            map(lambda result: 
                {
                    'remote_payment_id': result[api_spec['remote_payment_id']],
                    'total': result[api_spec['total']],
                    'last_4': result[api_spec['last_4']],
                    'details': result[api_spec['details']]
                },
               requests.get(api_spec['url']).json()
            )
        )
    return history