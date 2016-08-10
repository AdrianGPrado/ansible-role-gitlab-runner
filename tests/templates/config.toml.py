#!/usr/bin/env python

import os
import re
import sys
import yaml
from jinja2 import Environment,     \
                   FileSystemLoader

PROJECT_PATH = os.getcwd()

TEMPLATE_ENVIRONMENT = Environment(
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            loader=FileSystemLoader(os.path.join(PROJECT_PATH, 'templates')))

def write_template(template_filename, context, templ_env=TEMPLATE_ENVIRONMENT):
    out_fname = '.'.join(template_filename.split('.')[:-1])

    with open(out_fname, 'w') as f:
        rend_out = templ_env.get_template(template_filename).render(context)
        f.write(rend_out)

def filter_val(val, contex):
    regexp = re.compile(r'({{ (\w+) }})')
    # print("Ini:", val)
    for g in regexp.finditer(val):
        # The first and second parenthesized subgroup.
        search, replace = g.group(1, 2)
        val = re.sub(search, replace, val)

    # print("End:", val)
    return val

def read_yaml_files(vars_filename):
    """
    With a list of YAML files create a dictironary with all the variables.
    """
    print(vars_filename)
    context = dict()
    for f in vars_filename:
        with open(f, 'r') as stream:
            try:
                for key, val in yaml.load(stream).items():
                    if isinstance(val, str):
                        val = filter_val(val, context)
                    context[key] = val
            except yaml.YAMLError as exc:
                print(exc)
    return(context)

def input_files(files):
    """
    With a list of files, tiplicaly sys.argv[1:] return a tupple.
        - template_file: Is string with the path to the file to use as a template in Jinja2
        - context_files: Is a list of strings with the path to the files to be used to build the dictionary for the Jinja2 template render.
    """
    template_file = files[0]

    context_files = list()
    for fpath in files[1:]:
        context_files.append(os.path.join(PROJECT_PATH, fpath))

    return(template_file, context_files)

def main():
    # Generate tuple with Jinja2 template and vars input files
    template_file, context_files = input_files(sys.argv[1:])
    # Read input files and create a dictionary with the variables
    context = read_yaml_files(context_files)
    # Parse template
    write_template(template_file, context)
    print(os.getcwd())

########################################

if __name__ == "__main__":
    main()
