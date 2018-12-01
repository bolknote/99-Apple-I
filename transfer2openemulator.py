#!/usr/bin/env python
# run ./transfer2openemulator.py | /usr/bin/osascript

import itertools as I
import re

hexstr=r"""
:10028000F8A9994820D10220EB02A241A00220C681
:1002900002684820D10220F00220F70220FE026806
:1002A00038E9014820D10220EB0220F70268C9009A
:1002B000D0D12003034C1FFFC90FB0034CE5FF4C06
:1002C000DCFFBC0803E8BD080320EFFFE888D0F698
:1002D00060C900F0114820B802A203A00868C90153
:1002E000D001884CC602A2004CC202A20B4CC20232
:1002F000A20CA0084CC602A2C3A0024CC602A220B7
:100300004CC202A2434CC2020A4E4F20424F5454E8
:100310004C455314204F462042454552204F4E2015
:100320005448452057414C4C2254414B45204F4E98
:100330004520444F574E20414E44205041535320B6
:1003400049542041524F554E442C20804E4F204D51
:100350004F524520424F54544C4553204F46204263
:10036000454552204F4E205448452057414C4C2C77
:10037000204E4F204D4F524520424F54544C455330
:10038000204F4620424545522E8D474F20544F2046
:100390005448452053544F524520414E4420425525
:1003A0005920534F4D45204D4F52452C203939206F
:1003B000424F54544C4553204F462042454552200D
:0D03C0004F4E205448452057414C4C2E8D87
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

	vkcodes = get_vk_keycodes()

	for keys_group in keys:
		for key in keys_group:
			if key == "\n":
				yield 'keystroke return'
				yield 'delay 1'
			else:
				vk = vkcodes.get(key)
				if vk is None:
					yield 'keystroke "{}"'.format(key)
				else:
					yield 'key code {}'.format(vk)

				yield 'delay .05'
	yield 'end tell'

def get_vk_keycodes() -> dict:
	codes = {}

	fn = '/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/Headers/Events.h'
	try:
		with open(fn, 'rb') as f:
			for line in (line.decode('latin-1') for line in f):
				match = re.match(r'(?i)^\s+kVK_ANSI_(\w)\s*=\s*0x([0-9A-F]+)', line)
				if match:
					codes[match[1]] = int(match[2], 16)
	except FileNotFoundError:
		pass

	return codes

for cmds in to_osa_cmds(get_lines(hexstr, address)):
	print(cmds)
