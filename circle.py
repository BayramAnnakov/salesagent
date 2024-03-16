import dotenv

dotenv.load_dotenv()

import requests
import os 

from entity_secret import generate_entity_secret
import uuid



url = "https://api.circle.com/v1/w3s/developer/transactions/transfer"


def create_transfer(amount: str, destination_address: str, wallet_id: str) -> None:

    entitySecretCipherText = generate_entity_secret()

    #generate new uuid for idempotency key
    idempotencyKey = uuid.uuid4()

    print(idempotencyKey)

    payload = {
        "idempotencyKey": str(idempotencyKey),
        "entitySecretCipherText": entitySecretCipherText,
        "amounts": [amount],
        "destinationAddress": destination_address,
        "feeLevel": "HIGH",
        "tokenId": "7adb2b7d-c9cd-5164-b2d4-b73b088274dc",
        "walletId": wallet_id
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+os.environ['CIRCLE_API_KEY']
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return response.json().get('data').get('id')

def create_wallet(wallet_set_id: str) -> str:
    import requests

    url = "https://api.circle.com/v1/w3s/developer/wallets"

    entitySecretCipherText = generate_entity_secret()

    #generate new uuid for idempotency key
    idempotencyKey = uuid.uuid4()

    payload = {
        "idempotencyKey": str(idempotencyKey),
        "entitySecretCipherText": entitySecretCipherText,
        "blockchains": ["MATIC-MUMBAI"],
        "count": 1,
        "walletSetId": wallet_set_id
    }
    headers = {
        "Content-Type": "application/json",
         "Authorization": "Bearer "+os.environ['CIRCLE_API_KEY']
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return None

#create_wallet("018e479c-7fa5-748b-af39-5f459c2136a2")