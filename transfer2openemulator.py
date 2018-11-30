#!/usb/bin/env python
# run ./typer99.py | /usr/bin/osascript

import itertools as I
import re

hexstr=r"""
:10028000F8A9994820D50220EF02A241A00220CA75
:1002900002684820D50220F40220FB026838E901F8
:1002A0004820D50220EF02A2C3A00220CA0268C9DA
:1002B00000D0D02000034C1FFF4829F0D004684C28
:1002C000E5FF684CDCFFBC0503E8BD050320EFFF3C
:1002D000E888D0F660C900F0114820B902A203A056
:1002E0000868C901D001884CCA02A2004CC602A20B
:1002F0000B4CC602A20CA00820CA02A2204CC602C7
:10030000A2434CC6020A4E4F20424F54544C455310
:1003100014204F462042454552204F4E2054484518
:100320002057414C4C2254414B45204F4E452044D0
:100330004F574E20414E44205041535320495420A2
:1003400041524F554E442C20804E4F204D4F524528
:1003500020424F54544C4553204F4620424545526D
:10036000204F4E205448452057414C4C2C204E4F96
:10037000204D4F524520424F54544C4553204F4638
:1003800020424545522E8D474F20544F205448451A
:100390002053544F524520414E442042555920533A
:1003A0004F4D45204D4F52452C20393920424F5456
:1003B000544C4553204F462042454552204F4E2035
:0A03C0005448452057414C4C2E8D47
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

