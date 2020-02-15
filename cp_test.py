#! python3

# import CPio
import tkinter as tk
# from tkinter import ttk
# import Styles

# cp_config = CPio.readCP(
#     '/Users/charlielangrall/Desktop/Technical/Programming/python/Projects/flow-env/flow_transcribe_controlpanel/defaults.cfg')
# print(cp_config.sections())
# print(list(cp_config.keys()))
# print(list(cp_config.values()))
# print(cp_config.items('Connection'))
# print(list(cp_config['Connection'].keys()))
# print(cp_config.get('flow_server', ))
# for section in cp_config.sections():
#     print('[{}]'.format(section))
#     for (k, v) in cp_config.items(section):
#         print(k, '=', v)

# print('flow_api_port' in cp_config.values())

# root = tk.Tk()
# root.title('Tkinter CP Test')
# # root.resizable(width=False, height=False)
# # Styles.defineStyles(root)
#
# T = tk.Text(root, height=2, width=30)
# T.pack()
#
# value = T.get("1.0", 'end-1c')
# print(value)
#
# root.mainloop()


master = tk.Tk()


def var_states():
    print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))


tk.Label(master, text="Your sex:").grid(row=0, sticky='W')
var1 = tk.IntVar()
tk.Checkbutton(master, text="male", variable=var1).grid(row=1, sticky='W')
var2 = tk.IntVar()
tk.Checkbutton(master, text="female", variable=var2).grid(row=2, sticky='W')
tk.Button(master, text='Quit', command=master.quit).grid(row=3, sticky='W', pady=4)
tk.Button(master, text='Show', command=var_states).grid(row=4, sticky='W', pady=4)

master.mainloop()
