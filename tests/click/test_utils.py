from dbt_accelerator.click.prompt_utils import PromptUtils


def test_PromptUtils_allow_abort():
    assert PromptUtils.allow_abort("me") == "me, '[thistle1]ABORT[/thistle1]' to cancel"


def test_PromptUtils_allow_clear():
    assert PromptUtils.allow_clear("me") == "me, '[thistle1]CLEAR[/thistle1]' to clear"


def test_PromptUtils_color_red():
    assert PromptUtils.color_red("me") == "[red]me[/red]"


def test_PromptUtils_color_text():
    assert PromptUtils.color_text("me", "RED") == "[RED]me[/RED]"
