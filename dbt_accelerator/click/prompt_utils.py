import os

import rich_click as click
from click_repl import repl as internal_repl
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from dbt_accelerator.companion.constant import ABORT_KEYWORD, CLEAR_KEYWORD, PERSIST_FOLDER, PROMPT_COLOR

style = Style.from_dict(
    {
        "": PROMPT_COLOR,
    }
)

prompt_kwargs = {
    "history": FileHistory(os.path.expanduser(PERSIST_FOLDER + "/.repl_history")),
    "message": "> ",
    "style": style,
}


def setup_repl_prompt():
    prompt = "dbt_accelerator> "
    # if EnvironmentConfig().uses.domain:
    #     domain_prompt = EnvironmentConfig().uses.domain
    # if EnvironmentConfig().uses.model:
    #     model_prompt = f"{EnvironmentConfig().uses.model}"
    #     prompt_seperator = ":"
    # if model_prompt is None:
    #     model_prompt = ""
    # if EnvironmentConfig().uses.domain or EnvironmentConfig().uses.model:
    #     prompt = f"dbt_accelerator [{domain_prompt}{prompt_seperator}{model_prompt}] >"
    prompt_kwargs["message"] = prompt


def setup_repl():
    # if EnvironmentConfig().in_repl:
    setup_repl_prompt()
    internal_repl(
        click.get_current_context(),
        prompt_kwargs=prompt_kwargs,
    )


class PromptUtils(object):
    @staticmethod
    def allow_abort(text: str) -> str:
        return f"{text}, '[thistle1]{ABORT_KEYWORD}[/thistle1]' to cancel"

    @staticmethod
    def allow_clear(text: str) -> str:
        return f"{text}, '[thistle1]{CLEAR_KEYWORD}[/thistle1]' to clear"

    @staticmethod
    def color_text(text, color) -> str:
        return f"[{color}]{text}[/{color}]"

    @staticmethod
    def color_red(text: str) -> str:
        return PromptUtils.color_text(text, "red")
