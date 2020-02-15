#! python3

import tkinter as tk
from tkinter import ttk
import Styles


# class CheckBox(ttk.Checkbutton):
#     def __init__(self, parent, title):
#         super().__init__(parent)
#         self.checked = tk.BooleanVar()
#         print('parent:', parent)
#         print('title:', title)
#         self.configure(text=title)

class CheckBox(tk.Checkbutton):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.checked = tk.BooleanVar()
        # print('parent:', parent)
        # print('title:', title)
        # self.configure(text=title)

        self.configure(variable=self.checked,
                       #                text=title,
                       background='gray22',
                       #                foreground='DodgerBlue1',
                       #                # font='TkDefaultFont',
                       #                activebackground='gray22',  # n/a on mac
                       #                activeforeground='DodgerBlue1',  # n/a on mac
                       pady=5)


class CheckBoxLabel(ttk.Frame):
    '''
    Create a custom widget based on ttk.Frame, containing
    a tk.Checkbutton, which defaults to a checkmark on mac & windows,
    and a ttk.Label which can be styled as desired.
    '''

    def __init__(self, label):
        super().__init__()
        self.configure(borderwidth=2, relief='groove', padding='0 4 0 0')
        self.checkbox = CheckBox(self, '')
        self.checkbox.configure(pady=0)
        self.checkbox.grid(column=0, row=0)
        self.checked = self.checkbox.checked
        label = ttk.Label(self, text=label)
        label.configure(foreground='DodgerBlue1')
        label.grid(column=1, row=0)


root = tk.Tk()
Styles.defineStyles(root)
s = ttk.Style(root)
# s.theme_use('aqua')
# root.configure(width=200, height=100)
root.title("ttk style test")
# root.resizable(width=False, height=False)

# s.theme_use('default')
# print(s.layout('TLabelframe'))

# s.layout('cl.Tlabelframe', [('Labelframe.border', {'sticky': 'nswe', 'bordercolor': ''}
#                              )])

lf = ttk.Labelframe(root)
label_widget = CheckBoxLabel('Schedule')
lf.configure(width=200, height=100, padding='20 20 20 20',
             # text='labelframe test label',
             # relief='raised',
             labelwidget=label_widget,
             borderwidth=6)

print('\n\n--lf keys and values')
for k in lf.keys():
    print(k, ':', lf[k])

print(dir(lf))

print(label_widget.checked.get())


# cb = CheckBoxLabelWidget(lf, 'Here\'s a checkbox')

# s = ttk.Style(cb)
# s.theme_use('aqua')
# s.configure('TCheckbutton', foreground='DodgerBlue1',
#             padding='', indicatorrelief='', indicatormargin='')
# print('\n\n---TCheckbutton configured options')
# print(s.configure('TCheckbutton',))  # This shows all configured options
#
# print('\n\n--TCheckbutton layout')
# print(s.layout('TCheckbutton'))  # all elements of the layout, list of lists and tuples
#
# print('\n\n--Checkbutton.padding options')
# print(s.element_options('Checkbutton.padding'))  # tuple - all available padding options
#
# print('\n\n--Checkbutton.indicator options')
# print(s.element_options('Checkbutton.indicator'))  # tuple - all available indicator options
#
# print('\n\n--Checkbutton.focus options')
# print(s.element_options('Checkbutton.focus'))  # tuple - all available focus options
#
# print('\n\n--Checkbutton.label options')
# print(s.element_options('Checkbutton.label'))  # tuple - all available label options


# print('\n\n--cb keys and values')
# for k in cb.keys():
#     print(k, ':', cb[k])
# print(dir(cb))

lf.grid()
# cb.grid()

root.mainloop()
