#!python3

# Styles.py

from tkinter import ttk


''' ttk Style Definitions '''


def defineStyles(mainwindow):
    style = ttk.Style(mainwindow)
    style.theme_use('default')
    style.configure('.',
                    background='gray22',
                    foreground='gray80',
                    font='TkDefaultFont')

    style.configure('catdv.TFrame', background='gray22')

    style.configure('catdv.TNotebook',
                    background='gray22',
                    font='TkDefaultFont',
                    borderwidth=0)

    style.configure('catdv.TNotebook.Tab',
                    background='gray22',
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor='gray22',
                    highlightthickness=0,
                    highlightcolor='gray22',
                    padding='15 4 15 4')

    style.map('catdv.TNotebook.Tab',
              foreground=[('disabled', 'gray45'),
                          ('active', 'gray90'),
                          # ('!active', 'yellow'),
                          ('selected', 'gray80'),
                          ('!selected', 'gray45')],
              background=[('selected', 'gray30'),
                          ('!selected', 'gray12')],
              # highlightcolor=[('focus', 'DodgerBlue3'),
              #                 ('!focus', 'gray22'),
              #                 ('active', 'DodgerBlue3')],
              relief=[('pressed', 'flat'),
                      ('!pressed', 'flat')])

    style.configure('catdv.TLabel',
                    foreground='gray70',
                    background='gray22',
                    padding='4 5 4 5')
    style.map('catdv.TLabel',
              background=[('disabled', 'gray22')],
              foreground=[('disabled', 'gray50')])

    style.configure('blue.catdv.TLabel',
                    foreground='DodgerBlue1')

    ''' Re-structuring the 'default' theme button widget layout
    to match the button layout of the 'classic' theme '''

    classic_button_layout = [('Button.highlight', {'sticky': 'nswe', 'children': [
        ('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [
            ('Button.padding', {'sticky': 'nswe', 'children': [
                ('Button.label', {'sticky': 'nswe'})]})]})]})]
    style.layout('catdv.TButton', classic_button_layout)

    style.configure('catdv.TButton',
                    # foreground='gray80',
                    # background='gray22',
                    # focuscolor='red',
                    background='gray22',
                    focusthickness=0,
                    highlightthickness=0,
                    borderwidth=0,
                    padding='2 3 1 1',
                    relief='flat'
                    )
    style.map('catdv.TButton',
              foreground=[('disabled', 'gray40'),
                          ('pressed', 'gray80'),
                          ('active', 'gray80')],
              background=[('disabled', 'gray25'),
                          ('pressed', 'DodgerBlue3'),
                          ('!pressed', 'focus', 'DodgerBlue3'),
                          ('active', 'focus', 'gray22')],
              # highlightcolor=[('focus', 'DodgerBlue3'),
              #                 ('!focus', 'gray22'),
              #                 ('active', 'DodgerBlue3')],
              relief=[('pressed', 'flat'),
                      ('!pressed', 'flat')])

    style.configure('catdv.TCombobox',
                    # foreground='gray80',
                    fieldbackground='gray12',
                    highlightthickness=0,
                    borderwidth=0,
                    selectforeground='gray80',
                    selectbackground='DodgerBlue4',
                    selectborderwidth=0,
                    relief='flat',
                    padding='3')
    style.map('catdv.TCombobox',
              foreground=[('disabled', 'gray50'),
                          ('!disabled', 'gray80'),
                          ('readonly', 'gray80')],
              background=[('active', 'DodgerBlue3'),
                          ('!disabled', 'DodgerBlue4')],
              # selectbackground=[('readonly', '!focus', 'gray12')],
              fieldbackground=[('disabled', 'gray30'),
                               ('!disabled', 'gray12'),
                               ('readonly', 'gray12')])

    style.configure('TProgressbar',
                    troughcolor='gray80',
                    background='DodgerBlue3')
