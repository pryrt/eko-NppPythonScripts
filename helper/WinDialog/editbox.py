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
    WindowStyle as WS, WinMessages as WM,
    SendMessage, HIWORD
)
import ctypes

class ES(IntEnum):
    """EditControl Styles: https://learn.microsoft.com/en-us/windows/win32/controls/edit-control-styles
    """
    LEFT            = 0x0000
    CENTER          = 0x0001
    RIGHT           = 0x0002
    MULTILINE       = 0x0004
    UPPERCASE       = 0x0008
    LOWERCASE       = 0x0010
    PASSWORD        = 0x0020
    AUTOVSCROLL     = 0x0040
    AUTOHSCROLL     = 0x0080
    NOHIDESEL       = 0x0100
    OEMCONVERT      = 0x0400
    READONLY        = 0x0800
    WANTRETURN      = 0x1000
    NUMBER          = 0x2000
    
class EN(IntEnum):
    """EditControl Notifications: https://learn.microsoft.com/en-us/windows/win32/controls/bumper-edit-control-reference-notifications
    """
    SETFOCUS        = 0x0100
    KILLFOCUS       = 0x0200
    CHANGE          = 0x0300
    UPDATE          = 0x0400
    ERRSPACE        = 0x0500
    MAXTEXT         = 0x0501
    HSCROLL         = 0x0601
    VSCROLL         = 0x0602
    ALIGN_LTR_EC    = 0x0700
    ALIGN_RTL_EC    = 0x0701
    BEFORE_PASTE    = 0x0800
    AFTER_PASTE     = 0x0801

class EM(IntEnum):
    """Edit Control Messages: https://learn.microsoft.com/en-us/windows/win32/controls/bumper-edit-control-reference-messages
    """
    GETSEL              = 0x00B0
    SETSEL              = 0x00B1
    GETRECT             = 0x00B2
    SETRECT             = 0x00B3
    SETRECTNP           = 0x00B4
    SCROLL              = 0x00B5
    LINESCROLL          = 0x00B6
    SCROLLCARET         = 0x00B7
    GETMODIFY           = 0x00B8
    SETMODIFY           = 0x00B9
    GETLINECOUNT        = 0x00BA
    LINEINDEX           = 0x00BB
    SETHANDLE           = 0x00BC
    GETHANDLE           = 0x00BD
    GETTHUMB            = 0x00BE
    LINELENGTH          = 0x00C1
    REPLACESEL          = 0x00C2
    GETLINE             = 0x00C4
    LIMITTEXT           = 0x00C5
    CANUNDO             = 0x00C6
    UNDO                = 0x00C7
    FMTLINES            = 0x00C8
    LINEFROMCHAR        = 0x00C9
    SETTABSTOPS         = 0x00CB
    SETPASSWORDCHAR     = 0x00CC
    EMPTYUNDOBUFFER     = 0x00CD
    GETFIRSTVISIBLELINE = 0x00CE
    SETREADONLY         = 0x00CF
    SETWORDBREAKPROC    = 0x00D0
    GETWORDBREAKPROC    = 0x00D1
    GETPASSWORDCHAR     = 0x00D2
    SETMARGINS          = 0x00D3
    GETMARGINS          = 0x00D4
    SETLIMITTEXT        = LIMITTEXT   # win40 Name change
    GETLIMITTEXT        = 0x00D5
    POSFROMCHAR         = 0x00D6
    CHARFROMPOS         = 0x00D7
    SETIMESTATUS        = 0x00D8
    GETIMESTATUS        = 0x00D9
    ENABLEFEATURE       = 0x00DA
    

class EditBox(Control):
    """Implementation for a standard EDIT control"""
    # https://docs.microsoft.com/en-us/windows/desktop/Controls/static-control-styles   => coped from LABEL
    # https://learn.microsoft.com/en-us/windows/win32/controls/edit-control-styles

    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.windowClass = 'EDIT'
        self.style = WS.BORDER | WS.CHILD | WS.VISIBLE | WS.HSCROLL | WS.VSCROLL | ES.MULTILINE | ES.AUTOVSCROLL | ES.AUTOHSCROLL | ES.WANTRETURN
        self.name = name
        self.size = size
        self.position = position

    def callback(self, wparam, lparam):
        match HIWORD(wparam):
            case EN.CHANGE:
                print(f"[DEBUG] EditBox.callback(w:0x{wparam:08x},l:0x{lparam:08x})\tCHANGE NOTIFICATION")
                self.get_text()
            case _:
                return

    def get_text(self):
        l = SendMessage(self.hwnd, WM.GETTEXTLENGTH, 0, 0)
        ubuf = ctypes.create_unicode_buffer(l+1) # allow length for final NULL character
        lp_ubuf = ctypes.addressof(ubuf)
        r = SendMessage(self.hwnd, WM.GETTEXT, l+1, lp_ubuf)
        print(f"[DEBUG] EditBox.get_text() => Post Buffer = '{ubuf.value}', r={r}")
        return ubuf.value
    
