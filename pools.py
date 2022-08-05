from substrateinterface import SubstrateInterface

custom_type_registry = {
    "runtime_id": 1,
    "types": {
        "Address": "AccountId",
        "LookupSource": "AccountId",
        "Price": "u128",
        "AssetId": "u32",
        "Currency": "AssetId",
        "CurrencyId": "AssetId",
        "MultiLocation": "MultiLocationV1",
        "AssetNativeLocation": "MultiLocation",
        "AssetType": {"type": "enum", "value_list": ["Token", "ShareToken"]},
        "IntentionType": {"type": "enum", "value_list": ["SELL", "BUY"]},
        "IntentionId": "Hash",
    },
    "versioning": [],
}


def client(node):
    return SubstrateInterface(
        url=node,
        ss58_format=63,
        type_registry_preset="kusama",
        type_registry=custom_type_registry,
    )

def load_assets(client):
    assets = client.query_map("AssetRegistry", "AssetMetadataMap")

    r = {0: "BSX"}

    for asset in assets:
        asset_id = asset[0].decode()
        metadata = asset[1].decode()
        r[asset_id] = metadata["symbol"]

    print(r)
    return r


def get_balance(client, address, currency):
    if currency == 0:
        return client.query('System', 'Account', params=[address]).value["data"]["free"]
    else:
        return client.query('Tokens', 'Accounts', params=[address, currency]).value["free"]


if __name__ == "__main__":
    client = client("wss://rpc.basilisk.cloud")
    pools = client.query_map("XYK", "ShareToken")

    bsx_assets = load_assets(client)

    for pool in pools:
        pool_address = pool[0]
        share_token = pool[1]
        assets = client.query("XYK", "PoolAssets", params=[pool_address])
        a1 = assets[0].decode()
        a2 = assets[1].decode()
        asset_1_balance = get_balance(client, pool_address, a1)
        asset_2_balance = get_balance(client, pool_address, a2)

        a1_symbol = bsx_assets[a1]
        a2_symbol = bsx_assets[a2]

        print(f"Pool assets: ({a1_symbol, a2_symbol}) Share token: {share_token} Address: {pool_address}")
        print("")

        print(f"Asset {a1_symbol} balance: {asset_1_balance}")
        print(f"Asset {a2_symbol} balance: {asset_2_balance}")

        print("-------------------------------------------------------------------------")
    client.close()
