import argparse
from pathlib import Path


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfilename', type=str, default=None,
                        action='store',
                        help='The input file name')
    return parser


def build_py_module(inputfile, outputfile_py, mark='export'):
    mark = '# ' + mark
    new_definition = False
    functions = list()
    for line in inputfile:
        outputfile_py.write(line)
        if line.startswith(mark):
            new_definition = True
            continue
        if new_definition:
            function = parse_py_definition_line(line)
            functions.append(function)
            new_definition = False

    return functions


def parse_py_definition_line(line):
    if line[0:4] != 'def ':
        raise ValueError('Line after mark does not start with def: {}'
                         .format(line))
    line = line[4:]
    parts = line.partition('(')
    if parts[1] == '':
        raise ValueError('Could not read definition line: {}'.format(line))
    return parts[0]


def write_py_header(output):
    output.write('import sys\n')


def write_sh_wrappers(output, module, functions):
    for function in functions:
        output.write("function {} {{\n".format(function))
        output.write("    python3 {} {} $@\n".format(module, function))
        output.write("}\n")


def write_py_main(output, functions):
    output.write("\n\n")
    output.write("if __name__ == '__main__':\n")
    output.write("    if len(sys.argv) == 0:\n")
    output.write("        raise ValueError('Function name required')\n")
    output.write("\n")
    output.write("    functions = dict()\n")

    for function in functions:
        output.write("    functions['{0}'] = {0}\n".format(function))

    output.write("    function_to_call = sys.argv[1]\n")
    output.write("    del sys.argv[1]\n")
    output.write("    function = functions[function_to_call]\n")
    output.write("    result = function()\n")
    output.write("    if result is not None:\n")
    output.write("        print(result)\n")


if __name__ == '__main__':
    parser = create_parser()
    arguments = parser.parse_args()

    shelladder = Path.home() / '.shelladder'
    shelladder.mkdir(parents=True, exist_ok=True)

    inputfile = Path(arguments.inputfilename)
    outputfile_py = shelladder / inputfile.name
    outputfile_sh = shelladder / inputfile.with_suffix('.sh').name

    with inputfile.open('r') as inputfile:
        with outputfile_py.open('w') as output_py:
            functions = None
            write_py_header(output_py)
            functions = build_py_module(inputfile, output_py)
            write_py_main(output_py, functions)

        with outputfile_sh.open('w') as output_sh:
            write_sh_wrappers(output_sh, outputfile_py, functions)

    print(outputfile_sh)
