from IncognitoChain.Drivers.Connections import WebSocket


class SubscriptionWs:
    def __init__(self, web_socket: WebSocket):
        self.ws_conn = web_socket

    def subscribe_new_shard_block(self):
        return self.ws_conn.with_method("subcribenewshardblock").with_params([0]).execute()

    def subscribe_pending_transaction(self, tx_id):
        return self.ws_conn.with_method("subcribependingtransaction").with_params([tx_id]).execute()

    def subscribe_cross_output_coin_by_private_key(self, private_key):
        return self.ws_conn.with_method("subcribecrossoutputcoinbyprivatekey").with_params([private_key]).execute()

    def subscribe_cross_custom_token_privacy_by_private_key(self, private_key):
        return self.ws_conn.with_method("subcribecrosscustomtokenprivacybyprivatekey"). \
            with_params([private_key]).execute()

    def close_web_socket(self):
        self.ws_conn.close()

    def open_web_socket(self):
        self.ws_conn.open()
        return self
