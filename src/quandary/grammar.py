from parsimonious.grammar import Grammar

grammar = Grammar(r"""
    expr = ws logical_expr ws
    logical_expr = not_expr ( ws bool_operator ws not_expr )*

    not_expr = ("not" ws)? comparison_expr
    comparison_expr = sum_expr ( ws comparison_operator ws sum_expr )?

    sum_expr = factor_expr ( ws sum_operator ws factor_expr )*
    factor_expr = power_expr ( ws factor_operator ws power_expr )*
    power_expr = term ( ws power_operator ws term )?

    term = number / string / parens / boolean / function / lookup

    parens = ws "(" expr ")" ws

    # Operators

    bool_operator = "and" / "or"
    sum_operator = "+" / "-"
    factor_operator = "*" / "/"
    power_operator = "**"
    comparison_operator = "<=" / "<>" / "<" / "=" / ">=" / ">"

    # Functions

    arguments = expr ("," expr)*
    function = name "(" arguments? ")"

    # Basic value sources

    lookup = name ("." name)*

    name = ~r"[a-zA-Z]\w*"
    number  = ~r"-?\d+(\.\d+)?"
    boolean = "TRUE" / "FALSE"
    string = ~r"\"([^\"\\]|\\\")*?\""

    ws = ~r"\s*"
""")
