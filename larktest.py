from lark import Lark, tree

class MsgPrototype:
    def __init__(self, name, id, membertypes: list, membernames: list):
        self.name = name
        self.id = id
        self.membertypes = membertypes
        self.membernames = membernames
    
    @staticmethod
    def populate_from_tree(t: tree.Tree):
        name = []
        id = []
        membertypes = []
        membernames = []

        # Get members
        for mem in t.find_data("members"):
            for m in mem.children:
                membertypes.append(m.children[0].value)
                membernames.append(m.children[1].value)
        # get msg name
        for m in t.find_data("msgname"):
            for n in m.children:
                name = n.value
        # get msg id
        for m in t.find_data("msgid"):
            for n in m.children:
                id = n.value
        return MsgPrototype(name, id, membertypes, membernames)

    def generate_c_code(self):
        nl='\n'
        s = f"struct {self.name} {{"
        s += '\n\t'
        s += f"{self.name}(const Packet&);"
        s += '\n\t'
        s += f"int id={self.id};"
        s += '\n\t'
        for t, n in zip(self.membertypes, self.membernames):
            s += f"{t} {n};"
            s += '\n\t'
        s += f"}};"
        return s

def do_parse():
    grammar = open("grammar.lark")
    generate = open("generate.lark")

    parser = Lark(grammar.read())
    parser2 = Lark(generate.read())
    f = open("extra_messages.msg").read()
    g = open("msg.cpp").read()

    out = parser.parse(f)
    out2 = parser2.parse(g)
    msg = MsgPrototype.populate_from_tree(out)
    code = msg.generate_c_code()
    return code
    # tree.pydot__tree_to_png(out, "tree.png")
    # tree.pydot__tree_to_png(out2, "tree2.png")

if __name__ == "__main__":
    do_parse()