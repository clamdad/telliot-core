from telliot_core.apps.staker import Staker
from telliot_core.apps.staker import StakerList


def test_get():
    stakers = StakerList()

    mainnet_stakers = stakers.get(chain_id=1)
    assert len(mainnet_stakers) == 1
    assert isinstance(mainnet_stakers[0], Staker)

    tag_search = stakers.get(tag="my_mainnet_staker")
    assert len(tag_search) == 1
    assert isinstance(tag_search[0], Staker)

    address_search = stakers.get(address="0x00001234")
    assert len(address_search) == 1
    assert isinstance(address_search[0], Staker)

    key_search = stakers.get(private_key="0x0000xxxx")
    assert len(key_search) == 2
    assert isinstance(key_search[0], Staker)
    assert isinstance(key_search[1], Staker)

    failed_search = stakers.get(tag="bad_tag")
    assert len(failed_search) == 0
