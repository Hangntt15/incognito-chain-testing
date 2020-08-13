import pytest

from IncognitoChain.Configs.Constants import coin, PRV_ID
from IncognitoChain.Helpers.Logging import INFO, STEP, INFO_HEADLINE
from IncognitoChain.Helpers.TestHelper import l6
from IncognitoChain.Helpers.Time import get_current_date_time, WAIT
from IncognitoChain.Objects.IncognitoTestCase import SUT, ACCOUNTS
from IncognitoChain.TestCases.DEX import token_owner, token_id_1, token_id_2


def setup_function():
    token_owner.top_him_up_token_to_amount_if(token_id_1, coin(500), coin(1000), ACCOUNTS)
    token_owner.top_him_up_token_to_amount_if(token_id_2, coin(500), coin(1000), ACCOUNTS)
    token_owner.top_him_up_token_to_amount_if(PRV_ID, coin(500), coin(1000), ACCOUNTS)


@pytest.mark.parametrize('contributors, contribute_percent_of_bal_tok2, token1, token2', [
    (ACCOUNTS, 0.01, PRV_ID, token_id_1),
    # (ACCOUNTS, 0.1, token_id_1, token_id_2),
])
def test_add_liquidity_v2(contributors, contribute_percent_of_bal_tok2, token1, token2):
    pde_state_b4_test = SUT.REQUEST_HANDLER.get_latest_pde_state_info()
    rate_b4_test = pde_state_b4_test.get_rate_between_token(token1, token2)
    INFO_HEADLINE(f'Test tokens: {l6(token1)}:{l6(token2)}. Rate {rate_b4_test}')
    contributor_balance_tok1_b4 = {}
    contributor_balance_tok2_b4 = {}
    contributor_balance_tok1_af = {}
    contributor_balance_tok2_af = {}
    pair_ids = {}
    commit_amount_tok1 = {}
    commit_amount_tok2 = {}
    for account in contributors + [token_owner]:
        contributor_balance_tok1_b4[account] = account.get_token_balance(token1)
        contributor_balance_tok2_b4[account] = account.get_token_balance(token2)

    INFO(f'Private key | To commit {l6(token1)}/{l6(token2)} | balance {l6(token1)}/{l6(token2)} | '
         f'share amount {l6(token2)}')
    for account in contributors:
        pair_id = f'{l6(account.private_key)}_{l6(token1)}_{l6(token2)}_{get_current_date_time()}'
        pair_ids[account] = pair_id
        bal_tok1 = contributor_balance_tok1_b4[account]
        bal_tok2 = contributor_balance_tok2_b4[account]
        amount2 = int(bal_tok2 * contribute_percent_of_bal_tok2)
        amount1 = int(amount2 * rate_b4_test[0] / rate_b4_test[1])
        commit_amount_tok1[account] = amount1
        commit_amount_tok2[account] = amount2
        assert amount1 != 0, f'Calculated commit amount for {l6(token1)} is 0'
        assert amount2 != 0, f'Calculated commit amount for {l6(token2)} is 0'
        pde_share = pde_state_b4_test.get_pde_shares_amount(account, token1, token2)
        INFO("%8s %11s/%s %9s/%s %13s" % (l6(account.private_key), amount1, amount2, bal_tok1, bal_tok2, pde_share))

    STEP(1, f'Contribute {l6(token1)}')
    for acc in contributors:
        pair_id = pair_ids[acc]
        contribute_tx = acc.pde_contribute_v2(token1, commit_amount_tok1[acc], pair_id)
        contribute_tx.expect_no_error()
        INFO(f"Contribute {l6(token1)} tx_id: {contribute_tx.get_tx_id()} ")

    STEP(2, f'Wait 40s then verify contribution {l6(token1)} is in waiting list')
    WAIT(40)
    pde_state_after_contribute = SUT.REQUEST_HANDLER.get_latest_pde_state_info()
    for acc in contributors:
        pair_id = pair_ids[acc]
        assert pde_state_after_contribute.find_waiting_contribution_of_user(acc, pair_id, token1) != []

    STEP(3, f'Contribute {l6(token2)}')
    for acc in contributors:
        pair_id = pair_ids[acc]
        contribute_tx = acc.pde_contribute_v2(token2, commit_amount_tok2[acc], pair_id)

        contribute_tx.expect_no_error()
        INFO(f"Contribute {l6(token1)}, tx_id: {contribute_tx.get_tx_id()}")

    STEP(4, f'Wait 50s then verify {l6(token1)} is no longer in waiting list')
    WAIT(50)
    pde_state_after_test = SUT.full_node.get_latest_pde_state_info()
    for acc in contributors:
        pair_id = pair_ids[acc]
        assert pde_state_after_test.find_waiting_contribution_of_user(acc, pair_id, token1) == []

    STEP(5, 'Wait 30s then check balance after contribution')
    WAIT(30)
    for account in contributors + [token_owner]:
        contributor_balance_tok1_af[account] = account.get_token_balance(token1)
        contributor_balance_tok2_af[account] = account.get_token_balance(token2)

    INFO(f'User  | bal {l6(token1)} before/after  | {l6(token1)} commit amount | '
         f'bal {l6(token2)} before/after  | {l6(token2)} commit amount | '
         f'share amount before/after')
    for account in contributors:
        pde_share_b4 = pde_state_b4_test.get_pde_shares_amount(account, token1, token2)
        pde_share_after = pde_state_after_test.get_pde_shares_amount(account, token1, token2)
        bal_tok1_b4 = contributor_balance_tok1_b4[account]
        bal_tok2_b4 = contributor_balance_tok2_b4[account]
        bal_tok1_af = contributor_balance_tok1_af[account]
        bal_tok2_af = contributor_balance_tok2_af[account]

        INFO(f'{l6(account.payment_key)} | {bal_tok1_b4}/{bal_tok1_af} | {commit_amount_tok1[account]} | '
             f'{bal_tok2_b4}/{bal_tok2_af} | {commit_amount_tok2[account]} | '
             f'{pde_share_b4}/{pde_share_after}')

    STEP(6, f"Check rate {l6(token2)} vs {l6(token1)}")
    rate_before = pde_state_b4_test.get_rate_between_token(token1, token2)
    rate_after = pde_state_after_test.get_rate_between_token(token1, token2)

    sum_commit_token_1 = sum(commit_amount_tok1.values())
    sum_commit_token_2 = sum(commit_amount_tok2.values())

    INFO('Rate before test + sum contribute amount - rate after test')
    # each contribute calculation can be off by 1 nano,
    # so expect sum calculation will be off no more than: 1 * num of contributors
    assert abs(rate_before[0] + sum_commit_token_1 - rate_after[0]) <= len(contributors) and \
           INFO(f'{rate_before[0]} + {sum_commit_token_1} - {rate_after[0]} '
                f'= {rate_before[0] + sum_commit_token_1 - rate_after[0]}')

    assert abs(rate_before[1] + sum_commit_token_2 - rate_after[1]) <= len(contributors) and \
           INFO(f'{rate_before[1]} + {sum_commit_token_2} - {rate_after[1]} '
                f'= {rate_before[1] + sum_commit_token_2 - rate_after[1]}')