import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

my_address = '7TMV2KDJ7BT5FHOILFTFQY73KNAITPZ2GDYJMVMIZST6QY7DKE4OAKC4BY'
my_private_key = 'K0qcVcDUP381sGoLoUQPhcRVTSX/tXmAI7IKJdUQ+Cr82V0oafhn0p3IWWZYY/tTQIm/OjDwllWIzKfoY+NROA=='
my_pass = 'earth illness client equal leisure garlic like height cannon barely marble embark process fashion weird remove august mix flip expose prevent aerobic fit ability adjust'

client_address = 'WEPA7RMQSPZ6Z2VMUQFCCQKOAZ24KFAKYZRI4SUXWYMX7YZZUXFKOMHIPQ'
client_private_key = '/scAMyCPahlaVaNF1IaoyUEOv8LvJQz+Pq+XqYclAE2xHg/FkJPz7OqspAohQU4GdcUUCsZijkqXthl/4zmlyg=='

def transaction(my_address, my_private_key, client_address):
    # Initialize an algod client
    algod_address = "http://localhost:4001"
    algod_token = "7TMV2KDJ7BT5FHOILFTFQY73KNAITPZ2GDYJMVMIZST6QY7DKE4OAKC4BY"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Get the relevant params from the algod
    params = algod_client.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]

    # Create the transaction
    note = "Hello World".encode()
    txn = transaction.PaymentTxn(my_address, params, client_address, 1000000, note=note)

    # Sign the transaction
    stxn = txn.sign(my_private_key)

    # Send the transaction to the network
    txid = algod_client.send_transaction(stxn)
    print("Successfully sent tx with ID: {}".format(txid))

    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client, txid)

    # Get the transaction information
    pending_txn = algod_client.pending_transaction_info(txid)
    print("Pending transaction information: {}".format(json.dumps(pending_txn, indent=4)))

    # Get the confirmed transaction
    confirmed_txn = algod_client.pending_transaction_info(txid)
    print("Confirmed transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))