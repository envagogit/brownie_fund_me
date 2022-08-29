from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # Pass price feed address to the FundMe contract depending on wether
    # we're on local(Ganache) or online (rinkeby)
    # -> deploy mock vs use the rinkeby priceFeed address
    print(f"The active network is {network.show_active()}")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # network.show_active() returns rinkeby or development depending of what we run
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        # Use last aggregator contract deployed:
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # .get("verify") makews life easier if we forget
    # to add verify: True in config (we could use ["verify"] too)
    # Basically we set an if statement in config, if network is rinkeby
    #  it will show verify = True if it's development it will show False
    print(f"Contract Deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
