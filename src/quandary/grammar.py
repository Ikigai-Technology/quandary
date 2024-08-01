from parsimonious.grammar import Grammar

grammar = Grammar(r"""
    expr = ows logical_expr ows
    logical_expr = not_expr ( ows bool_operator ows not_expr )*

    not_expr = ("not" ws)? comparison_expr
    comparison_expr = sum_expr ( ows comparison_operator ows sum_expr )?

    sum_expr = factor_expr ( ows sum_operator ows factor_expr )*
    factor_expr = power_expr ( ows factor_operator ows power_expr )*
    power_expr = term ( ows power_operator ows term )?

    term = number / string / parens / boolean / function / lookup / condition / condition_if / list

    parens = ows "(" expr ")" ows

    list = ows "[" arguments? "]"

    # Operators

    bool_operator = "and" / "or"
    sum_operator = "+" / "-"
    factor_operator = "*" / "/"
    power_operator = "^" / "**"  # ** is legacy power operator
    comparison_operator = "<=" / "<>" / "<" / "=" / ">=" / ">" / "in"

    # Functions

    arguments = expr ("," expr)*
    function = name "(" arguments? ")"

    # Conditional (ternary form)

    condition = "(" (condition_rule ":" )+ expr ")"
    condition_rule = expr "?" expr

    # Conditional (if form)
    condition_if = "(" condition_if_rule ( "," condition_if_rule)* ("," ows)? "else" expr ")"
    condition_if_rule = expr "if" expr

    # Basic value sources

    lookup = name ("." name)*

    name = ~r"[a-zA-Z]\w*"
    number  = ~r"-?\d+(\.\d+)?"
    boolean = "TRUE" / "FALSE"
    string = ~r"\"([^\"\\]|\\\")*?\""

    ows = ~r"\s*"   # Optional whitespace
    ws = ~r"\s+"    # Necessary whitespace
""")
