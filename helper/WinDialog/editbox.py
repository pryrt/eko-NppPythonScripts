""" Dialog EDIT control implementation

For now, it's basically a copy of the LABEL control

reference:
- https://stackoverflow.com/questions/11379421/how-to-create-an-embedded-text-input-box-in-win32-windows
    CreateWindow(
        "EDIT", 
        0,  // name
        WS_BORDER|WS_CHILD|WS_VISIBLE, 
        56, 
        10, 
        50, 
        18, 
        g_hWnd, 
        0, 
        hInst, 
        0
    );
- https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowa
    void CreateWindowA(
        [in, optional]  lpClassName,
        [in, optional]  lpWindowName,
        [in]            dwStyle,
        [in]            x,
        [in]            y,
        [in]            nWidth,
        [in]            nHeight,
        [in, optional]  hWndParent,
        [in, optional]  hMenu,
        [in, optional]  hInstance,
        [in, optional]  lpParam
    );
- https://learn.microsoft.com/en-us/windows/win32/controls/edit-control-styles
    CreateWindow(
        "EDIT",
        NULL,
        WS_BORDER | WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_LEFT | ES_MULTILINE | ES_AUTOVSCROLL,
        0,0,0,0,
        hwnd,
        (HMENU) ID_OUTBOX,
        (HINSTANCE) GetWindowLongPtr(hwnd, GWLP_HINSTANCE),
        NULL
   )
"""

from enum import IntEnum
from .dialog_template import Control
from .win_helper import (
    WindowStyle as WS
)

class SS(IntEnum):
    LEFT             = 0x00000000
    CENTER           = 0x00000001
    RIGHT            = 0x00000002
    ICON             = 0x00000003
    BLACKRECT        = 0x00000004
    GRAYRECT         = 0x00000005
    WHITERECT        = 0x00000006
    BLACKFRAME       = 0x00000007
    GRAYFRAME        = 0x00000008
    WHITEFRAME       = 0x00000009
    USERITEM         = 0x0000000A
    SIMPLE           = 0x0000000B
    LEFTNOWORDWRAP   = 0x0000000C
    OWNERDRAW        = 0x0000000D
    BITMAP           = 0x0000000E
    ENHMETAFILE      = 0x0000000F
    ETCHEDHORZ       = 0x00000010
    ETCHEDVERT       = 0x00000011
    ETCHEDFRAME      = 0x00000012
    TYPEMASK         = 0x0000001F
    REALSIZECONTROL  = 0x00000040
    NOPREFIX         = 0x00000080  # Don't do "&" character translation
    NOTIFY           = 0x00000100
    CENTERIMAGE      = 0x00000200
    RIGHTJUST        = 0x00000400
    REALSIZEIMAGE    = 0x00000800
    SUNKEN           = 0x00001000
    EDITCONTROL      = 0x00002000
    ENDELLIPSIS      = 0x00004000
    PATHELLIPSIS     = 0x00008000
    WORDELLIPSIS     = 0x0000C000
    ELLIPSISMASK     = 0x0000C000


class EditBox(Control):
    """Implementation for a standard EDIT control"""
    # https://docs.microsoft.com/en-us/windows/desktop/Controls/static-control-styles   => coped from LABEL
    # https://learn.microsoft.com/en-us/windows/win32/controls/edit-control-styles
        # TODO: implement the ES constants from the Edit Control Styles, similar to how
        #   the copy from LABEL implements the SS constants from Static (LABEL) Control Styles


    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.windowClass = 'EDIT'
        self.style = WS.BORDER | WS.CHILD | WS.VISIBLE | WS.VSCROLL
        self.name = name
        self.size = size
        self.position = position

    def callback(self, wparam, lparam):
        print(f"EditBox Callback w:0x{wparam:04x} l:0x{lparam:04x}")

