#!/usb/bin/env python
# run ./transfer2openemulator.py | /usr/bin/osascript

import itertools as I
import re

hexstr=r"""
:10028000F8A9994820D40220EE02A241A00220C978
:1002900002684820D40220F30220FA0220010368F9
:1002A00038E9014820D40220EE0220FA0268C90091
:1002B000D0D12006034C1FFF4829F0D004684CE53C
:1002C000FF684CDCFFBC0B03E8BD0B0320EFFFE82D
:1002D00088D0F660C900F0114820B802A203A00837
:1002E00068C901D001884CC902A2004CC502A20B0A
:1002F0004CC502A20CA0084CC902A2C3A0024CC962
:1003000002A2204CC502A2434CC5020A4E4F204215
:100310004F54544C455314204F46204245455220DB
:100320004F4E205448452057414C4C2254414B4598
:10033000204F4E4520444F574E20414E44205041BF
:1003400053532049542041524F554E442C20804E47
:100350004F204D4F524520424F54544C4553204F4F
:10036000462042454552204F4E2054484520574193
:100370004C4C2C204E4F204D4F524520424F545450
:100380004C4553204F4620424545522E8D474F2025
:10039000544F205448452053544F524520414E4419
:1003A0002042555920534F4D45204D4F52452C204A
:1003B000393920424F54544C4553204F4620424532
:1003C0004552204F4E205448452057414C4C2E8DCD
:00000001FF
"""

address = 0x280
chunk_size = 40

def remove_extra(s: str) -> str:
	return re.sub(r'\s', '', re.sub(r'(?m)^:.{8}|..$', '', s))

def split_by_n(seq: str, n: int):
	for i in range(0, len(seq), n):
		ch = seq[i:i+n].lstrip('0')
		yield '0' if ch == '' else ch

def get_hex_lines(hexstr: str):
	pairs = enumerate(split_by_n(remove_extra(hexstr), 2))
	for x in I.groupby(pairs, lambda x: x[0] // chunk_size):
		yield (item[1] for item in x[1])

def get_lines(hexstr: str, address: int):
	start = hex(address)[2:]

	for line in get_hex_lines(hexstr):
		yield hex(address)[2:]+':'
		for item in line:
			yield ' '+item
		yield "\n"

		address += chunk_size

	yield start + '\nR\n'

def to_osa_cmds(keys):
	yield 'activate application "OpenEmulator"'
	yield 'tell application "System Events"'

	for keys_group in keys:
		for key in keys_group:
			if key == "\n":
				yield 'keystroke return'
				yield 'delay 1'
			else:
				yield 'keystroke "{}"'.format(key)
				yield 'delay .05'
	yield 'end tell'

for cmds in to_osa_cmds(get_lines(hexstr, address)):
	print(cmds)

