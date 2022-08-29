from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3
import os

FORKED_LOCAL_ENVIROMNENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8  # How many zeroes from Starting Price are just decimals
STARTING_PRICE = 200000000000  # Starting Price without decimals


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMNENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("Deploying Mocks...")
    # Remember that MockV3Aggregator is a list of all aggregator contracts deployed,
    # so if len is <1 means we havn't deployed, else we already have
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    # toWei is just adding 18 decimals to 2000
    print("Mocks Deployed")


def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("freecodecamp") #
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])
    # ^this way we have 1 source of truth to store keys and pull from all scripts (config + .env)
    simple_storage = SimpleStorage.deploy({"from": account})
    # ^saves address of contract

    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)  # How many blocks we want to wait
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)
    print(simple_storage)
