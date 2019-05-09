# pythonCodeAnalysis

Serverless function to analyse problem and solution code to identify features used

# Constructs

'constructs' code features correspond to various programming constructs, such
as slicing, list comprehension, keyword argument usage, etc.
Note that not all constructs are independent from each other and there may
be some overlap between them. In particular, some constructs are specialized
versions of broader constructs. For example, there is a general construct
'Comprehension' and its specialized versions 'ListComprehension',
'SetComprehension', 'DictionaryComprehension' and 'GeneratorExpression'. Thus
a list comprehension is counted both as a 'Comprehension' construct and as a
'ListComprehension' construct. Similarly a multi-target assignment
(e.g. "a, b = 1, 2") is counted both as an 'Assignment' construct and as a
'MultiTargetAssignment' construct.

**Currently detected/recognized constructs are:**

**Assignment -** Corresponds to an assignment statement.
**MultiTargetAssignment -** Corresponds to an assignment statement with
multiple targets.
Example:
a, b = 1, 2
Also counts as an Assignment construct.
**ChainedCompare -** Corresponds to a chained sequence of comparison
expressions.
Example:
1 < x <= y < 10
**KeywordArgumentUsage -** Corresponds to a function call with a keyword
argument (argname=value syntax).
Example:
print('abc', end='')
**Subscription -** Referring to an item (or multiple items) of a
sequence or mapping object.
Example:
a[1]
line[4:-2]
table['abc']
**Slicing -** Usage of slicing ( [start?:end?:stride?] ) in
subscription.
Example:
items[:]
line[1:-1]
array[::2]
**IfExpression -** Usage of an if-expression.
Example:
a if a > b else b
**Comprehension -** Corresponds to any usage of list, set or dictionary
comprehension or generator expression.
**FilteredComprehension -** Corresponds to a comprehension containing one
or more if's.
Example:
[x for x in xlist if x > 0]
Also counts as a Comprehension construct.
**MultilevelComprehension -** Corresponds to a comprehension containing two
or more for's.
Examples:
[(x,y) for x in xlist for y in ylist][x for y in z for x in y]
Also counts as a Comprehension construct.
**ListDisplay -** Corresponds to a new list object, specified by
either a list of expressions or a comprehension
enclosed in square brackets.
Examples:
[1, 2, 3][2*x for x in y]
**ListComprehension -** A specialized form of a ListDisplay construct. Also
counts as a Comprehension construct.
**SetDisplay -** Corresponds to a new set object, specified by
either a list of expressions or a comprehension
enclosed in curly braces.
Examples:
{1, 2, 3}
{x**2 for x in y}
**SetComprehension -** A specialized form of a SetDisplay construct. Also
counts as a Comprehension construct.
**DictionaryDisplay -** Corresponds to a possibly empty series of key:datum
pairs (possibly produced through a comprehension)
enclosed in curly braces, defining a new dictionary
object.
Examples:
{1:'a', 2:'b', 3:'c'}
{x:bin(x) for x in y}
**DictionaryComprehension -** A specialized form of a DictionaryDisplay construct.
Also counts as a Comprehension construct.
**GeneratorExpression -** A comprehension enclosed in parentheses, producing
a new generator object. Also counts as a
Comprehension construct.
**FunctionDef -** Definition of a function.
**ClassDef -\*\* Definition of a class.
