from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_breed
import json


def main():
    print(f"Working on {network.show_active()}")
    # Get the latest collectible
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()

    # Iterate through collectibles
    for token_id in range(number_of_collectibles):
        # Get the breed with the tokenIdToBreed mapping
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        # If the tokenURI has not been assigned
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            f = open(f"./metadata/{network.show_active()}/IPFS.json")
            metadata_urls = json.load(f)
            set_tokenURI(token_id, advanced_collectible, metadata_urls[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenUri(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)} "
    )
    print("Wait a couple of minutes and hit refresh")
