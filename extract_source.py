from collections import defaultdict

import json

import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('path')
def show(path):
    sources = defaultdict(list)
    with open(path, 'r') as jfile:
        obs_json = json.load(jfile)
        for source in obs_json.get('sources', []):
            sources[source["id"]].append(source["name"])
    for source_type in sorted(sources.keys()):
        for src in sorted(sources[source_type]):
            print(f'{source_type: >{24}} {src}')

@cli.command()
@click.option('--source', help='source name(s) to extract', multiple=True)
@click.argument('path')
def extract(path, source):
    output = []
    with open(path, 'r') as jfile:
        obs_json = json.load(jfile)
        for src in obs_json.get('sources', []):
            if src['name'] in source:
                output.append(src)

    if len(output) == 1:
        output = output[0]
    print(json.dumps(output, indent=4))

if __name__ == '__main__':
    cli()