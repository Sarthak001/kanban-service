import structlog
from pathlib import Path


def configure_logger(log_file_path=None):
    # Configure structlog
    structlog.configure(
        processors=[
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.WriteLoggerFactory(
        file=Path(log_file_path).with_suffix(".log").open("wt")
    ),    
    )
    return structlog.get_logger()