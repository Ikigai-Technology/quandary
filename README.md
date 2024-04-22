# Quandary

`quandary` is a minimalist language for allowing your users to express decision logic.

## Usage

```py
from qandary import compiler

code = compiler.parse("""a + 6""")

scope = {
    "a": 5.0,
}

result = code(scope)  # 11.0
```

## Syntax

Scope lookup

    a
    a.b
    a.b.c

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
    x ** 2

Comparisons

    <
    <=
    =
    <>
    >=
    >
    in

Logic

    not x
    x and y
    x or y

Conditional (two styles available)

    (x=1 ? "x equals one" : "x isn't one")
    (x=1 ? "one" : x=2 ? "two" : x=3 ? "three" : "something else")
    ("one" if x=1, "two" if x=2 else "three")
    ("one" if x=1, else "not one")

Functions

    func(arg, arg, ...)

Functions must be attached to the `scope` as a property [not a key].

## Scope

To help, there is the `Scope` class.

    import math

    from quandary import compiler, Scope

    scope = Scope({
            "scale": 1.5,
            "dimension": {"width": 200}
        },
        functions={
            "root": math.sqrt,
        },
    )

    code = compiler.parse("root(scale * dimension.width)")

    code(scope)  # 17.320508075688775

## Default values

When a scope lookup is made for a name that doesn't exist, `quandary` will look
for a `default` property on the `scope`, or default to `None`.

The `Scope` class a `default` argument, letting you specify the value to use.

    from quandary import compiler, Scope

    scope = Scope({}, default=False)

    func = compiler.parse("a")

    result = func(scope)

    assert result is False


# Thanks

Special thanks to Joey Smith (joeysmith@gmail.com) for helping to refine the
grammer to handle expressions properly.

