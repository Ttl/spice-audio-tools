#!/usr/bin/env python3
#coding: utf-8

import argparse
import re
import struct
import sys
import wave

SAMPLING_RATE = 44100


def parse_output(spice_output):
	''' parses ngspice output. use `wrdata <filename> v(<pin>)` command
		to generate right output
	'''

	times = []
	voltages = []

	with open(spice_output, 'r') as output:
		for line in output:
			if line:
				row = re.split('\s+', line.strip())
				times.append(float(row[0]))
				voltages.append(float(row[1]))

	return times, voltages


def lin_interp(x0, x1, y0, y1, x):
    x0 = float(x0)
    x1 = float(x1)
    y0 = float(y0)
    y1 = float(y1)
    x = float(x)
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def write_wav(times, voltages, filename, clipping):
	with wave.open(filename, 'w') as w:
		w.setparams((1, 2, SAMPLING_RATE, 0, 'NONE', 'not compressed'))
		m = max(max(voltages), -min(voltages))
		vrange = clipping if clipping else m

		values = bytes([])
		t = 0.0
		step = 1.0 / SAMPLING_RATE

		for i in range(len(voltages)-1):
			while times[i] <= t * step < times[i+1]:
				sample = lin_interp(times[i], times[i+1],
					voltages[i], voltages[i+1], t*step) / vrange
				sample = 1 if sample >1 else sample
				sample = -1 if sample <-1 else sample
				d = struct.pack('<h',int(32767 * sample))
				values += d
				t += 1

		w.writeframes(values)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("spice_output",
		help="Specify file with spice output")
	parser.add_argument("wav_file",
		help="Specify filename for wav data")
	parser.add_argument("--clipping", dest='clipping',
			default=0, type=float)
	args = parser.parse_args()

	times, voltages = parse_output(args.spice_output)
	write_wav(times, voltages, args.wav_file, args.clipping)

if __name__ == "__main__":
    main()
