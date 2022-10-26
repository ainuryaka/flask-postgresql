from flask import Flask, request
import requests
import psycopg2

app = Flask(__name__)


@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        address = request.form.get('address')
        url = 'https://solana-gateway.moralis.io/nft/mainnet/' + address + '/metadata'
        headers = {
            "accept": "application/json",
            "X-API-Key": "iWXzBLaUXSfgBOJ5y8lmb9h5xAstww6nm2wkDTXOxsL1vLeoANc8njHGpnTrQWcM"
        }
        response = requests.get(url, headers=headers)
        print(response.text)

        # establishing the connection
        conn = psycopg2.connect(
            database="nft", user='postgres', password='sunset', host='localhost', port='5433'
        )

        cursor = conn.cursor()


        create_script = ''' CREATE TABLE IF NOT EXISTS NFT
(
  address character varying(1000)
    name character varying(200))'''

        cursor.execute(create_script)

        insert_script = "INSERT INTO NFT (name, address) VALUES (%s, %s)"
        insert_value = ("NFT name", response.text)

        cursor.execute(insert_script, insert_value)

        conn.commit()

        conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)



