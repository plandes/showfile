"""Command line entry point to the application.

"""
__author__ = 'Paul Landes'

from typing import List, Any, Dict, Union
import sys
from zensols.cli import ActionResult, CliHarness
from zensols.cli import ApplicationFactory as CliApplicationFactory


class ApplicationFactory(CliApplicationFactory):
    def __init__(self, *args, **kwargs):
        kwargs['package_resource'] = 'zensols.showfile'
        super().__init__(*args, **kwargs)

    def get_instance(self, args: Union[List[str], str] = None) -> Any:
        """Get the application instance."""
        if args is None:
            args = 'config'
        return super().get_instance(args)


def main(args: List[str] = sys.argv, **kwargs: Dict[str, Any]) -> ActionResult:
    harness: CliHarness = ApplicationFactory.create_harness(relocate=False)
    harness.invoke(args, **kwargs)
