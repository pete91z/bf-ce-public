# Use Python 3.9
# Call from Redshift Lambda UDF
# Create new layer with requests module
import json
import requests

def lambda_handler(event, context):
    # TODO implement
    args=event['arguments']
    print(args)
    ret = dict()
    res = []
    def fetch_price(inarr):
        url = f"https://api.coinbase.com/v2/prices/{inarr[0]}-{inarr[1]}/buy"
        tr=requests.get(url).json()
        try:
            res1 = float(tr['data']['amount'])
        except:
            res1 = 0
        return res1
        
    try:
        res = list(map(fetch_price, args))
        print(res)
        ret['results'] = res
        ret['success'] = True
    except:
        ret['error_msg'] = 'pair not valid'
        ret['success'] = False
        
    return json.dumps(ret)
