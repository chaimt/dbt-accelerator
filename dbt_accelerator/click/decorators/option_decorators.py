import logging
import typing as t

import rich_click as click
from click.core import Option as Option
from click.decorators import FC, _param_memo

logger = logging.getLogger(__name__)


def build_option(f, param_decls, option_attrs):
    OptionClass = option_attrs.pop("cls", Option)
    _param_memo(f, OptionClass(param_decls, **option_attrs))
    return f


def trace_option() -> t.Callable[[FC], FC]:
    def decorator(f: FC) -> FC:
        return build_option(
            f,
            ("-t", "--trace"),
            {"default": False, "help": "Enable :point_right: [yellow]debug mode[/] :point_left:", "is_flag": True},
        )

    return decorator


def dry_run_option() -> t.Callable[[FC], FC]:
    def decorator(f: FC) -> FC:
        return build_option(f, ("-dr", "--dry-run"), {"help": "Dry run w/o any actual execution", "default": False, "is_flag": True})

    return decorator


# def full_build_option() -> t.Callable[[FC], FC]:
#     def decorator(f: FC) -> FC:
#         return build_option(f, ("-f", "--full"), {"default": False, "show_default": True, "help": "compile full build", "is_flag": True})

#     return decorator


def filenames_option() -> t.Callable[[FC], FC]:
    def decorator(f: FC) -> FC:
        return build_option(
            f,
            ("-f", "--filenames"),
            {"default": "", "is_flag": False, "help": "Sets target filenames", "metavar": "<filenames>", "type": click.STRING},
        )

    return decorator


# def deps_option() -> t.Callable[[FC], FC]:
#     def decorator(f: FC) -> FC:
#         return build_option(f, ("-deps", "--deps"), {"default": False, "help": "Add deps command to compile", "is_flag": True})

#     return decorator


# def models_option(action) -> t.Callable[[FC], FC]:
#     def decorator(f: FC) -> FC:
#         return build_option(f, ("-m", "--models"), {"type": str, "help": "Name of model(s) to " + action, "multiple": True})

#     return decorator


# def upstream_option(action) -> t.Callable[[FC], FC]:
#     def decorator(f: FC) -> FC:
#         return build_option(
#             f,
#             ("-u", "--upstream"),
#             {
#                 "default": True,
#                 "help": f"{action} upstream model(s) (of specified model(s))",
#                 "is_flag": True,
#             },
#         )

#     return decorator


# def downstream_option(action) -> t.Callable[[FC], FC]:
#     def decorator(f: FC) -> FC:
#         return build_option(
#             f,
#             ("-d", "--downstream"),
#             {
#                 "default": False,
#                 "help": f"{action} downstream model(s) (of specified model(s))",
#                 "is_flag": True,
#             },
#         )

#     return decorator
