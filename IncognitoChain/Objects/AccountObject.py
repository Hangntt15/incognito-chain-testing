from typing import List


class Account:

    def __init__(self, private_key=None, payment_key=None, shard=None,
                 validator_key=None, public_key=None, read_only_key=None):
        self.private_key = private_key
        self.validator_key = validator_key
        self.payment_key = payment_key
        self.public_key = public_key
        self.read_only_key = read_only_key
        self.shard = shard

    def __eq__(self, other):
        if self.private_key == other.private_key:
            return True
        return False

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        return True

    def from_json(self, json_string):
        self.public_key = json_string.get('public')
        self.private_key = json_string.get('private')
        self.payment_key = json_string.get('payment')
        self.read_only_key = json_string.get('read')
        self.validator_key = json_string.get('validator')
        self.shard = json_string.get('shard')
        return self

    def __str__(self):
        return f'Shard = {self.shard}\n' + \
               f'Private key = {self.private_key}\n' + \
               f'Payment key = {self.payment_key}\n' + \
               f'Read only key = {self.read_only_key}\n' + \
               f'Validator key = {self.validator_key}\n' + \
               f'Public key = {self.public_key}\n'

    def find_in_list(self, a_list: list):
        for account in a_list:
            if self.__eq__(account):
                return a_list.index(account)
        return -1

    def get_token_balance(self, token_id):
        pass

    def get_prv_balance(self, shard_id=None):
        """
        get account's prv balance, by default it will ask the full node.
        when the shard_id is specify, then it will on that shard
        if shard if = -1, it will ask for the balance on it own shard
        :param shard_id:
        :return:
        """
        from IncognitoChain.Objects.IncognitoTestCase import SUT
        if shard_id is None:
            return SUT.full_node.transaction().get_balance(self.private_key)
        if shard_id == -1:
            shard_to_ask = self.shard
        else:
            shard_to_ask = shard_id
        return SUT.shards[shard_to_ask].get_representative_node().transaction().get_balance(self.private_key)

    def send_prv_to(self, to_account, amount_prv, fee=-1, privacy=1):
        from IncognitoChain.Objects.IncognitoTestCase import SUT
        return SUT.full_node.transaction(). \
            send_transaction(self.private_key, to_account.payment_key, amount_prv, fee, privacy)


def get_accounts_in_shard(shard_number: int, account_list) -> List[Account]:
    accounts_in_shard: List[Account] = []
    for account in account_list:
        if account.shard == shard_number:
            accounts_in_shard.append(account)
    return accounts_in_shard