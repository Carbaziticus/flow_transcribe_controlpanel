#!python3

# flow_transcribe_controlpanel.py
# Version 0.1.0
#  macOS

'''
After compiling this as Flow Transcribe Control Panel.app,
copy the flow_transcribe unix executable into it's bundle:
/Applications/Flow Transcribe/Flow Transcribe Control Panel.app/Contents/MacOS/
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import re
import os
import sys
import queue
# import threading
from datetime import datetime
import calendar
import logging
# import traceback
import shutil
# import zipfile
import subprocess
import requests
import plistlib
import SysInfo
import FileInfo
import CPio
import KeyMan
import Styles


print(SysInfo.system(), SysInfo.release())
print('Python {}'.format(sys.version))
print('Tcl', tk.Tcl().eval('info patchlevel'))


''' Evaluate License '''
auth = KeyMan.authentication()


''' Define regex patterns '''
nonint_chars2digits = re.compile(r"^[0-9]{1,2}$")
message_intsonly2digits = (("Enter only integers ", 'centered'),
                           ("0-99", ('centered', 'green')),)
nonint_chars5digits = re.compile(r"^[0-9]{1,5}$")
message_intsonly5digits = (("Enter only integers ", 'centered'),
                           ("0-99999", ('centered', 'green')),)
special_chars = re.compile(r"^((?![\&\'\*\^\`\$\?\;\"]).)*$")
message_nospecial = (("Avoid special characters in paths: ", 'centered'),
                     (r"& ' * ^ ` $ ? ; " + "\"", ('centered', 'yellow')),)
ascii_16_127 = re.compile(r"^[\x20-\x7F]+$")
message_asciionly = (("Enter only standard printable characters: ", 'centered'),
                     ("(ASCII 16-127)", ('centered', 'green')),)
license_format = re.compile(r"^([A-Z0-9]{4}-){7}[A-Za-z0-9]{4}$")
message_license = (("Enter 8 groups of 4 characters, caps and numbers", 'centered'),)
messageclear = (("", ''),)
# need ip address format


def build_default_targets(cp_obj):
    '''
     path_targets is a list of tuples (target file or dir, browse function)
     each to be passed to an instantance of PathEntryWithBrowseButton
    '''
    path_targets = []
    for option in cp_obj.options("Paths"):  # get each path from cp_obj
        path = cp_obj.get("Paths", option)
        exp = expand_wildcards(path)  # expand any wildcards in the path
        norm = os.path.normpath(exp)  # normalize the os.sep's
        if os.path.isfile(norm):
            browse_function = askopenfilename  # browse function for files
        else:
            browse_function = askdirectory  # browse function for directories
        base = os.path.basename(norm)  # get just the filename or final dirname
        path_targets.append((base, browse_function))  # append to list as a tuple
    return(path_targets)


def reset_settings_from_cp(cp_obj):
    '''
    load all user inputs from cp_obj
    '''
    for w in data_entry_widgets:
        w.load(cp_obj)


# test if the provided path exists, or if any sub-component of the path exists
def test_path(e_obj, p):  # p is a 2-tuple, initially (fullpath, '')
    if not os.path.exists(p[0]):
        p = os.path.split(p[0])  # p is now a 2-tuple from path.split (firstpart, lastcomponent)
        # insert 'red' tag for failed component
        e_obj.tag_add('red', '1.' + str(len(p[0])+1), 'end')
        e_obj.tag_configure('red', foreground='red')
        e_obj.configure(highlightcolor='red')
        # recursing backwards to the parent component until a valid sub-path is found
        test_path(e_obj, p)


def expand_wildcards(path):  # expands wildcard patterns in path
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    if path != "":  # normpath converts empty string to '.', which we don't want
        path = os.path.normpath(path)  # normalize the os.sep's
    return(path)


# def create_schedule(load_unload):  # mac
#     '''
#     create macos launchagent plist
#     '''
    # pl = dict()
    # label = 'com.langrallconsulting.flow_transcribe'
    # pl['Label'] = label
    # transcribe_app_path = os.path.join(FileInfo.currentDir(), 'flow_transcribe.app')
    # if cp_config.get('Preferences', 'debug_messages_on') == 'True':
    #     debug = 'On'
    # else:
    #     debug = 'Off'
    # pl['ProgramArguments'] = ['/usr/bin/open', '-W', transcribe_app_path, '--args', '-d', debug]
    #
    # if cp_config.get('Schedule', 'run_minutes_on') == 'True':
    #     pl['StartInterval'] = cp_config.get('Schedule', 'run_minutes')
    # elif cp_config.get('Schedule', 'run_days_on') == 'True':
    #     run_time = '{}{}'.format(
    #         cp_config.get('Schedule', 'run_days_time'),
    #         cp_config.get('Schedule', 'run_days_ampm'))
    #     run_time = datetime.strptime(str(run_time), '%I:%M%p').strftime('%H:%M')
    #     hour = run_time.split(':')[0]
    #     minute = run_time.split(':')[1]
    #     day = cp_config.get('Schedule', 'run_days_day')
    #     if day == 'Day':
    #         pl['StartCalendarInterval'] = dict(Hour=hour, Minute=minute)
    #     else:
    #         pl['StartCalendarInterval'] = dict(Day=day, Hour=hour, Minute=minute)
    #
    # user_launchagents_dir = os.path.join(os.path.expanduser('~'), 'Library', 'LaunchAgents')
    # plist_name = '{}.plist'.format(label)
    # service_path = os.path.join(user_launchagents_dir, plist_name)
    #
    # # Execute service unload command (in case this plist has previously been loaded)
    # launchctlCmd = ['/bin/launchctl', 'unload', path]  # removed -w
    # p = subprocess.Popen(launchctlCmd, shell=False, bufsize=1,
    #                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = p.communicate()
    # print('unload:', stdout)
    # print('unload:', stderr)
    #
    # # wirite the new plist into the LaunchAgents directory
    # with open(service_path, 'wb') as fp:
    #     # with open('com.langrallconsulting.flow_transcribe.plist', 'wb') as fp:
    #     plistlib.dump(pl, fp)
    #
    # # Execute service load command
    # launchctlCmd = ['/bin/launchctl', 'load', service_path]  # removed -w
    # p = subprocess.Popen(launchctlCmd, shell=False, bufsize=1,
    #                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = p.communicate()
    # print('load:', stdout)
    # print('load:', stderr)
    #
    # # execute the service start command
    # launchctlCmd = ['/bin/launchctl', 'start', label]
    # p = subprocess.Popen(launchctlCmd, shell=False, bufsize=1,
    #                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = p.communicate()
    # print('start', stdout)
    # print('start', stderr)


def saveall(filepath):  # filepath is either configfile or defaultsfile
    # #  should expand wildcards and test paths with a msgbox if error
    # #  how to handle saving invalid paths (leave blank?) or ints (set to 0 or default?)
    # if filepath == FileInfo.defaultsPath():
    #     response = messagebox.askyesno("Overwrite Defaults File",
    #                                    "Do you really want to overwrite\n"
    #                                    "'catdv_backup_defaults.cfg'?",
    #                                    default='no',
    #                                    icon='warning')
    #     if response is False:
    #         return
    #     else:
    #         message = (
    #             ("Saved current settings to 'catdv_backup_defaults.cfg'", 'centered'))
    # else:
    message = (("Saved current settings", 'centered'))
    # update cp_config with current settings and save to disk
    for w in data_entry_widgets:
        cp_config.set(w.cp_section, w.cp_key, str(w.report()))
    #  should wrap this disk write in a try block
    CPio.writeCP(cp_config, filepath)
    t_status.setmessage(message)
    plist = Plist()
    if plist.launchctl_list() == 0:  # an existing plist is already loaded
        print('unloading existing plist:', plist.label)
        plist.launchctl_unload()
    if cp_config.get('Schedule', 'schedule_on') == 'True':
        plist.write_plist()
        plist.launchctl_load()
    elif cp_config.get('Schedule', 'schedule_on') == 'False':
        plist.delete_plist()
        # plist.launchctl_start()  # immediaqte mode for testing


def conditional_quit():
    # saved = no difference between current widget value and cp_config
    saved = True
    for w in data_entry_widgets:
        if str(w.report()) != cp_config.get(w.cp_section, w.cp_key):
            saved = False
            break
    if saved is False:
        response = messagebox.askyesno("Unsaved Changes",
                                       "You have unsaved changes.  Quit anyway?",
                                       default='no',
                                       icon='warning')
        if response is True:
            sys.exit(0)
    else:
        sys.exit(0)


class Plist():
    '''
    manage task scheduling via macos launchagent plist
    '''

    def __init__(self):
        self.label = 'com.langrallconsulting.flow_transcribe'  # hard-coded plist label
        self.transcribe_app_path = os.path.join(
            FileInfo.appDir(), 'flow_transcribe')  # This is NOT the bundle dir (sys.MEIPASS)
        print('self.transcribe_app_path: {}'.format(self.transcribe_app_path))
        # sys.exit(0)
        self.launchagents_dir = os.path.join(os.path.expanduser('~'), 'Library', 'LaunchAgents')
        self.plist_name = '{}.plist'.format(self.label)
        self.service_path = os.path.join(self.launchagents_dir, self.plist_name)
        self.create_plist()

    def create_plist(self):
        self.pl = dict()
        self.pl['Label'] = self.label
        if cp_config.get('Preferences', 'debug_messages_on') == 'True':
            self.debug = 'On'
        else:
            self.debug = 'Off'
        self.pl['ProgramArguments'] = [self.transcribe_app_path,  # was '/usr/bin/open', '-W', '--args',
                                       '-d', self.debug]
        # '&>', '/dev/null']  # added output redirection to null
        # print(self.pl['ProgramArguments'])
        # sys.exit(0)
        if cp_config.get('Schedule', 'run_minutes_on') == 'True':
            self.pl['StartInterval'] = int(cp_config.get('Schedule', 'run_minutes')) * 60
        elif cp_config.get('Schedule', 'run_days_on') == 'True':
            self.run_time = '{}{}'.format(
                cp_config.get('Schedule', 'run_days_time'),
                cp_config.get('Schedule', 'run_days_ampm'))
            self.run_time = datetime.strptime(str(self.run_time), '%I:%M%p').strftime('%H:%M')
            self.hour = int(self.run_time.split(':')[0])
            self.minute = int(self.run_time.split(':')[1])
            self.day = cp_config.get('Schedule', 'run_days_day')
            if self.day == 'Day':
                self.pl['StartCalendarInterval'] = dict(Hour=self.hour, Minute=self.minute)
            else:
                self.pl['StartCalendarInterval'] = dict(
                    Day=self.day, Hour=self.hour, Minute=self.minute)

    def write_plist(self):
        # wirite the new plist into the LaunchAgents directory
        with open(self.service_path, 'wb') as fp:
            # with open('com.langrallconsulting.flow_transcribe.plist', 'wb') as fp:
            plistlib.dump(self.pl, fp)

    def delete_plist(self):
        # delete flow_transcribe.plist
        rmCmd = ['/bin/rm', self.service_path]
        p = subprocess.Popen(rmCmd, shell=False, bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print('rm:', stdout)
        print('rm:', stderr)

    def launchctl_list(self):
        # check if a flow_transcribe.plist is already loaded
        launchctlCmd = ['/bin/launchctl', 'list']
        p1 = subprocess.Popen(launchctlCmd, stdout=subprocess.PIPE)
        grepCmd = ['/usr/bin/grep', self.label]
        p2 = subprocess.Popen(grepCmd, stdin=p1.stdout,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p1.stdout.close()
        stdout, stderr = p2.communicate()
        print('list:', stdout)
        print('list:', stderr)
        if self.label in str(stdout):
            return(0)
        else:
            return(1)

    def launchctl_load(self):
        # Execute service load command
        launchctlCmd = ['/bin/launchctl', 'load', self.service_path]  # removed -w
        p = subprocess.Popen(launchctlCmd, shell=False, bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print('load:', stdout)
        print('load:', stderr)

    def launchctl_unload(self):
        # Execute service unload command
        launchctlCmd = ['/bin/launchctl', 'unload', self.service_path]  # removed -w
        p = subprocess.Popen(launchctlCmd, shell=False, bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print('unload:', stdout)
        print('unload:', stderr)

    def launchctl_start(self):
        # execute the service start command
        launchctlCmd = ['/bin/launchctl', 'start', self.label]
        p = subprocess.Popen(launchctlCmd, shell=False, bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print('start', stdout)
        print('start', stderr)

        # def launchctl_stop(self): # may be unnecessary


''' Widget Class and Function Definitions '''


def create_label(parent, title, style):
    label = ttk.Label(parent, text=title, style=style)
    return(label)


class CheckBox(tk.Checkbutton):
    def __init__(self, parent, title, cp_section, cp_key):
        super().__init__(parent)
        self.cp_section = cp_section
        self.cp_key = cp_key
        self.checked = tk.BooleanVar()

        self.configure(variable=self.checked,
                       text=title,
                       background='gray22',
                       foreground='DodgerBlue1',
                       # font='TkDefaultFont',
                       activebackground='gray22',  # n/a on mac
                       activeforeground='DodgerBlue1',  # n/a on mac
                       pady=5)

    def load(self, cp_object):  # set value of checkbox from cp_object
        self.checked.set(cp_object.get(self.cp_section, self.cp_key))

    def report(self):  # report current value of checkbox
        return(self.checked.get())

    def toggle_off(self):
        # if this checkbox is currently checked, uncheck it
        if self.checked:
            self.checked.set(False)


class CheckBoxWithLabel(ttk.Frame):
    '''
    Create a custom widget based on ttk.Frame, containing
    a tk.Checkbutton, which defaults to a checkmark on mac & windows,
    and a ttk.Label which can be styled as desired.  Intended for use
    as a label frame labelwidget.
    '''

    def __init__(self, label, cp_section, cp_key):
        super().__init__()
        self.configure(borderwidth=0, relief='groove', padding='0 4 0 0')
        self.cp_section = cp_section
        self.cp_key = cp_key
        self.checkbox = CheckBox(self, '', cp_section, cp_key)  # label is emptry
        self.checkbox.configure(pady=0)
        self.checkbox.grid(column=0, row=0)
        label = ttk.Label(self, text=label)
        label.configure(foreground='DodgerBlue1')
        label.grid(column=1, row=0)


class NoteBookCatdv(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(padding='10 10 10 10',
                    style='catdv.TNotebook')
        self.grid(column=0, row=0, ipady=5)
        self.t_flow = ttk.Frame(style='TFrame')
        self.t_speechmatics = ttk.Frame(style='TFrame')
        self.t_transcribe = ttk.Frame(style='TFrame')
        self.t_license = ttk.Frame(style='TFrame')
        self.t_about = ttk.Frame(style='TFrame')
        self.add(self.t_flow, text="Flow")
        self.add(self.t_speechmatics, text="Speechmatics")
        self.add(self.t_transcribe, text="Transcribe")
        self.add(self.t_license, text="License")
        self.add(self.t_about, text="About")
        self.imagepath = os.path.join(FileInfo.currentDir(), "images")
        self.ok_png = tk.PhotoImage(
            file=os.path.join(self.imagepath, "checkmark-12.gif"))
        self.warn_png = tk.PhotoImage(
            file=os.path.join(self.imagepath, "warning-16.gif"))

        def about_page():  # build the "About" page content
            logopath = os.path.join(self.imagepath, "AsaPro_logo_no_alpha_small.gif")
            logoimage = tk.PhotoImage(file=logopath)
            about_logo = ttk.Label(self.t_about, image=logoimage, padding='0 40 0 25')
            about_logo.image = logoimage
            about_logo.grid(row=0, column=0)
            self.t_about.columnconfigure(0, weight=1)
            largelabelfont = ('TkDefaultFont', 16, 'bold')
            about_app = create_label(
                self.t_about, "Flow Transcribe Control Panel", style='catdv.TLabel')
            about_app.configure(font=largelabelfont)
            about_app.grid()
            about_version = create_label(self.t_about, "Version 1.0", style='catdv.TLabel')
            about_version.grid()
            about_copyright = create_label(
                self.t_about, "Copyright (C) 2019 Langrall Consulting Inc.", style='catdv.TLabel')
            about_copyright.grid()
            # smalllabelfont = ('TkDefaultFont', 11, 'normal')
            about_legal = create_label(
                self.t_about, "Unauthorized duplication, distribution or reverse engineering\
                 of this copyrighted software is prohibited by law.", style='catdv.TLabel')
            about_legal.configure(wraplength=400, justify='center',
                                  foreground='gray60', padding='0 25 0 0')
            about_legal.grid()

        def update_when_tab_changed(event):
            dsp.event_handler(event)

        about_page()

        self.bind("<<NotebookTabChanged>>", update_when_tab_changed)

    # add an image to a notebook tab
    def tab_image(self, tab, *image):
        # if image is not provided, the current image turns off
        self.tab(tab, image=image, compound=tk.RIGHT)


class LabelFrameCatdv(ttk.LabelFrame):
    def __init__(self, parent, title, row):
        super().__init__(parent)

        self.labelWidget = create_label(parent, title, 'blue.catdv.TLabel')
        self.config(height=100,
                    width=90,
                    borderwidth=1,
                    relief='groove',
                    labelwidget=self.labelWidget)
        self.grid(row=row, column=0, columnspan=4, padx=12, pady=2, ipadx=10, sticky='EW')


class LabelFrameWithCheckbox(LabelFrameCatdv):
    def __init__(self, parent, title, row, cp_section, cp_key):
        super().__init__(parent, '', row)

        self.checkboxlabel = CheckBoxWithLabel(title, cp_section, cp_key)
        self.checkbox = self.checkboxlabel.checkbox
        self.checkbox.config(command=self.toggle_scheduling)
        self.config(labelwidget=self.checkboxlabel)

    def toggle_scheduling(self):
        if self.checkbox.checked.get() is False:
            for w in self.winfo_children():
                w.configure(state='disabled')
        elif self.checkbox.checked.get() is True:
            for w in self.winfo_children():
                w.configure(state='normal')
        # self.checkbox.configure(state='normal')


class StatusMessageBox(tk.Text):
    def __init__(self, parent):
        super().__init__(parent)
        # self.config(height=1, width=90)
        self.config(height=1,
                    width=70,
                    background='gray22',
                    foreground='gray80',
                    highlightthickness=0,
                    relief='flat')
        # self.tag_add('centered', 1.0, 'end')
        # should investigate redundant tag configuration in other modules
        self.tag_configure('centered', justify='center')
        # self.tag_add('green', 1.0, 'end')
        self.tag_configure('green', foreground='Green2')
        # self.tag_add('red', 1.0, 'end')
        self.tag_configure('red', foreground='red')
        # self.tag_add('yellow', 1.0, 'end')
        self.tag_configure('yellow', foreground='yellow')
        self.tag_configure('underline', underline=True)

    def setmessage(self, *arg):
        # arg is a list of tuples in the form (text, tag)
        self.config(state='normal')
        self.delete(1.0, 'end')
        for text, tag in arg:
            self.insert('end', text, tag)
        self.config(state='disabled')


class LicenseStatusMessageBox(StatusMessageBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(height=4,
                    selectbackground='DeepSkyBlue3',
                    selectforeground='white',
                    )
        # allow the message box to take focus when clicked
        # enables text selection and copying, even though entry is disabled
        self.bind('<ButtonPress>', lambda event: self.focus_set())


class EntryBox(tk.Text):
    ''' Includes a formatted ttk label '''
    ''' Subclass of the standard tk Text widget '''
    ''' Styling needs to be set explicitly here '''

    def __init__(self, parent, title, width, row, labelstyle, regex, validmessage, cp_section, cp_key):
        self.p = regex
        self.m = validmessage
        self.cp_section = cp_section
        self.cp_key = cp_key
        super().__init__(parent)

        label = ttk.Label(parent, text=title, style=labelstyle)
        label.grid(row=row, column=0, sticky='W')

        self.configure(
            background='gray12',
            borderwidth=0,
            highlightthickness=3,
            selectbackground='DeepSkyBlue3',
            inactiveselectbackground='DeepSkyBlue3',
            foreground='gray80',
            insertbackground='white',
            insertwidth=2,
            highlightcolor='DodgerBlue3',  # 'red' for error
            highlightbackground='gray12',
            selectborderwidth=0,
            relief='flat',
            height=1,
            width=width,
            undo=True)
        self.grid(row=row, column=1, sticky='W',)
        self.bind("<KeyRelease>", self.validate)

    def validate(self, event=None):  # or self, name, index, mode
        if not self.p.search(self.get('1.0', 'end-1c')):
            t_status.setmessage(*self.m)
            if self.m == message_intsonly2digits:
                self.configure(highlightcolor='red')
                self.tag_add('red', self.index('insert - 1 chars'))
                self.tag_configure('red', foreground='red')
            if self.m == message_intsonly5digits:
                self.configure(highlightcolor='red')
                self.tag_add('red', self.index('insert - 1 chars'))
                self.tag_configure('red', foreground='red')
            if self.m == message_nospecial:
                self.configure(highlightcolor='yellow')
                self.tag_add('yellow', self.index('insert - 1 chars'))
                self.tag_configure('yellow', foreground='yellow')
            if self.m == message_asciionly:
                self.configure(highlightcolor='red')
                self.tag_add('red', self.index('insert - 1 chars'))
                self.tag_configure('red', foreground='red')
            # no special tag colors for message_licensie
        else:
            t_status.setmessage(*messageclear)
            self.configure(highlightcolor='DodgerBlue3')

    def load(self, cp_object):  # set value of entrybox from cp_object
        self.delete('1.0', 'end-1c')
        self.insert('1.0', cp_object.get(self.cp_section, self.cp_key))

    def report(self):  # report current value of entrybox
        return(self.get('1.0', 'end-1c'))


class ButtonCatdv(ttk.Button):
    ''' Highly customized ttk buttons with images and mouse event bindings '''

    def __init__(self, parent, title, row, column, hint):
        super().__init__(parent)

        button_png = tk.PhotoImage(
            file=os.path.join(FileInfo.currentDir(), "images", "Button16small.gif"))
        button_darkblue_png = tk.PhotoImage(
            file=os.path.join(FileInfo.currentDir(), "images", "Button16smalldarkblue.gif"))
        button_lightblue_png = tk.PhotoImage(
            file=os.path.join(FileInfo.currentDir(), "images", "Button16smallblue.gif"))
        button_yellow_png = tk.PhotoImage(
            file=os.path.join(FileInfo.currentDir(), "images", "Button16smallyellow.gif"))

        self.configure(
            text=title,
            image=button_png,
            compound='center',
            style='catdv.TButton')
        self.grid(column=column, row=row, padx=(12, 0), pady=2)
        self['state'] = 'enabled'  # all buttons start in the enabled state

        def update_when_mouse_enters_button(event):
            if self['state'] == 'enabled':
                self.configure(image=button_darkblue_png)
                t_status.setmessage(*hint)

        def update_when_mouse_leaves_button(event):
            if self['state'] == 'enabled':
                self.configure(image=button_png)
                m = messageclear
                t_status.setmessage(*m)

        def update_when_button_pressed(event):
            if self['state'] == 'enabled':
                if (event.state == 16 and SysInfo.system() == 'Darwin') or \
                        (event.state == 12 and SysInfo.system() == 'Windows'):  # specify mac/windows
                    self.configure(image=button_yellow_png)
                else:
                    self.configure(image=button_lightblue_png)
                dsp.event_handler(event)

        def update_when_button_released(event):
            if self['state'] == 'enabled':
                self.configure(image=button_darkblue_png)

        self.bind('<Enter>', update_when_mouse_enters_button)
        self.bind('<Leave>', update_when_mouse_leaves_button)
        self.bind('<ButtonPress>', update_when_button_pressed)
        self.bind('<ButtonRelease>', update_when_button_released)


class ButtonPasteCatdv(ButtonCatdv):
    ''' Paste Button for quick entry of license registration '''
    ''' Parses the registration text from the clipboard, '''
    ''' fills two text entry boxes with pasted text'''
    ''' and attempts to authenticate '''

    def __init__(self, parent, title, row, column, hint):
        super().__init__(parent, title, row, column, hint)

        def paste():  # get clipboard data
            p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
            # retcode = p.wait()  # what does this do?
            clipboard = p.stdout.read()
            if clipboard:
                textlist = clipboard.decode('UTF8').split('\n')
                if len(textlist) == 2:
                    registered = re.sub('^(.*[:|=]\ )', '', textlist[0])
                    license = re.sub('^(.*[:|=]\ )', '', textlist[1])
                    auth.license_key = license
                    auth.registered_to = registered
                    auth.authenticate()
                    dsp.authentication_refresh()
        self.configure(command=paste)


class ButtonApplyCatdv(ButtonCatdv):
    '''
    Apply Button for use with manual entry of license registration
    and attempts to authenticate
    '''

    def __init__(self, parent, title, row, column, hint):
        super().__init__(parent, title, row, column, hint)

        def apply():  # attempt to authenticate based on user-entered license
            auth.license_key = e_license.get('1.0', 'end-1c')
            auth.registered_to = e_registered.get('1.0', 'end-1c')
            auth.authenticate()
            dsp.authentication_refresh()

        self.configure(command=apply)


class PathEntryWithBrowseButton(EntryBox):
    def __init__(self, parent, title, width, row, labelstyle, buttontext, target, cp_section, cp_key):
        super().__init__(parent, title, width, row, labelstyle,
                         special_chars, message_nospecial, cp_section, cp_key)

        self.cp_section = cp_section
        self.cp_key = cp_key
        self.target = target[0]

        def browse():
            if SysInfo.system() == 'Darwin':
                t_status.setmessage(
                    ("Press ", ('centered')),
                    # specify mac/windows (how to reveal hidden files on windows?)
                    ("Shift+Cmd+.", ('centered', 'green')),
                    (" to view hidden files and folders", ('centered')))
            # elif system == 'Windows':
            #     t_status.setmessage(
            #         ("Press ", ('centered')),
            #         # specify mac/windows (how to reveal hidden files on windows?)
            #         ("Shift+Cmd+.", ('centered', 'green')),
            #         (" to view hidden files and folders", ('centered')))
            root.update()
            path = os.path.dirname(self.get(1.0, 'end-1c'))
            path = expand_wildcards(path)
            while path != "/":  # specify mac/windows
                if os.path.exists(path):
                    break
                else:
                    path = os.path.dirname(path)
            prompt = "Locate  " + self.target
            selection = target[1](initialdir=path, title=prompt)
            if selection:
                selection = os.path.normpath(selection)  # converts "/" to local os.sep
                self.delete('1.0', 'end-1c')
                self.insert('1.0', selection)
        self.hint = messageclear
        b = ButtonCatdv(parent, buttontext, row, 2, self.hint)
        b.configure(command=browse)

        self.bind("<Tab>", self.autocomplete)

    def autocomplete(self, event=None):  # autocompletes path fragment if result is valid path
        path = self.get(1.0, 'end-1c')
        insertion_index = self.index('insert')
        s0 = int(self.search(os.sep, insertion_index,
                             backwards=True).split('.')[1])  # previous os.sep index
        if s0 > int(insertion_index.split('.')[1]):
            s0 = 0  # handle boundary conditions (the .search method wraps around)
        s1 = int(self.search(os.sep, insertion_index,
                             forwards=True).split('.')[1])  # next os.sep index
        if s1 < int(insertion_index.split('.')[1]):
            s1 = len(path)  # handle boundary conditions (the .search method wraps around)
        head = path[0:s0+1]
        fragment = path[s0+1:int(insertion_index.split('.')[1])]
        tail = path[s1:]
        head = expand_wildcards(head)
        tail = expand_wildcards(tail)
        if os.path.exists(head):
            for x in os.listdir(head):
                if x.startswith(fragment):
                    newtail = x + tail
                    test = os.path.join(head, newtail)
                    if os.path.exists(test):  # validate autocomplete path
                        self.delete(1.0, 'end-1c')
                        self.insert(1.0, test)
                        break  # prevent further matching
        return('break')  # prevents the normal TAB event propagation


class ComboBox(ttk.Combobox):

    def __init__(self, parent, width, values, row, column, cp_section, cp_key):
        super().__init__(parent)
    # removed valueindex,

        self.cp_section = cp_section
        self.cp_key = cp_key
        self.configure(width=width,
                       values=values,
                       style='catdv.TCombobox',
                       state='readonly')
        ''' Adding *TCombobox*Listbox items to the tkinter option database
        allows us to set colors in the dropdown Listbox'''
        self.option_add('*TCombobox*Listbox.background', 'gray12')
        self.option_add('*TCombobox*Listbox.foreground', 'gray80')
        self.option_add('*TCombobox*Listbox.selectBackground', 'DeepSkyBlue3')
        self.option_add('*TCombobox*Listbox.selectForeground', 'gray80')
    # combobox.option_add('*TCombobox*troughcolor', 'red')
    # combobox.current(valueindex)
        self.grid(row=row, column=column, sticky='W')

    def load(self, cp_object):  # set value of conbobox from cp_object
        self.set(cp_object.get(self.cp_section, self.cp_key))

    def report(self):  # report current value of combobox
        return(self.get())


class DisplayController():
    ''' handle UI events and refresh display on authentication '''
    # def __init__(self):

    def authentication_refresh(self):  # set notebook state based on license status
        if not auth.authenticated:  # disable the Settings Tab
            n_book.tab(0, state='disabled')  # Flow tab
            n_book.tab(1, state='disabled')  # Speechmatics tab
            n_book.tab(2, state='disabled')  # Transcribe tab
            n_book.select(3)  # if unlicensed, select the License Tab
        else:
            n_book.tab(0, state='normal')  # enable the Flow Tab
            n_book.tab(1, state='normal')  # enable the Speechmatics Tab
            n_book.tab(2, state='normal')  # enable the Transcribe Tab
            #  refresh the licensing information display
            e_registered.delete('1.0', 'end-1c')
            e_registered.insert('1.0', auth.registered_to)
            e_license.delete('1.0', 'end-1c')
            e_license.insert('1.0', auth.license_key)
        self.license_message_refresh()

    def license_message_refresh(self):
        if auth.authenticated:
            message_license = (("Licensed.\nThank you for registering Flow Transcribe.", ''),)
            message_thanks = (("Thank you for registering!", 'centered'),)
            if (n_book.index(n_book.select()) == 1):  # tab 1 (License) selected
                t_status.setmessage(*message_thanks)
        else:
            message_license = (
                ("Transcribe Control Panel is not currently licensed on this machine.\n", ''),
                ("To obtain a license, email your installation ID ", ''),
                (auth.installationid, ('', 'green')),
                ("\nto ", ''),
                ("support@asapro-line.com", ('', 'underline'))
            )
        t_licstatus.setmessage(*message_license)

    def event_handler(self, event):
        ''' Event listener '''
        if event.widget == n_book:
            if (n_book.index(n_book.select()) == 0):  # tab 0 Flow selected
                b_reset['state'] = 'enabled'
                b_test['state'] = 'enabled'
                b_run['state'] = 'enabled'
                b_save['state'] = 'enabled'
                b_quit['state'] = 'enabled'
            elif (n_book.index(n_book.select()) == 1):  # tab 1 Speechmatics selected
                b_reset['state'] = 'enabled'
                b_test['state'] = 'enabled'
                b_run['state'] = 'enabled'
                b_save['state'] = 'enabled'
                b_quit['state'] = 'enabled'
            elif (n_book.index(n_book.select()) == 2):  # tab 2 Transcribe selected
                b_reset['state'] = 'enabled'
                b_test['state'] = 'enabled'
                b_run['state'] = 'enabled'
                b_save['state'] = 'enabled'
                b_quit['state'] = 'enabled'
            elif n_book.index(n_book.select()) == 3:  # tab 3 License selected
                b_reset['state'] = 'disabled'
                b_test['state'] = 'disabled'
                b_run['state'] = 'disabled'
                b_save['state'] = 'disabled'
                b_quit['state'] = 'enabled'
                lf_licensestatus.focus_set()  # avoid accidental typing in the registration boxes
            elif n_book.index(n_book.select()) == 4:  # tab 4 About selected
                b_reset['state'] = 'disabled'
                b_test['state'] = 'disabled'
                b_run['state'] = 'disabled'
                b_save['state'] = 'disabled'
                b_quit['state'] = 'enabled'
        if event.widget == b_reset:
            if (event.state == 16) and (SysInfo.system() == 'Darwin') or \
                    (event.state == 12) and (SysInfo.system() == 'Windows'):  # specify mac/windows
                reset_settings_from_cp(cp_default)  # reload defaults from disk
                message = ("Reloaded defaults.", 'centered')
            else:
                reset_settings_from_cp(cp_config)  # reload config from disk
                message = ("Changes undone.", 'centered')
            for t in range(4):  # clear all tab images
                n_book.tab_image(t, '')
            t_status.setmessage(message)  # clear status message
        if event.widget == b_test:
            ''' test the Flow Server API connection with username & password '''
            try:
                response = requests.get('https://{}:{}/users'.format(
                    e_flowserver.report(), '12154'),  # hard-coded api port 12154
                    auth=(
                    e_flowuser.report(),
                    e_flowpasswd.report()),
                    verify=False)
                if 'Unauthorised' in response.text:
                    raise requests.exceptions.RequestException(response.text)
            except Exception as err:
                print(err)
                n_book.tab_image(n_book.t_flow, n_book.warn_png)
            else:
                n_book.tab_image(n_book.t_flow, n_book.ok_png)

            ''' test the Speechmatics API connection with user & token '''
            base_url = 'https://api.speechmatics.com/v1.0'
            # print('base_url:', base_url)
            user = e_speechmaticsuser.report()
            # print('user:', user)
            token = e_speechmaticstoken.report()
            # print('token:', token)
            lang = c_speechmaticslanguage.report()
            # print('lang:', lang)
            params = {'auth_token': token}
            # data = {'model': lang}
            try:
                response = requests.get('{}/user/{}'.format(base_url, user),
                                        params=params, verify=True)
                if 'Invalid' in response.text or '404' in response.text:
                    raise requests.exceptions.RequestException(response.text)
            except Exception as err:
                print(err)
                n_book.tab_image(n_book.t_speechmatics, n_book.warn_png)
            else:
                n_book.tab_image(n_book.t_speechmatics, n_book.ok_png)

            ''' test paths '''
            tests, warnings, errors = 0, 0, 0
            # warn_text = " had warnnings"
            for e in paths_entries:
                expanded = expand_wildcards(e.get('1.0', 'end-1c'))
                e.delete('1.0', 'end')
                e.insert('1.0', expanded)  # insert result of expansion
                test_path(e, (e.get('1.0', 'end-1c'), ''))
                tests += 1
                if e.tag_ranges('red'):  # test_path() marks invalid path components RED
                    errors += 1
                elif os.path.basename(expanded) != e.target:
                    warnings += 1
                    # warn_text = warn_text + " (unexpected name)"
                    index = e.search(os.path.basename(expanded), 'end-1c', backwards=True)
                    e.tag_add('yellow', index, 'end-1c')
                    e.tag_configure('yellow', foreground='yellow')
                    e.configure(highlightcolor='yellow')
            # message = (str(tests) + " paths tested. " + str(errors) + " had errors; " + str(warnings) +
            #            warn_text + ".",  'centered')
            # t_status.setmessage(message)
            if warnings or errors:
                n_book.tab_image(n_book.t_transcribe, n_book.warn_png)
            else:
                n_book.tab_image(n_book.t_transcribe, n_book.ok_png)
        # if event.widget == b_backupnow:
        #     saveall(FileInfo.configPath())  # save current settings
        #     backup_gui = BackupGUI()
        if event.widget == b_save:
            # if event.state == 16:  # ALT + ButtonPress
            #     root.update()
            #     saveall(FileInfo.defaultsPath())
            # else:
            saveall(FileInfo.configPath())
        if event.widget == b_quit:
            conditional_quit()


''' Initialize the tkinter window '''

root = tk.Tk()
root.title('Flow Transcribe Control Panel')
root.resizable(width=False, height=False)
Styles.defineStyles(root)


''' Read The Defaults File From Disk '''
# assert os.path.exists(FileInfo.defaultsPath())
cp_default = CPio.readCP(FileInfo.defaultsPath())  # read the defaults file from disk

browse_goals = build_default_targets(cp_default)

''' Instantiate Widgets '''

''' Frames '''
mainframe = ttk.Frame(root, padding='0 0 0 0', style='catdv.TFrame')
mainframe.pack(expand=tk.YES, fill=tk.BOTH)

buttonframe = ttk.Frame(mainframe, style='catdv.TFrame', padding='0 5 0 0')
# specify padding mac/windows (55 10 0 0)  probably font-dependant
buttonframe.grid(column=0, row=4)


''' Notebook '''
n_book = NoteBookCatdv(mainframe)
# n_book.tab_image(n_book.t_speechmatics, n_book.ok_png)
# n_book.tab_image(n_book.t_flow, n_book.warn_png)


''' Label Frames '''
lf_connection = LabelFrameCatdv(n_book.t_flow, 'Connection', 0)
lf_preferences = LabelFrameCatdv(n_book.t_speechmatics, 'Options', 1)
lf_paths = LabelFrameCatdv(n_book.t_transcribe, 'Paths', 2)
lf_schedule = LabelFrameWithCheckbox(n_book.t_transcribe, 'Schedule', 3, 'Schedule', 'schedule_on')
lf_licensestatus = LabelFrameCatdv(n_book.t_license, 'Status', 0)
lf_licenseinfo = LabelFrameCatdv(n_book.t_license, 'Licensing Information', 1)

# initialize a list of all the data entry widgets: textboxes, comboboxes and checkboxes
data_entry_widgets = []

'''
Flow Tab Connection Group: Entryboxes with Labels
'''

e_flowserver = EntryBox(lf_connection, 'Flow Database Server IP Address:', 20,
                        0, 'catdv.TLabel', ascii_16_127, message_asciionly, 'Connection', 'flow_server')
data_entry_widgets.append(e_flowserver)


# e_flowapiport = EntryBox(lf_connection, 'Flow Database Server API Port:', 20,
#                          1, 'catdv.TLabel', nonint_chars5digits, message_intsonly5digits, 'Connection', 'flow_api_port')
# data_entry_widgets.append(e_flowapiport)


e_flowuser = EntryBox(lf_connection, 'Flow User:', 20,
                      2, 'catdv.TLabel', ascii_16_127, message_asciionly, 'Connection', 'flow_user')
data_entry_widgets.append(e_flowuser)


e_flowpasswd = EntryBox(lf_connection, 'Flow Password:', 20,
                        3, 'catdv.TLabel', ascii_16_127, message_asciionly, 'Connection', 'flow_passwd')
data_entry_widgets.append(e_flowpasswd)


'''
Transcribe Tab Paths Group: Entryboxes with Labels and Browse Buttons
'''
paths_entries = []  # list of path widgets to be used in "Test Paths"

e_tempdir = PathEntryWithBrowseButton(lf_paths, 'Temp Directory:', 55, 0,
                                      'catdv.TLabel', "Browse...", browse_goals[0], 'Paths', 'temp_dir')
paths_entries.append(e_tempdir)
data_entry_widgets.append(e_tempdir)

e_logdir = PathEntryWithBrowseButton(lf_paths, 'Log Directory:', 55,
                                     1, 'catdv.TLabel', "Browse...", browse_goals[1], 'Paths', 'log_dir')
paths_entries.append(e_logdir)
data_entry_widgets.append(e_logdir)

# e_smbmountpointdir = PathEntryWithBrowseButton(lf_paths, 'SMB Mountpoint:',  55,
#                                                2, 'catdv.TLabel', "Browse...", browse_goals[2], 'Paths', 'smbmountpoint_dir')
# paths_entries.append(e_smbmountpointdir)
# data_entry_widgets.append(e_smbmountpointdir)


'''
Speechmatics Tab Options Group: Entryboxes and Checkboxes
'''

e_speechmaticsuser = EntryBox(lf_preferences, 'Speechmatics User:', 8,
                              0, 'catdv.TLabel', nonint_chars5digits, message_intsonly5digits,
                              'Preferences', 'speechmatics_user')
data_entry_widgets.append(e_speechmaticsuser)

e_speechmaticstoken = EntryBox(lf_preferences, 'Speechmatics Token:', 55,
                               1, 'catdv.TLabel', ascii_16_127, message_asciionly,
                               'Preferences', 'speechmatics_token')
data_entry_widgets.append(e_speechmaticstoken)

# e_speechmaticslanguage = EntryBox(lf_preferences, 'Speechmatics Language:', 8,
#                                   4, 'catdv.TLabel', ascii_16_127, message_asciionly,
#                                   'Preferences', 'speechmatics_language')
# data_entry_widgets.append(e_speechmaticslanguage)

create_label(lf_preferences, 'Speechmatics Language:',
             'catdv.TLabel').grid(row=4, column=0, sticky='W')
languages = [
    'Any language (auto)', 'Arabic (ar)', 'Bulgarian (bg)', 'Catalan (ca)',
    'Croatian (hr)', 'Czech (cs)', 'Danish (da)', 'Dutch (nl)', 'English - British (en-GB)',
    'English - Global (en)', 'English - North American (en-US)', 'Finnish (fi)', 'French (fr)',
    'German (de)', 'Greek (el)', 'Hindi (hi)', 'Hungarian (hu)', 'Italian (it)', 'Japanese (ja)',
    'Korean (ko)', 'Latvian (lv)', 'Lithuanian (lt)', 'Polish (pl)', 'Portugese (pt)',
    'Romanian (ro)', 'Russian (ru)', 'Slovak (sk)', 'Slovenian (sl)', 'Spanish (es)', 'Swedish (sv)'
]
c_speechmaticslanguage = ComboBox(lf_preferences, 25, languages,
                                  4, 1, 'Preferences', 'speechmatics_language')
data_entry_widgets.append(c_speechmaticslanguage)

create_label(lf_preferences, 'Speechmatics Notifications:',
             'catdv.TLabel').grid(row=3, column=0, sticky='W')
chk = False
e_speechmaticsnotifications = CheckBox(
    lf_preferences, '', 'Preferences', 'speechmatics_notifications_on')
e_speechmaticsnotifications.grid(row=3, column=1, sticky='W')
data_entry_widgets.append(e_speechmaticsnotifications)

e_speechmaticsnotificationemail = EntryBox(lf_preferences, 'Speechmatics Notification Email:', 55,
                                           2, 'catdv.TLabel', ascii_16_127, message_asciionly,
                                           'Preferences', 'speechmatics_notifications_email')
data_entry_widgets.append(e_speechmaticsnotificationemail)

create_label(lf_preferences, 'Transcript Timestamp Every:',
             'catdv.TLabel').grid(row=5, column=0, sticky='W')
timestamps = ['Speaker', 'Sentence']
c_timestamp = ComboBox(lf_preferences, 8, timestamps, 5, 1, 'Preferences', 'transcript_timestamps')
data_entry_widgets.append(c_timestamp)

create_label(lf_preferences, 'Debug Messages in Log:',
             'catdv.TLabel').grid(row=6, column=0, sticky='W')
chk = False
e_debugmessages = CheckBox(
    lf_preferences, '', 'Preferences', 'debug_messages_on')
e_debugmessages.grid(row=6, column=1, sticky='W')
data_entry_widgets.append(e_debugmessages)

'''
Transcribe Tab Schedule Group: Comboboxes with Labels
'''

data_entry_widgets.append(lf_schedule.checkbox)

e_runminuteson = CheckBox(lf_schedule, '', 'Schedule',
                          'run_minutes_on')
e_runminuteson.grid(row=0, column=0, sticky='W')
data_entry_widgets.append(e_runminuteson)

create_label(lf_schedule, 'Run Every',
             'catdv.TLabel').grid(row=0, column=1, sticky='W')
minutes = []
# for h in range(1, 13):
for m in range(5, 65, 5):
    minutes.append(str(m))
c_minutes = ComboBox(lf_schedule, 5, minutes, 0, 2, 'Schedule', 'run_minutes')
data_entry_widgets.append(c_minutes)
create_label(lf_schedule, 'Minutes', 'catdv.TLabel').place(
    in_=c_minutes, relx=1.4, rely=0.5,
    anchor='center', bordermode="outside")

e_rundayson = CheckBox(lf_schedule, '', 'Schedule',
                       'run_days_on')
e_rundayson.grid(row=1, column=0, sticky='W')
data_entry_widgets.append(e_rundayson)
# establish an xor relationship between runminutes and rundays
e_runminuteson.configure(command=e_rundayson.toggle_off)
e_rundayson.configure(command=e_runminuteson.toggle_off)

create_label(lf_schedule, 'Run Every',
             'catdv.TLabel').grid(row=1, column=1, sticky='W')
#  should use calendar.day_name from the calendar module
weekdays = ('Day', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
c_weekday = ComboBox(lf_schedule, 9,  weekdays, 1, 2, 'Schedule', 'run_days_day')
data_entry_widgets.append(c_weekday)

create_label(lf_schedule, 'At',
             'catdv.TLabel').grid(row=1, column=3, sticky='W')
times = []
for h in range(1, 13):
    for m in range(0, 60, 15):
        times.append(str(h) + ":" + str(m).zfill(2))
c_hour = ComboBox(lf_schedule, 5, times, 1, 4, 'Schedule', 'run_days_time')
data_entry_widgets.append(c_hour)

ampm = ('AM', 'PM')
c_ampm = ComboBox(lf_schedule, 3, ampm, 0, 2, 'Schedule', 'run_days_ampm')
c_ampm.place(in_=c_hour, relx=1.4, rely=0.5, anchor='center', bordermode="outside")
data_entry_widgets.append(c_ampm)


''' License Tab Status '''
t_licstatus = LicenseStatusMessageBox(lf_licensestatus)
t_licstatus.grid(column=0, row=0, columnspan=5, padx=(10, 10), pady=(10, 10))

''' License Tab Licensing Information: Entry Boxes with Label and Paste Button '''
e_registered = EntryBox(lf_licenseinfo, 'Registered to:', 40, 0,
                        'catdv.TLabel', ascii_16_127, message_asciionly, '', '')

e_license = EntryBox(lf_licenseinfo, 'Registration code:', 40, 1,
                     'catdv.TLabel', license_format, message_license, '', '')

b_paste = ButtonPasteCatdv(lf_licenseinfo, 'Paste', 0, 3, "")

b_apply = ButtonApplyCatdv(lf_licenseinfo, 'Apply', 1, 3, "")


''' Create The Status Messages Text Box '''

t_status = StatusMessageBox(buttonframe)
t_status.grid(column=0, row=1, columnspan=5, pady=(0, 10))


''' Create The Lower Button Block '''

if SysInfo.system() == 'Darwin':
    tooltip = (
        ('Undoes changes. ', 'centered'),
        ('Option+Click', ('centered', 'yellow')),  # specify mac/windows
        (' reloads defaults.', 'centered')
    )
elif SysInfo.system() == 'Windows':
    tooltip = (
        ('Undoes changes. ', 'centered'),
        ('Ctrl+Click', ('centered', 'yellow')),  # specify mac/windows
        (' reloads defaults.', 'centered')
    )
b_reset = ButtonCatdv(buttonframe, 'Reset', 0, 0, tooltip)

# tooltip = messageclear
if SysInfo.system() == 'Darwin':
    tooltip = (
        ('Test connections to Flow and Speechmatics. Test Transcribe paths.', 'centered'),
    )
elif SysInfo.system() == 'Windows':
    tooltip = (
        ('Test connections to Flow and Speechmatics. Test Transcribe paths.', 'centered'),
    )
b_test = ButtonCatdv(buttonframe, 'Test', 0, 1, tooltip)

if SysInfo.system() == 'Darwin':
    tooltip = (
        ('Transcribe the first clip found tagged \"Send to Speechmatics\".', 'centered'),
    )
elif SysInfo.system() == 'Windows':
    tooltip = (
        ('Transcribe the first clip found tagged \"Send to Speechmatics\".', 'centered'),
    )
b_run = ButtonCatdv(buttonframe, 'Run', 0, 2, tooltip)

if SysInfo.system() == 'Darwin':
    tooltip = (
        # ('Saves changes. ', 'centered'),
        # ('Option+Click', ('centered', 'yellow')),  # specify mac/windows (Alt+Click)
        # (' writes changes into the defaults file.', 'centered')
    )
elif SysInfo.system() == 'Windows':
    tooltip = (
        # ('Saves changes. ', 'centered'),
        # ('Ctrl+Click', ('centered', 'yellow')),  # specify mac/windows (Alt+Click)
        # (' writes changes into the defaults file.', 'centered')
    )
b_save = ButtonCatdv(buttonframe, 'Save', 0, 3, tooltip)

tooltip = messageclear
b_quit = ButtonCatdv(buttonframe, 'Quit', 0, 4, tooltip)

''' Create the Display Controller '''
dsp = DisplayController()
dsp.authentication_refresh()

'''  Read The Config File From Disk '''

cp_config = CPio.readCP(FileInfo.configPath())  # read the configuration file from disk
if cp_config.sections() == []:  # no confifguration file
    cp_config = CPio.readCP(FileInfo.defaultsPath())  # read the defaults file from disk
reset_settings_from_cp(cp_config)  # load the display widgets with values from cp_config
lf_schedule.toggle_scheduling()  # refresh the schedule_on state in the GUI


root.mainloop()
