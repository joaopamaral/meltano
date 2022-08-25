"""Various utils and formatters for log rendering control."""

from __future__ import annotations

from typing import Sequence

import structlog
from structlog.types import Processor

TIMESTAMPER = structlog.processors.TimeStamper(fmt="iso")

LEVELED_TIMESTAMPED_PRE_CHAIN = frozenset(
    (
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        TIMESTAMPER,
    )
)


def _process_formatter(processor: Processor):
    """Use _process_formatter to configure a structlog.stdlib.ProcessFormatter.

    It will automatically add log level and timestamp fields to any log entries not originating from structlog.

    Args:
        processor: A structlog message processor such as structlog.dev.ConsoleRenderer.

    Returns:
        A configured log processor.
    """
    return structlog.stdlib.ProcessorFormatter(
        processor=processor, foreign_pre_chain=LEVELED_TIMESTAMPED_PRE_CHAIN
    )


def console_log_formatter(
    colors: bool = False, exception_formatter: str = "plain"
) -> None:
    """Create a logging formatter for console rendering that supports colorization.

    Args:
        colors: Add color to output.
        exception_formatter: Format exceptions as "plain" or "rich".

    Returns:
        A configured console log formatter.
    """
    processor = (
        structlog.dev.ConsoleRenderer(colors=colors)
        if exception_formatter == "rich"
        else structlog.dev.ConsoleRenderer(
            colors=colors, exception_formatter=structlog.dev.plain_traceback
        )
    )
    return _process_formatter(processor)


def key_value_formatter(
    sort_keys: bool = False,
    key_order: Sequence[str] | None = None,
    drop_missing: bool = False,
) -> None:
    """Create a logging formatter that renders lines in key=value format.

    Args:
        sort_keys: Whether to sort keys when formatting.
        key_order: key_order: List of keys that should be rendered in this exact order. Missing keys will be rendered as None, extra keys depending on *sort_keys* and the dict class.
        drop_missing: When True, extra keys in *key_order* will be dropped rather than rendered as None.

    Returns:
        A configured key=value formatter.
    """
    return _process_formatter(
        processor=structlog.processors.KeyValueRenderer(
            sort_keys=sort_keys, key_order=key_order, drop_missing=drop_missing
        )
    )


def json_formatter() -> None:
    """Create a logging formatter that renders lines in JSON format.

    Returns:
        A configured JSON formatter.
    """
    return _process_formatter(processor=structlog.processors.JSONRenderer())
