import pytest

from IncognitoChain.Configs.Constants import PRV_ID, coin
from IncognitoChain.Helpers.Logging import INFO, STEP, WARNING
from IncognitoChain.Helpers.TestHelper import calculate_contribution, l6
from IncognitoChain.Helpers.Time import get_current_date_time, WAIT
from IncognitoChain.Objects.IncognitoTestCase import SUT
from IncognitoChain.Objects.PdeObjects import PDEContributeInfo, wait_for_user_contribution_in_waiting, \
    wait_for_user_contribution_out_waiting
from IncognitoChain.TestCases.DEX import token_id_1, token_owner, token_id_2


@pytest.mark.parametrize('token1,token2', (
        [PRV_ID, PRV_ID],
        # [token_id_1, token_id_1],
        # [token_id_1, token_id_2],
        # [token_id_2, token_id_1]
))
def test_contribute_prv(token1, token2):
    pair_id = f'auto_{l6(token1)}_{l6(token2)}_{get_current_date_time()}'
    tok1_contrib_amount = coin(1234)
    tok2_contrib_amount = coin(2134)
    pde_state_b4 = SUT.REQUEST_HANDLER.get_latest_pde_state_info()
    contr_info = PDEContributeInfo()

    INFO(f"""
            test_DEX20_contribute_reject:
            - contribute a pair of token {l6(token1)} vs {l6(token2)}
            - reject contribution if:
                + same token_id
                + pair not contains prv
            """)
    STEP(0, "Checking env - checking waiting contribution list, pool pair, and share amount")
    assert pde_state_b4.find_waiting_contribution_of_user(token_owner, pair_id, token1) == []
    assert pde_state_b4.find_waiting_contribution_of_user(token_owner, pair_id, token2) == []
    # assert not token_owner.is_my_token_waiting_for_contribution(pair_id, token1)
    # assert not token_owner.is_my_token_waiting_for_contribution(pair_id, token2)

    bal_tok1_be4_contrib = token_owner.get_token_balance(token1)
    bal_tok2_be4_contrib = token_owner.get_token_balance(token2)

    all_share_amount = SUT.full_node.help_get_pde_share_list(token2, token1)
    owner_share_amount = token_owner.get_my_current_pde_share(token2, token1)
    INFO(f'{l6(token1)} balance before contribution: {bal_tok1_be4_contrib}')
    INFO(f'{l6(token2)} balance before contribution: {bal_tok2_be4_contrib}')

    rate = SUT.full_node.get_latest_rate_between(token2, token1)
    if rate is not None:
        INFO(f'Rate before contribution: {l6(token2)}:{l6(token1)} is {rate}')
        INFO(f'Sum share amount before contribution  : {all_share_amount}')
        INFO(f'Owner share amount before contribution: {owner_share_amount}')
    else:
        WARNING(f'{l6(token2)}:{l6(token1)} is not existed, new contribution')
    # breakpoint()
    STEP(1, f"Contribute {l6(token1)}")
    if token1 == PRV_ID:
        contribute_token1_result = token_owner.pde_contribute_prv_v2(tok1_contrib_amount, pair_id)
    else:
        contribute_token1_result = token_owner.pde_contribute_token_v2(token1, tok1_contrib_amount, pair_id)
    contribute_token1_fee = contribute_token1_result.subscribe_transaction().get_fee()

    STEP(2, 'Verify contribution')
    # TODO: get pde contribution status = 1 before continue
    contr_info.wait_for_contribution_status(pair_id, 1)
    # assert token_owner.wait_till_my_token_in_waiting_for_contribution(pair_id, token1)
    wait_for_user_contribution_in_waiting(token_owner, pair_id, token1)

    STEP(3, f'Contribute {l6(token2)}')
    if token2 == PRV_ID:
        contribute_token2_result = token_owner.pde_contribute_prv_v2(tok2_contrib_amount, pair_id)
    else:
        contribute_token2_result = token_owner.pde_contribute_token_v2(token2, tok2_contrib_amount, pair_id)
    contribute_token2_fee = contribute_token2_result.subscribe_transaction().get_fee()
    contrib_fee_sum = contribute_token1_fee + contribute_token2_fee

    STEP(4, f'Verify {l6(token1)} is no longer in waiting contribution list')
    wait_for_user_contribution_out_waiting(token_owner, pair_id, token1)

    STEP(5, f'Get contribution status of {pair_id}')
    # PDENotFoundStatus = 0
    # PDEContributionWaitingStatus = 1 PDEContributionAcceptedStatus = 2 PDEContributionRefundStatus = 3 PDEContributionMatchedNReturnedStatus = 4
    # PDETradeAcceptedStatus = 1 PDETradeRefundStatus = 2
    # PDEWithdrawalAcceptedStatus = 1 PDEWithdrawalRejectedStatus = 2
    # -------

    # Wait for contribution status is rejected
    contr_info.wait_for_contribution_status(pair_id, 3)

    # Wait for balance update:
    if token1 == token2:
        bal_tok1_aft_contrib = token_owner.wait_for_balance_change(token1, bal_tok1_be4_contrib, 100)
        INFO(f'{l6(token1)} after contribute: {bal_tok1_aft_contrib}')
    else:
        bal_tok2_aft_contrib = token_owner.wait_for_balance_change(token2, bal_tok2_be4_contrib, 100)
        bal_tok1_aft_contrib = token_owner.wait_for_balance_change(token1, bal_tok1_be4_contrib, 100)
        INFO(f'{l6(token1)} after contribute: {bal_tok1_aft_contrib}')
        INFO(f'{l6(token2)} after contribute: {bal_tok2_aft_contrib}')

    refund_tok1 = contr_info.get_return_amount_1()
    commit_tok1 = contr_info.get_amount_token1()
    refund_tok2 = contr_info.get_return_amount_2()
    commit_tok2 = contr_info.get_amount_token2()

    # VERIFY: refund amount in API
    assert (refund_tok1 == 0 and commit_tok1 == 0) and INFO(
        f"{l6(token1)} is going to refund"), f"{l6(token1)} refund amount is not correct"
    assert (refund_tok2 == 0 and commit_tok2 == 0) and INFO(
        f"{l6(token2)} is going to refund"), f"{l6(token2)} refund amount is not correct"

    # VERIFY: account balance after refund
    if token1 == token2 and token1 == PRV_ID:
        assert bal_tok1_be4_contrib == bal_tok1_aft_contrib - contrib_fee_sum
        # assert bal_tok2_be4_contrib == bal_tok2_aft_contrib
    elif token1 == token2 and token1 != PRV_ID:
        assert bal_tok1_be4_contrib == bal_tok1_aft_contrib
    elif token2 == PRV_ID:
        assert bal_tok1_be4_contrib == bal_tok1_aft_contrib
        assert bal_tok2_be4_contrib == bal_tok2_aft_contrib - contrib_fee_sum
    else:
        assert bal_tok1_be4_contrib == bal_tok1_aft_contrib - contrib_fee_sum
        assert bal_tok2_be4_contrib == bal_tok2_aft_contrib

    INFO(f"Account balance is verified for {l6(token1)} and {l6(token2)}")

    STEP(6, f'Check rate {l6(token1)} vs {l6(token2)} after contribution')
    rate_after = SUT.full_node.get_latest_rate_between(token1, token2)
    INFO(f'rate {l6(token1)} vs {l6(token2)} = {rate_after}')
    owner_share_amount_after = token_owner.get_my_current_pde_share(token2, token1)
    all_share_amount_after = SUT.full_node.help_get_pde_share_list(token2, token1)

    INFO(f"""
        Owner share amount before: {owner_share_amount}
        Owner share amount after : {owner_share_amount_after}
        All share amount before  : {all_share_amount}
        All share amount after   : {all_share_amount_after}
        Rate before: {rate}
        Rate after : {rate_after}
        Contributed:
            contribute {l6(token1)} : {tok1_contrib_amount}
            contribute {l6(token2)} : {tok2_contrib_amount}
        Expect contribution Refund:
            {l6(token1)}            : {tok1_contrib_amount}
            {l6(token2)}            : {tok2_contrib_amount}
        From API:
            contribute {l6(token1)} : {commit_tok1}
            contribute {l6(token2)} : {commit_tok2}
            return     {l6(token1)} : {refund_tok1}
            return     {l6(token2)} : {refund_tok2}""")

    assert rate == rate_after and INFO(
        "rate after contribution is correct"), f"rate {rate} != {rate_after}"
    assert owner_share_amount == owner_share_amount_after and INFO(
        "owner_share_amount after contribution is correct"), f"owner_share_amount {owner_share_amount} != {owner_share_amount_after}"
    assert all_share_amount == all_share_amount_after and INFO(
        "all_share_amount after contribution is correct"), f"all_share_amount {all_share_amount} != {all_share_amount_after}"