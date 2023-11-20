"""Utilities and constants."""

import asyncio

__all__ = ["LOOP_WAIT", "EM", "LORUM", "wait_coro"]

LOOP_WAIT = 0.015
EM = 8  # In px.
LORUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum at "
    "elit non orci luctus porta et sit amet turpis. Vestibulum magna velit, "
    "finibus vel luctus vitae, condimentum eleifend diam. Maecenas ultrices "
    "neque at orci porta, a gravida eros aliquam. Phasellus eget ex placerat, "
    "condimentum nunc eget, convallis ante. Quisque feugiat magna massa, sit "
    "amet consectetur velit iaculis non. Aliquam nec."
)


def wait_coro(coro, loop):
    """Wait for async coroutine to complete.

    Args:
        coro (Coroutine): Coroutine to wait for.
        loop (asyncio.AbstractEventLoop, optional): Asyncio event loop to use.

    Returns:
        Any: Return value of the coroutine.
    """
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        return future.result()
    finally:
        future.cancel()