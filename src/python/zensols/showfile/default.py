"""Web browser default implementation.

"""
__author__ = 'Paul Landes'

from typing import Dict, Sequence, List
from dataclasses import dataclass, field
import logging
from pathlib import Path
import webbrowser
import screeninfo as si
from screeninfo.common import Monitor
from zensols.util import APIError
from zensols.persist import persisted
from . import Size, Extent, Browser

logger = logging.getLogger(__name__)


@dataclass
class WebBrowser(Browser):
    """A class that displays a file or URL in a web browser.

    """
    def _file_to_url(self, path: Path) -> str:
        return f'file://{path.absolute()}'

    def _open_url(self, url: str):
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'opening browser at: {url}')
        webbrowser.open(url, autoraise=False)

    def _get_screen_size(self) -> Size:
        mons: List[Monitor] = si.get_monitors()
        mon: Monitor = next(iter(filter(lambda m: m.is_primary, mons)))
        return Size(mon.width, mon.height)

    def show_file(self, path: Path, extent: Extent = None):
        self._open_url(self._file_to_url(path))

    def show_url(self, url: str, extent: Extent):
        self._open_url(url)