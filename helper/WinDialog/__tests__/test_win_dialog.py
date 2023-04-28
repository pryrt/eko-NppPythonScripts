from Npp import console
from WinDialog import (
    Dialog,
    Button, CheckBoxButton, GroupBox, CommandButton, RadioButton,
    SimpleLabel, TruncatedLabel, BlackFramedLabel, CenteredLabel, RigthAlignedLabel,
    ComboBox, EditBox
)

console.show()

class ButtonDialog(Dialog):
    def __init__(self, title='Some buttons dialog'):
        super().__init__(title)

        _button1 = CheckBoxButton('Simple', (90,14), (10, 10))
        _button1.on_click = lambda: self.on_click(_button1)
        _button2 = CheckBoxButton('Three state check box', (90,14), (10, 30), three_state=True)
        _button2.on_click = lambda: self.on_click(_button2)

        _button3 = GroupBox('Group Box 1', (160, 30), (10, 50))
        # _button3a starts a new group of radio buttons,
        # all following radio buttons are part of this group
        # unless they start a new group
        _button3a = RadioButton('Radio button 1', (60,14), (20, 60), group=True)
        _button3b = RadioButton('Radio button 2', (60,14), (90, 60))
        # new group started by _button4a
        _button4 = GroupBox('Group Box 2', (160, 30), (10, 90))
        _button4a = RadioButton('Radio button 1', (60,14), (20, 100), group=True)
        _button4b = RadioButton('Radio button 2', (60,14), (90, 100))

        _button5 = Button('Close dialog', (80,22), (10,130))
        _button5.on_click = self.on_close

        _button6 = Button('Default push button', (80,22), (90,130))
        _button6.set_default()
        _button6.on_click = lambda: self.on_click(_button6)

        _button7 = CommandButton('Command link', (100,26), (10,160))

        self.add_controls([
               _button1, _button2,
               _button3, _button3a, _button3b,
               _button4, _button4a, _button4b,
               _button5, _button6,
               _button7,
               ])
        self.show()

    def on_close(self):
        self.terminate()

    def on_click(self, btn):
        print(f"button clicked: {self} {btn.name}")


class LabelDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)

        _label1 = SimpleLabel('Simple label', (90, 14), (10, 10))
        _label2 = TruncatedLabel('Simple label with truncates text', (80, 14), (10, 30))
        _label3 = BlackFramedLabel('', (90, 30), (10, 50))
        _label4 = SimpleLabel('Label within black frame', (90,14), (15, 60))
        _label6 = CenteredLabel('Centered label', (90, 14), (10, 90))
        _label7 = RigthAlignedLabel('Right alligned label', (90, 14), (10, 110))
        
        _edit1 = EditBox('Default EditBox', (120,42), (10,130))

        self.add_controls([ _label1, _label2, _label3, _label4,  _label6, _label7, _edit1 ])
        self.show()

class ComboBoxDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)
        self.size = (110, 120)
        self.cb1 = ComboBox((80,10), (10,10))
        self.cb1.items = ['Item1', 'Item2', 'Item3',]
        self.cb1.on_selchange = self.on_selchange

        self.cb2 = ComboBox((80,10), (10,60))
        self.cb2.items = []
        self.cb2.on_selchange = self.on_selchange2

        self.add_controls([self.cb1, self.cb2])
        self.on_selchange()
        self.show()

    def on_selchange(self):
        match self.cb1.get_selected_item():
            case 0:
                self.cb2.update(['100', '101', '102',])
            case 1:
                self.cb2.update(['200', '201', '202',])
            case _:
                self.cb2.update(['301', '301', '302',])

    def on_selchange2(self):
        s1 = self.cb1.items[self.cb1.get_selected_item()]
        s2 = self.cb2.items[self.cb2.get_selected_item()]
        print(f"selected {s1}.{s2}\n")

from random import random

class EditDialog(Dialog):
    def __init__(self, title='test dialog with edit'):
        super().__init__(title)
        
        _edit1 = EditBox('My Initial Text', (120,42), (10,10))
        _edit1.set_text("Yo!")

        _button_ok = Button('Close dialog', (80,22), (10,62))
        _button_ok.on_click = lambda: self.on_ok(_edit1)
        
        _button_rnd = Button('Random', (80,22), (10,88))
        _button_rnd.on_click = lambda: _edit1.set_text(str(random()))

        _button_print = Button('Print Text', (80,22), (10,114))
        _button_print.on_click = lambda: print("Print Text => '{}'".format(_edit1.get_text()))

        self.add_controls([ _edit1, _button_ok, _button_rnd, _button_print ])
        _edit1.set_text("Before Show")
        self.show()
        _edit1.set_text("After Show")

    def on_ok(self, _editbox):
        # simple way to access the editbox text: pass the editbox reference through the on_click lambda,
        #   and then use that pass-parameter
        print(f"OK => editbox:'{_editbox.get_text()}'")
        
        # alternate method: the elements of self.control_list are in the order from the .add_controls above,
        #   the following commented-out code shows me verifying this, and seeing what other meta-info
        #   #   for c in self.control_list:
        #   #       print(f"\tctrl.name='{c.name}', ctrl.title='{c.title}', ctrl.windowClass='{c.windowClass}'")
        #   but now that I know, if I knew that _edit1 was the first element in the self.control_list,
        #   I could just call self.control_list[0].get_text() directly.
        #
        #   side note: c.name and c.title are both set to the initial text that populates
        #       the control when it's created.  Added .set_text(str) similar to 
        #       .get_text() ... but since Eko is actively working on the RC-file-parsing version
        #       of this library, and his demo implies that it will have EDIT controls,
        #       it may be moot in the near future anyway.
        #       Unfortunately, no matter where I try it, there isn't a place I can put it between the 
        #       creation of the control and the .show() where I can change the text, so I cannot give
        #       the control a separate title compared to the initial visible text.
        
        # close the dialog
        self.terminate()
        pass


#ButtonDialog()
#LabelDialog()
#ComboBoxDialog()
EditDialog()

"""
Peter's Notes:
- all the win32 calls are done in the .show() method => .__create_dialog() method
    - defines an  byte array "controls"
    - for each control, convert the python data into a bytearray (control.create())
      appends it to the "controls" byte array, and aligns it to a multiple of sizeof(DWORD)
    - it then creates the Window object in python, 
        translates it to a bytearrat using .create(),
        and aligns to DWORD
    - it combines those two byte arrays into a final bytearray
    - it calls DialogBoxIndirectParam() on that final bytearray, which actually runs the
        dialog; that dialog keeps the focus until it is terminated.

"""