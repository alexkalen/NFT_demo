from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    # We get the earliest deployed contract
    advanced_collectible = AdvancedCollectible[-1]
    # We get the number of available NFTS
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")

    # For every NFT created we give it a metadata file name
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        # If metadata file does not exists (else), we create the metadata file from
        # the existing template.
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} path already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pawpy!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            # Uploads the image to IPFS and get the IPFS path for it.
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri

            # Opens the metadata file and dumps all the information
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)

            # Uploads the metadata to IPFS and gets the metadata URL
            metadata_url = upload_to_ipfs(metadata_file_name)

            # We dump the metadata URL in IPFS.json file
            IPFS_json = f"./metadata/{network.show_active()}/IPFS.json"
            new_metadata_url = {breed: metadata_url}

            if Path(IPFS_json).exists():
                with open(IPFS_json, "r") as file:
                    data = json.load(file)
                # 2. Update json object
                data[breed] = metadata_url

                with open(IPFS_json, "w") as file:
                    json.dump(data, file)
            else:
                with open(IPFS_json, "w") as file:
                    json.dump(new_metadata_url, file)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        response = requests.post(ipfs_url + end_point, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
