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

create_transfer("1", "0xd1c31e2c6c5558c306c9c71d51e1faffd80ef517", "0b28bb7d-7584-5585-ad56-12a3c814d427")