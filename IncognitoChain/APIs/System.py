from IncognitoChain.Drivers.Connections import RpcConnection


class SystemRpc:
    def __init__(self, url):
        self.rpc_connection = RpcConnection(url=url)
        self._cache = {}

    def retrieve_block_by_height(self, block_height, shard_id):
        """

        :param block_height:
        :param shard_id: shard id to retrieve data from
        :return:
        """
        level = '1'
        return self.rpc_connection.with_method('retrieveblockbyheight').with_params(
            [block_height, shard_id, level]).execute()

    def get_mem_pool(self):
        return self.rpc_connection.with_method("getmempoolinfo").execute()

    def get_beacon_best_state_detail(self, refresh_cache=True):
        if refresh_cache:
            beacon_best_state_detail = self.rpc_connection.with_method('getbeaconbeststatedetail').with_params(
                []).execute()
            self._cache['getbeaconbeststatedetail'] = beacon_best_state_detail
        else:
            try:
                beacon_best_state_detail = self._cache['getbeaconbeststatedetail']
            except KeyError:
                beacon_best_state_detail = self.rpc_connection.with_method('getbeaconbeststatedetail').with_params(
                    []).execute()
        return beacon_best_state_detail

    def get_beacon_best_state(self):
        return self.rpc_connection. \
            with_method("getbeaconbeststate"). \
            with_params([]). \
            execute()

    def remove_tx_in_mem_pool(self, tx_id):
        return self.rpc_connection.with_method('removetxinmempool').with_params([tx_id]).execute()

    def get_block_chain_info(self):
        return self.rpc_connection.with_method('getblockchaininfo').with_params([]).execute()
