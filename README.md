# `ctrl-lang` overview

## Philosophy

`ctrl-lang` is about using concepts from functional programming languages to enable high performance code which remains readable and compact, with an eye to math-heavy domains (for instance: data processing, academic simulations, or graphical rendering).

Unlike other languages, `ctrl-lang` differentiates "procedures" from "functions". Procedures are our traditional understanding of functions: a block of code which executes statement-by-statement when called. Functions, on the other hand, are "pure". These have no side effects, and will return the same thing when called many times. Procedures exist as a way of sitting between the stateful world and the pure world of functional programming. As such, procedures may call functions or other procedures, but functions can only call other functions.

The purity of functions produce a number of performance improvements:
 - As functions do not depend on the state, the time they are called is not when they have to be computed. For instance, a latent thread may be able to compute near-future functions ahead of their call, or the results of functions which are called repeatedly may be stored.
 - As functions cannot modify resources, many traditional problems arising from parallel resource access in multi-threaded environments are excluded.

Note: This document is more of a lodestar to work towards, rather than documentation of what is currently implemented.

## Syntax

### Comments

Comments are prefixed by `/*` and suffixed by `*/`. These can span multiple lines.

```java
/* This is an inline comment */

/*
   This is a comment,
   over several lines.
 */
```

### Literals, Types, and Variables

When operating within the functional world, all variables are immutable.

While variable types are not explicitly stated, `ctrl-lang` is strongly typed through inferrence.

Unlike traditional languages, which use the `=` operator, assignment is done with the the `:=` operator in `ctrl-lang`. `=` is instead reserved to test equality.

```java
a := 3         /* integer */
b := 2.0       /* double */
c := [0,1,2]   /* fixed length array */ 
d := [0,...,2] /* same array built from range constructor */
```

### Functions

Function declaration is of the form `<function name> <arguments> :: <type_signature>`. Code blocks are defined by an indent, and the return value is the final line in the block. For example:

```java
square n :: int -> int
    n * n
```

### Function Application

The function application operator `|>` is a syntax sugar which makes `x |> f` equivalent to `f(x)`, which helps make long chains of function calls easier to read.

For given types `T` and `U`, applying a function with type signature `T -> U` to a list with type `[T]` will implicitly call the map function to return a list of type `[U]`. For example, the following returns a list of every square number up to the nth:

```java
sum_of_squares n :: int -> int
    x := [1,...,n]
    x |> square
```

Note: function calls do not require brackets, as this becomes quickly unreadable with large chains of function calls.

### Pattern Matching

`ctrl-lang` features no explicit loops (`for`, `while`) or control flow (`if-else`, `switch`). Instead, `ctrl-lang` can match variable(s) against a number of patterns:

 - a literal will match anything with exactly equals that
 - an expression will match anything which resolves to the outcome of the expression
 - `_` (wildcard) will match anything
 - `[]` will match the empty set
 - `[element]` will match a set with a single element and destructure a variable `element` out of the array
 - `[head, ...tails]` will match a set of any length and destructure the array of type `T` into a variable `head` of type `T` and the rest of the list into a variable of type `[T]` called `tail`

Each pattern to match against follows the form `<variable> | <pattern> => <action>`. For example:

```java
sum A :: [int] -> int
    A | []        => 0
      | [x]       => x
      | [x,...xs] => x + sum xs
```

### Sum of Squares Example

The following returns the sum of all square numbers up to the nth:

```java
square n :: int -> int
    n * n
    
sum A :: [int] -> int
    A | []        => 0
      | [x]       => x
      | [x,...xs] => x + sum xs
      
sum_of_squares n :: int->int
    A := [1, ..., n]
    A |> square
      |> sum
```
