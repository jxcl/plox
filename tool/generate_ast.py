import sys

from os import path

class IndentWriter:
    INDENTATION = ' ' * 4

    def __init__(self, fp):
        self.fp = fp

    def write(self, content, indent_level):
        indentation = self.INDENTATION * indent_level

        self.fp.write(indentation)
        self.fp.write(content)
        self.fp.write('\n')

def extract_field_names(fields):
    field_list = fields.split(', ')
    return [f.split(' ')[1] for f in field_list]

def define_ast(output_directory, base_name, types):
    output_path = path.join(output_directory, '{}.py'.format(base_name.lower()))

    with open(output_path, 'w') as fp:
        writer = IndentWriter(fp)
        writer.write("class {}:".format(base_name), indent_level=0)

        writer.write("pass", indent_level=1)
        writer.write("", indent_level=0)

        for ty in types:
            class_name, fields = ty.split(':')
            define_type(writer, base_name, class_name.strip(), fields.strip())

def define_type(writer, base_name, class_name, fields):
    field_names = extract_field_names(fields)

    writer.write("class {}({}):".format(class_name, base_name), indent_level=0)

    writer.write("def __init__(self, {}):".format(', '.join(field_names)), indent_level=1)
    for name in field_names:
        writer.write("this.{0} = {0}".format(name), indent_level=2)

    writer.write('', indent_level=0)

if __name__ == '__main__':
    if len(sys.argv[1:]) != 1:
        print("Usage: generate_ast.py <output_directory>")
        sys.exit(1)

    output_directory = sys.argv[1]

    define_ast(output_directory, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "literal  : Object value",
        "Unary    : Token operator, Expr right",
    ])
