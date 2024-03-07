# Quandary

`quandary` is a minimalist language for allowing your users to express decision logic.

## Usage

```py
from qandary import compiler

code = compiler.parse("""a + 6""")

scope = {
    "a": 5.0,
}

result = code.eval(scope)  # 11.0
```

## Syntax

Variable lookup

    a
    a.b

Only two levels of lookup are supported.

Literals

    1
    -1
    1.0
    -1.0
    "string"

Maths

    a + b
    a - -5
    (a + 6) * -3.0

Comparisons

    <
    <=
    =
    <>
    >=
    >

Logic

    not x
    x and y
    x or y

Functions

    func(arg, arg, ...)

Functions must be attached to the `scope` as a property [not a key].

To help, there is the `Scope` class.

    scope = Scope({default data}, functions={...})
