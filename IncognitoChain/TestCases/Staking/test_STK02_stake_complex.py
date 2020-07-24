"""
1. keep chain data after run the previous tc
2. as step2. accountU stake for A. verify account U -1750PRV -tx_fee
3.4.5.6.8 as previous. 7. AccountU +1750PRV
9. run all step of case1 (skip step1) with account A
10. run all step of case1 (skip step1) with account T
11. run all step of case1 (skip step1) with account U
"""
from IncognitoChain.Configs.Constants import coin
from IncognitoChain.Objects.IncognitoTestCase import COIN_MASTER
from IncognitoChain.TestCases.Staking import account_u, account_a, account_t
from IncognitoChain.TestCases.Staking.test_STK01 import \
    test_self_stake_n_stake_other_with_auto_stake_false as do_stake_test


def test_stake_complex():
    accounts = [account_a, account_t, account_u]
    multi_out_put = dict()
    for acc in accounts:
        if acc.get_prv_balance() <= coin(1750):
            multi_out_put[acc] = coin(1850) - acc.get_prv_balance_cache()

    COIN_MASTER.send_prv_to_multi_account(multi_out_put, privacy=0).subscribe_transaction()

    try:
        account_u.subscribe_cross_output_coin()
    except:
        pass

    do_stake_test(account_u, account_a)
    do_stake_test(account_a, account_a)
    do_stake_test(account_t, account_t)
    do_stake_test(account_u, account_u)
