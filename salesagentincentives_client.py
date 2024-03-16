from dotenv import load_dotenv

load_dotenv()

from web3 import Web3
from web3.middleware import geth_poa_middleware

import os

#alchemy_key = os.environ['ALCHEMY_API_KEY']
alchemy_key = os.environ['ALCHEMY_API_KEY_ARB']

w3 = Web3(Web3.HTTPProvider(f'https://base-sepolia.g.alchemy.com/v2/{alchemy_key}'))
#w3 = Web3(Web3.HTTPProvider(f'https://arb-sepolia.g.alchemy.com/v2/{alchemy_key}'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

assert w3.is_connected()

print(w3.eth.block_number)

contract_abi = """[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "jobId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "bonus",
				"type": "uint256"
			}
		],
		"name": "BonusReleased",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "jobId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "score",
				"type": "uint256"
			}
		],
		"name": "JobCompleted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "jobId",
				"type": "uint256"
			}
		],
		"name": "JobCreated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "jobId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "PaymentReleased",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_jobId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_performanceScore",
				"type": "uint256"
			}
		],
		"name": "completeJob",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_salesAgent",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_paymentAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_bonusAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_bonusThreshold",
				"type": "uint256"
			}
		],
		"name": "createJob",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_jobId",
				"type": "uint256"
			}
		],
		"name": "fundJob",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getContractBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "jobCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "jobs",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "salesAgent",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "paymentAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bonusAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bonusThreshold",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "performanceScore",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "jobCompleted",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "paymentReleased",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_jobId",
				"type": "uint256"
			}
		],
		"name": "releasePayment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]"""

contract = w3.eth.contract(abi=contract_abi, address="0xD24315294aFC0d5eBe11F4702637682176E6540F")
#contract = w3.eth.contract(abi=contract_abi, address="0xDAA3624F4aD873292dc2349B4EF0BA66F62c0f4d")

owner_account = w3.eth.account.from_key(os.environ['MY_PRIVATE_KEY'])

payment_amount = w3.to_wei(0.00000001, 'ether')  # Example payment amount
bonus_amount = w3.to_wei(0.00000004, 'ether')  # Example bonus amount
bonus_threshold = 70  # Example bonus threshold

def create_job() -> int:
   

    create_job_tx = contract.functions.createJob(
        "0xAA64A7Db2C3951375dCDF8DB76ADb46C258840E7", payment_amount, bonus_amount, bonus_threshold
    ).build_transaction({
        'from': owner_account.address,
        'nonce': w3.eth.get_transaction_count(owner_account.address),
        'gas': 200000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })

    # Sign the transaction
    signed_tx = owner_account.sign_transaction(create_job_tx)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(tx_receipt)

    job_created_events = contract.events.JobCreated().process_receipt(tx_receipt)
    job_id = job_created_events[0]['args']['jobId'] if job_created_events else None

    if job_id is not None:
        print(f"Job created successfully with Job ID: {job_id}")
    else:
        print("Job creation failed or JobCreated event not found.")
    return job_id



def complete_job(job_id, performance_score) -> dict:
    complete_job_tx = contract.functions.completeJob(
        job_id, performance_score
    ).build_transaction({
        'from': owner_account.address,
        'nonce': w3.eth.get_transaction_count(owner_account.address),
        'gas': 200000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })


    # Sign the transaction
    signed_tx = owner_account.sign_transaction(complete_job_tx)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print (f"Job {job_id} completed successfully, transaction hash: {tx_hash.hex()}")

    return tx_receipt

def release_payment(job_id) -> dict:
    release_payment_tx = contract.functions.releasePayment(
        job_id
    ).build_transaction({
        'from': owner_account.address,
        'nonce': w3.eth.get_transaction_count(owner_account.address),
        'gas': 200000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })

    signed_tx = owner_account.sign_transaction(release_payment_tx)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Payment for job {job_id} released successfully, transaction hash: {tx_hash.hex()}")
    return tx_receipt

def fund_job(job_id) -> dict:
    fund_job_tx = contract.functions.fundJob(
        job_id
    ).build_transaction({
        'from': owner_account.address,
        'nonce': w3.eth.get_transaction_count(owner_account.address),
        'value': payment_amount + bonus_amount,  # This is where you specify the Ether amount to send
        'gas': 200000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })

    # Sign the transaction
    signed_tx = owner_account.sign_transaction(fund_job_tx)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Job {job_id} funded successfully, transaction hash: {tx_hash.hex()}")

    return tx_receipt

# job_id = create_job()

# fund_job(job_id)

# complete_job(job_id, 90)

# release_payment(job_id)

