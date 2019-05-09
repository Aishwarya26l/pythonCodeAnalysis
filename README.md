# pythonCodeAnalysis

Serverless function to analyse python problem and solution code to identify features used.<br/>
The python code analysis function helps identify the following features -

1. Constructs
2. Statements
3. Expressions
4. Functions
5. Imports

## Constructs

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

### Currently detected/recognized constructs are:

- **Assignment -**<br/>
  Corresponds to an assignment statement.<br/>

- **MultiTargetAssignment -**<br/>
  Corresponds to an assignment statement with multiple targets.<br/>
  Example:<br/>
  a, b = 1, 2<br/>
  Also counts as an Assignment construct.<br/>

- **ChainedCompare -**<br/>
  Corresponds to a chained sequence of comparison expressions.<br/>
  Example:<br/>
  1 < x <= y < 10<br/>

- **KeywordArgumentUsage -**<br/>
  Corresponds to a function call with a keyword argument (argname=value syntax).<br/>
  Example:<br/>
  print('abc', end='')<br/>

- **Subscription -**<br/>
  Referring to an item (or multiple items) of a sequence or mapping object.<br/>
  Example:<br/>
  a[1]<br/>
  line[4:-2]<br/>
  table['abc']<br/>

- **Slicing -**<br/>
  Usage of slicing ( [start?:end?:stride?] ) in subscription.<br/>
  Example:<br/>
  items[:]<br/>
  line[1:-1]<br/>
  array[::2]<br/>

- **IfExpression -**<br/>
  Usage of an if-expression.<br/>
  Example:<br/>
  a if a > b else b<br/>

- **Comprehension -**<br/>
  Corresponds to any usage of list, set or dictionary comprehension or generator expression.<br/>

- **FilteredComprehension -**<br/>
  Corresponds to a comprehension containing one or more if's.<br/>
  Example:<br/>
  [x for x in xlist if x > 0]<br/>
  Also counts as a Comprehension construct.<br/>

- **MultilevelComprehension -**<br/>
  Corresponds to a comprehension containing twoor more for's.<br/>
  Examples:<br/>
  [(x,y) for x in xlist for y in ylist][x for y in z for x in y]<br/>
  Also counts as a Comprehension construct.<br/>

- **ListDisplay -**<br/>
  Corresponds to a new list object, specified by either a list of expressions or a comprehension enclosed in square brackets.<br/>
  Examples:<br/>
  [1, 2, 3][2*x for x in y]<br/>

- **ListComprehension -**<br/>
  A specialized form of a ListDisplay construct. Also counts as a Comprehension construct.<br/>

- **SetDisplay -**<br/>
  Corresponds to a new set object, specified by either a list of expressions or a comprehension enclosed in curly braces.<br/>
  Examples:<br/>
  {1, 2, 3}<br/>
  {x\*\*2 for x in y}<br/>

- **SetComprehension -**<br/>
  A specialized form of a SetDisplay construct. Also counts as a Comprehension construct.<br/>

- **DictionaryDisplay -**<br/>
  Corresponds to a possibly empty series of key:datum pairs (possibly produced through a comprehension) enclosed in curly braces, defining a new dictionary object.<br/>
  Examples:<br/>
  {1:'a', 2:'b', 3:'c'}<br/>
  {x:bin(x) for x in y}<br/>

- **DictionaryComprehension -**<br/>
  A specialized form of a DictionaryDisplay construct. Also counts as a Comprehension construct.<br/>

- **GeneratorExpression -**<br/>
  A comprehension enclosed in parentheses, producing a new generator object. Also counts as a Comprehension construct.<br/>

- **FunctionDef -**<br/>
  Definition of a function.<br/>

- **ClassDef -**<br/>
  Definition of a class.<br/>

## 2. Statements

### Currently detected/recognized statements are:<br/>

- While
- For
- Return
- If
- Continue
- Break
- Try
- With
- Raise
- Pass
- Assert
- Del
- Yield

## 3. Expressions

### Currently detected/recognized Expressions are:<br/>

- Unary
- Binary
- Boolean
- Compare

## 4. Functions

- Recognises function definitions and calls

## 5. Imports

- Recognises imported modules
