import json
import random
import ssl
import requests
from flask import Flask, request
import os

def edit_order(order_number, item_no):
    # Connect to the Shopify store
    token = os.environ.get('SHOPIFY_TOKEN')
    store_url = os.environ.get('SHOPIFY_URL')
    product_list = ['CALCITE', 'CARNELIAN', 'AGATE', 'FLUORITE', 'JASPER', 'SODALITE', 'YOOPERLITE', 'AVENTURINE', 'PORKSTONE', 'OPAL', 'LEPIDOLITE', 'AMETHYST', 'MOONSTONE', 'QUARTZ']
    endpoint = f"https://{store_url}/admin/api/2023-01/orders/{order_number}.json"

    # Find the order by its order number
    get_response = requests.get(endpoint, headers={"X-Shopify-Access-Token": token})
    pick_no = 4 * int(item_no)
    note = json.loads(get_response.content)['order']['note']
    if note is None:
        note = 'Thanks for order!'
    if pick_no > 14:
        selected_items = product_list
    else:
        selected_items = random.sample(product_list, pick_no)
    data = {
        'order': {
            "id": order_number,
            'note': note + '\n' + '=================' + '\n' + 'Let your constellation sign guide you, SoulNewMe Al have found [ ' +' '.join(selected_items) + ' ] is a prefect fit you!' 
             
        }
    }  
    put_response = requests.put(endpoint, json=data, headers={"X-Shopify-Access-Token": token})
    return put_response.status_code


app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_post():
    data = request.get_data(as_text=True)
    print(data)
    order_number = json.loads(data)['id']
    item_no = json.loads(data)['item_no']

    edit_order(order_number, item_no)
    return 'success'

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/app/server.crt', '/app/private.key')
    app.run(host='0.0.0.0', port=8888, ssl_context=context)




