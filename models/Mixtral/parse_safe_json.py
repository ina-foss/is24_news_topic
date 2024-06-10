#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    description='Script to cleanup the JSON that should be generated by ' \
    'Mixtral into valid JSON. It also tries to remove hallucinations with ' \
    'various techniques, such as detecting characters `<<<` that indicates a ' \
    'new example being generated by the model.'
)
parser.add_argument(
    '--input_file',  required=True, type=str,
    help='Input text file that should containg JSON generated by Mixtral.'
)
parser.add_argument(
    '--output_file', required=True, type=str,
    help='Output JSON file that will be valid, whatever the inputs were. ' \
    'Do not specify the same file for input and output.'
)
parser.add_argument(
    '--force_overwrite', action='store_true',
    help='If False (default) will not parse the JSON if the output file exists.'
)
args = parser.parse_args()

####################################################

import re
import os
import json

assert os.path.exists(args.input_file)
if not args.force_overwrite and os.path.exists(args.output_file):
    exit(0)

with open(args.input_file, 'r') as f:
    input = f.read()

def safe_parse(input_origin):
    input = input_origin
    if len(input) == 0:
        return []

    input = input.replace('{', '[').replace('}', ']').replace("'", '"').replace('\\', '').lower().strip()

    def rm_prefix(input, prefix, remove_end=None):
        if input.startswith(prefix):
            input = input[len(prefix):]
            if remove_end:
                input = input[:remove_end]
        return input

    input = rm_prefix(input, "categories:")
    input = rm_prefix(input, '["categories": ', remove_end=-1)
    input = rm_prefix(input, '["category": ', remove_end=-1)

    input = input.replace(': 1.0', '').replace(': 1', '').replace(': ""', '')

    # removing everything after <<< (hallucinations)
    sub = '<'*3
    if sub in input:
        input = input[:input.index(sub)]

    def _custom_json_loads(s):
        loaded = json.loads(s)
        if isinstance(loaded, str):
            return [loaded]
        if isinstance(loaded, list) and len(loaded) == 1 and not isinstance(loaded[0], str):
            return loaded[0]
        return loaded

    try:
        loaded = _custom_json_loads(input)
        if isinstance(loaded, str):
            return [loaded]
        return loaded
    except json.decoder.JSONDecodeError:
        lines = input.splitlines()
        if len(lines) > 1:
            return safe_parse(lines[0])

        if '[' in input and ']' in input:
            # fallback: return dict of words
            start = input.index('[')
            end = input.index(']')
            cut = input[start:end+1]
            try:
                return _custom_json_loads(cut)
            except json.decoder.JSONDecodeError:
                parts = re.split(r'[", :\[\]]', cut)
                return [p for p in parts if len(p) > 0]

        print(f"ERROR: could not parse the following original json ({args.input_file}):")
        print("```json")
        print(input_origin)
        print("```")
        print("\n\n")
        return []

with open(args.output_file, 'w') as f:
    json.dump(safe_parse(input), f, indent=4, ensure_ascii=False)
