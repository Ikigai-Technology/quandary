from parsimonious.grammar import Grammar

grammar = Grammar(r"""
# Boolean

bool_expr = (bool_term _ "or" _ bool_term) / bool_term

bool_term = (bool_factor _ "and" _ bool_factor) / bool_factor

bool_factor = ("(" bool_expr ")") / ("not" _ bool_factor) / comparison

# Comparisons

comparison = (sum _ comp_op _ sum) / sum

comp_op = "<=" / "<>" / "<" / "=" / ">=" / ">"

# Basic maths

sum = (term _ sum_op _ sum) / term

sum_op = "+" / "-"

term = (factor _ prod_op _ term) / factor

prod_op = "*" / "/"

factor = function / string / boolean / lookup / number / factor

# Functions

arguments = (bool_expr "," _ arguments) / bool_expr
function = name "(" arguments ")"

# Basic value sources

lookup = (name "." name) / name

name    = ~r"[a-zA-Z]\w*"
number  = ~r"-?\d+(\.\d+)?"
boolean = "TRUE" / "FALSE"
string = ~r"\"([^\"\\]|\\\")*?\""

_ = ~r"\s+"
""")
