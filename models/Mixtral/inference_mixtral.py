#!/usr/bin/env python3

import time
from openai import OpenAI

def ask_model(client, model, prompt, transcript, output_file=None):
    result = client.chat.completions.create(
        model=model,
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt.replace('{transcript}', transcript)
            },
        ]
    )
    if output_file is not None:
        with open(output_file, 'w') as f:
            assert len(result.choices) == 1, \
                f"Error, should have only one response. {result}"
            print(result.choices[0].message.content, file=f)
    return result

def _process(params):
    client, input_file, output_file, model, prompt = params
    # do not process already processed files
    if os.path.exists(output_file):
        return

    # read the transcript of this file
    with open(input_file, 'r') as f:
        trans = f.read()

    # ask the model it's prediction
    ask_model(
        client=client,
        model=model,
        prompt=prompt,
        transcript=trans,
        output_file=output_file,
    )

if __name__ == "__main__":
    import argparse
    import tqdm
    import glob
    import os

    from tqdm.contrib.concurrent import process_map

    parser = argparse.ArgumentParser(
        description='Script to perform inference of the Mixtral model running' \
        ' on a OpenAI-compatible server (VLLM).'
    )
    parser.add_argument(
        '--prompt_file', required=True, type=str,
        help='Path to a file containing the prompt. `{transcript}` will be ' \
        'replaced with the dialogue transcript.'
    )
    parser.add_argument(
        '--input_dir', required=True, type=str,
        help='Directory containing input text files with dialogues.'
    )
    parser.add_argument(
        '--output_dir', required=True, type=str,
        help='Directory that will contain output files.'
    )
    parser.add_argument(
        '--openai_api_key', type=str, default='EMPTY'
    )
    parser.add_argument(
        '--openai_api_base', required=True, type=str,
        help='Endpoint of the OpenAI-compatible API server.'
    )
    parser.add_argument(
        '--ask_jobs', default=4, type=int,
        help='Number of parallel jobs that will ask to the API for inference.'
    )
    parser.add_argument(
        '--model', default='casperhansen/mixtral-instruct-awq', type=str,
        help='Name of the model to perform inference with.'
    )
    args = parser.parse_args()

    client = OpenAI(
        api_key=args.openai_api_key,
        base_url=args.openai_api_base,
    )

    import random
    random.seed(42)

    with open(args.prompt_file, 'r') as f:
        prompt = f.read()

    files = glob.glob(os.path.join(args.input_dir, '*.txt'))
    random.shuffle(files)

    params = (
        (
            client,
            file,
            os.path.join(args.output_dir, os.path.basename(file)),
            args.model,
            prompt
        ) for file in files
    )

    process_map(_process, params, max_workers=args.ask_jobs, total=len(files))
