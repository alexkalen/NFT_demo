from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]

    fund_with_link(advanced_collectible.address)
    creation_tx = advanced_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Collectible created!")
