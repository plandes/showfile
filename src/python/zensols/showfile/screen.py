"""Domain classes and the a screen manager class.

"""
__author__ = 'Paul Landes'

from typing import Sequence, Dict, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import textwrap
from pathlib import Path
import applescript as aps
from applescript._result import Result
import re
from zensols.util import APIError
from zensols.config import Dictable, ConfigFactory
from zensols.persist import persisted
from zensols.cli import ApplicationError

logger = logging.getLogger(__name__)


class ApplescriptError(APIError):
    pass


class ErrorType(Enum):
    ignore = auto()
    warning = auto()
    error = auto()


@dataclass(eq=True, unsafe_hash=True)
class Size(Dictable):
    """A screen size configuration.  This is created either for the current
    display, or one that's configured.

    """
    width: int
    height: int

    def __str__(self):
        return f'{self.width} X {self.height}'


@dataclass(eq=True, unsafe_hash=True)
class Extent(Size):
    """The size (parent class) and the position of the screen.

    """
    x: int = field(default=0)
    y: int = field(default=0)


@dataclass(eq=True, unsafe_hash=True)
class Display(Size):
    """The screen display.

    """
    _DICTABLE_WRITE_EXCLUDES = {'name'}
    name: str = field()
    """The name of the display as the section name in the configuration."""

    target: Extent = field()
    """The extends of the display or what to use for the Preview app."""

    def __str__(self):
        return super().__str__() + f' ({self.name})'


@dataclass
class ScreenManager(object):
    """Resizing Preview.app based on provided screen configuration.
    """
    config_factory: ConfigFactory = field()
    """Set by the framework and used to get other configurations."""

    show_preview_script_path: Path = field()
    """The applescript file path used for managing Preview.app."""

    display_names: Sequence[str] = field(default_factory=list)
    """The configured display names, used to fetch displays in the
    configuration.

    """
    applescript_warns: Dict[str, str] = field(default_factory=set())
    """A set of string warning messages to log instead raise as an
    :class:`.ApplicationError`.

    """
    switch_back_app: str = field(default=None)
    """The application to activate (focus) after the resize is complete."""

    def _get_error_type(self, res: Result) -> ErrorType:
        err: str = res.err
        for warn, error_type in self.applescript_warns.items():
            if err.find(warn) > -1:
                return ErrorType[error_type]
        return ErrorType.throw

    def _exec(self, cmd: str, app: str = None) -> str:
        ret: aps.Result
        if app is None:
            ret = aps.run(cmd)
        else:
            ret = aps.tell.app(app, cmd)
        if ret.code != 0:
            err_type: ErrorType = self._get_error_type(ret)
            cmd_str: str = textwrap.shorten(cmd, 40)
            msg: str = f'Could not invoke <{cmd_str}>: {ret.err} ({ret.code})'
            if err_type == ErrorType.warning:
                logger.warning(msg)
            elif err_type == ErrorType.error:
                raise ApplescriptError(msg)
        return ret.out

    @property
    @persisted('_displays')
    def displays(self) -> Dict[str, Size]:
        """The configured displays."""
        def map_display(name: str) -> Display:
            targ = Extent(**fac(f'{name}_target').asdict())
            return Display(**fac(name).asdict() |
                           {'name': name, 'target': targ})

        fac = self.config_factory
        return {d.name: d for d in map(map_display, self.display_names)}

    @property
    @persisted('_displays_by_size')
    def displays_by_size(self) -> Dict[Size, Display]:
        """A dictionary of displays keyed by size."""
        return {Size(d.width, d.height): d for d in self.displays.values()}

    @property
    @persisted('_show_preview_script')
    def show_preview_script(self) -> str:
        """The applescript content used for managing Preview.app."""
        with open(self.show_preview_script_path) as f:
            return f.read()

    @property
    def screen_size(self) -> Size:
        """Get the screen size for the current display."""
        bstr: str = self._exec('bounds of window of desktop', 'Finder')
        bounds: Sequence[int] = tuple(map(int, re.split(r'\s*,\s*', bstr)))
        width, height = bounds[2:]
        return Size(width, height)

    def _switch_back(self):
        if self.switch_back_app is not None:
            self._exec(f'tell application "{self.switch_back_app}" to activate')

    def resize(self, file_name: Path, extent: Extent):
        """Open and resize a file.

        :param file_name: the PDF (or image) file to resize

        :param extent: the screen position of where to put the app

        """
        logger.info(f'resizing {file_name.name} to {extent}')
        file_name_str: str = str(file_name.absolute())
        fn = (f'showPreview("{file_name_str}", {extent.x}, {extent.y}, ' +
              f'{extent.width}, {extent.height})')
        cmd = (self.show_preview_script + '\n' + fn)
        self._exec(cmd)
        self._switch_back()

    def detect_and_resize(self, file_name: Path):
        """Like :meth:`resize` but use the screen extents of the current screen.

        :param file_name: the PDF (or image) file to resize

        """
        screen: Size = self.screen_size
        display: Display = self.displays_by_size.get(screen)
        logger.debug(f'screen size: {screen} -> {display}')
        if display is None:
            raise ApplicationError(f'No display entry for bounds: {screen}')
        logger.debug(f'detected display {display}')
        self.resize(file_name, display.target)
