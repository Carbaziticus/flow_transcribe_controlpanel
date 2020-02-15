#!python3

import plistlib

'''
create macos launchagent
'''

transcribeapp_path = '/Users/charlielangrall/Desktop/Technical/Programming/python/Projects/flow-env/dist/flow_transcribe.app'
label = 'com.langrallconsulting.flow_transcribe'
hour = 0
minute = 0
interval = 60
debug = 'On'
pl = dict()
#     Label=label,
#     ProgramArguments=['/usr/bin/open', '-W', transcribeapp_path],
#     StartCalendarInterval=dict(
#         Hour=hour,
#         Minute=minute,
#     ),
#     StartInterval=interval,
# )
print(pl.items())

pl['Label'] = label
pl['ProgramArguments'] = ['/usr/bin/open', '-W', transcribeapp_path, '--args', '-d', debug]
if hour != 0:
    pl['StartCalendarInterval'] = dict(Hour=hour, Minute=minute)
if interval != 0:
    pl['StartInterval'] = interval

with open('/Users/charlielangrall/Library/LaunchAgents/com.langrallconsulting.flow_transcribe.plist', 'wb') as fp:
    # with open('com.langrallconsulting.flow_transcribe.plist', 'wb') as fp:
    plistlib.dump(pl, fp)
