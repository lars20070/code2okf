"""code2okf: compile Markdown into an OKF wiki with the Pi coding agent."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("code2okf")
except PackageNotFoundError:
    __version__ = "0.0.0+local"
