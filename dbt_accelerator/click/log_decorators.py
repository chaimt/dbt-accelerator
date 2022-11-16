import logging
import typing as t
from functools import update_wrapper

from click.decorators import FC, F
from click.exceptions import Abort

logger = logging.getLogger(__name__)


def wrap_action(action: str) -> t.Callable[[FC], FC]:
    def pass_action(f: F) -> F:
        """Similar to :func:`pass_context`, but only pass the object on the
        context onwards (:attr:`Context.obj`).  This is useful if that object
        represents the state of a nested system.
        """

        def new_func(*args, **kwargs):  # type: ignore
            logger.info("-----------------------------------------")
            logger.info(f"Action: {action}")
            try:
                return f(*args, **kwargs)
            except Abort:
                logger.info("Aborted")
                return None

        return update_wrapper(t.cast(F, new_func), f)

    return pass_action
