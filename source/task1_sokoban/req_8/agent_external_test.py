NAME = "TeamOther-Test"


def choose_action(view, time_limit):
    """test thu agent ma ko chon bat ki thuat toan nao"""
    del time_limit
    return "East" if view.agent_id == 0 else "West"
