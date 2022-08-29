from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

# We use deploy_fund_me from deploy.py by adding return fund_me at the end of the function
# This way we get the instance of the deployed contract passed to this script


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # If launching without the pytest.raises... Line, the cmd line gives this error:
    # brownie.exceptions.VirtualMachineError: revert
    # Because contract will revert transaction, as it doesn't meet the requirements
    # Since we want this to happen, we use the with statement
    # Telling python, that we want the test to be passed if the VirtualMachineError
    # exception is raised by brownie ie, the one calling the withdraw function is not the owner
    # we need exceptions package and pytest imported
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
