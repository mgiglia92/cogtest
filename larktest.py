from lark import Lark, tree

grammar = open("grammar.lark")

parser = Lark(grammar.read())
f = open("extra_messages.msg").read()
tree.pydot__tree_to_png(parser.parse(f), "tree.png")