from brownie import network
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # deploy contract
    # create NFT
    # get a random breed back

    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(200)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
