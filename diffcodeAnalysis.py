from collections import deque
import ast
import json
from collections import defaultdict


def MultiTargetAssignment(ast_node):
    '''
    Detects usage of an assignment with multiple targets
    Example:
        a, b = 1, 2
    '''
    return isinstance(ast_node.targets[0], ast.Tuple)


def FilteredComprehension(ast_node):
    '''
    Detects usage of a comprehension construct with 1 or more if's.
    Example:
        [x for x in xlist if x > 0]
    '''
    for c in ast_node.generators:
        if len(c.ifs) > 0:
            return True
    return False


def MultilevelComprehension(ast_node):
    '''
    Detects usage of a comprehension construct with 2 or more for's.
    Example:
        [(x,y) for x in xlist for y in ylist]
    '''
    return len(ast_node.generators) > 1


def ChainedCompare(ast_node):
    '''
    Detects usage of a chained sequence of comparisons.
    Example:
        1 < x < y <= 5
    '''
    return len(ast_node.ops) > 1


def KeywordArgumentUsage(ast_node):
    '''
    Detects usage of a keyword argument in a function call.
    Example:
        print('abc', end='')
        #            ^^^^^^
    '''
    return len(ast_node.keywords) > 0


comprehension = 'Comprehension', FilteredComprehension, MultilevelComprehension

# A helper function


def makeComprehensionSpec(collection_type):
    return (collection_type + 'Comprehension',
            collection_type + 'Display',
            *comprehension)


# A map defining construct names for listed AST node types and/or checks
# that must be performed on such AST nodes. In the latter case, if a node
# satisfies the test, the name of the test function is used as the detected
# construct name.
construct_def_map = {
    ast.FunctionDef:   ('FunctionDef',),
    ast.ClassDef:      ('ClassDef',),
    ast.IfExp:         ('IfExpression',),
    ast.Assign:        ('Assignment', MultiTargetAssignment),
    ast.AugAssign:     ('AugmentedAssignment',),
    ast.List:          ('ListDisplay',),
    ast.ListComp:      makeComprehensionSpec('List'),
    ast.Set:           ('SetDisplay',),
    ast.SetComp:       makeComprehensionSpec('Set'),
    ast.Dict:          ('DictionaryDisplay',),
    ast.DictComp:      makeComprehensionSpec('Dictionary'),
    ast.GeneratorExp:  ('GeneratorExpression', *comprehension),
    ast.Compare:       (ChainedCompare,),
    ast.Subscript:     ('Subscription',),
    ast.Slice:         ('Slicing',),
    ast.Call:          (KeywordArgumentUsage,)
}


def getAllConstructs(tree):
    result = defaultdict(int)

    for node in ast.walk(tree):
        if type(node) in construct_def_map:
            for x in construct_def_map[type(node)]:
                if isinstance(x, str):
                    result[x] += 1
                elif x(node):
                    result[x.__name__] += 1

    return dict(result)


def countNodesOfGivenTypes(tree, node_types):
    result = defaultdict(int)

    for node in ast.walk(tree):
        if type(node) in node_types:
            result[type(node).__name__] += 1

    return dict(result)


statementNodeTypes = frozenset([ast.While,
                                ast.For,
                                ast.Return,
                                ast.If,
                                ast.Continue,
                                ast.Break,
                                ast.Try,
                                ast.With,
                                ast.Raise,
                                ast.Pass,
                                ast.Assert,
                                ast.Del,
                                ast.Yield])

# Collect all statements


def getAllStatements(tree):
    return countNodesOfGivenTypes(tree, statementNodeTypes)


def getAllExpr(tree):
    result = defaultdict(int)
    for node in ast.walk(tree):
        if isinstance(node, ast.UnaryOp) or isinstance(node, ast.BinOp) or isinstance(node, ast.BoolOp):
            result[type(node.op).__name__] += 1
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                result[type(op).__name__] += 1
    return dict(result)


class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        # print(self._name)
        return ''.join(self._name)  # was ".".join() removing . option

    @name.deleter
    def name(self):
        self._name.clear()

    # Updating to only show obj for ids
    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            # hacking for demonstration list of functions
            # self._name.appendleft(node.value.id)
            self._name.appendleft("")
            # print(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def getFuncCalls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)
    result = defaultdict(int)
    for item in func_calls:
        result[item] += 1
    return dict(result)


def getFuncDefs(tree):
    r = set()
    for node in ast.walk(tree):
        if type(node) is ast.FunctionDef:
            r.add(node.name)

    return list(r)


def getAllImports(a):
    """Gather all imported module names"""
    if not isinstance(a, ast.AST):
        return set()
    imports = set()
    for child in ast.walk(a):
        if type(child) == ast.Import:
            for alias in child.names:
                imports.add(alias.name)
        elif type(child) == ast.ImportFrom:
            for alias in child.names:  # these are all functions
                imports.add(child.module + "." + alias.name)
    result = {}
    for item in imports:
        result[item] = 1  # True
    return result


def simplify(d):
    result = {}
    for key in d:
        if d[key] != {}:
            result[key] = d[key]
    return result


def code_features(src):
    tree = ast.parse(src)
    funcCalls = getFuncCalls(tree)
    result = {
        "statements":  getAllStatements(tree),
        "functions":   funcCalls,
        "imports":     getAllImports(tree),
        "expressions": getAllExpr(tree),
        "constructs": getAllConstructs(tree)
    }
    definedFunctions = getFuncDefs(tree)
    for df in definedFunctions:
        if df in funcCalls:
            del funcCalls[df]
    return simplify(result)


def getIndexPage():
    defaultGetResponse = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width" />
        <title>Python Code Analysis</title>
    </head>
    <body>
        <div id="app">
        <h3>Given Code</h3>
        <textarea v-model="givenText"></textarea>
        <h3>Solution Code</h3>
        <textarea v-model="solutionText"></textarea>
        <br />
        <button @click="postData">Analyze</button>
        <br />
        <h3>Solutions to post</h3>
        <pre>{{ solutions }}</pre>
        <hr />
        <h3>Code Analysis Result</h3>
        <pre>{{ analysisResult }}</pre>
        </div>
        <script src="https://unpkg.com/vue"></script>
        <script>
        var app = new Vue({
            el: "#app",
            data: {
            givenText: "print(x)",
            solutionText: "print(x)",
            analysisResult: ""
            },
            computed: {
            solutions: function() {
                return {
                givenCode: this.givenText,
                solutionCode: this.solutionText
                };
            }
            },
            methods: {
            postData: function() {
                var data = this.solutions;
                const gatewayUrl = "";
                fetch(gatewayUrl, {
                method: "POST", // the method
                body: JSON.stringify(data) // the body
                })
                .then(response => {
                    // we received the response and print the status code
                    console.log(response.status);
                    // return response body as JSON
                    return response.json();
                })
                .then(json => {
                    // print the JSON
                    console.log(json);
                    this.analysisResult = json;
                });
            }
            }
        });
        </script>
    </body>
    </html>
    """
    return defaultGetResponse


def solution_features(parameters):
    givenCode = parameters.get("givenCode", "")
    givenFeatures = {}
    solutionCode = parameters.get("solutionCode", "")
    solutionFeatures = {}
    difference = {}
    givenNotebook = parameters.get("givenNotebook", None)
    solutionNotebook = parameters.get("solutionNotebook", "")
    targetCell = parameters.get("targetCell", 0)

    if givenNotebook:
        givenCode = "".join(givenNotebook["cells"][targetCell]['source'])
        print("Given code")
        print(givenCode)
        print("")

    if solutionNotebook:
        solutionCode = "".join(solutionNotebook["cells"][targetCell]['source'])
        print("Solution code")
        print(solutionCode)
        print("")

    if givenCode != "":
        src = givenCode
        try:
            givenFeatures = code_features(src)
        except:
            givenFeatures = {}

    if solutionCode != "":
        src = solutionCode
        solutionFeatures = code_features(src)

    result = {"givenCode": givenCode,
              "givenFeatures": givenFeatures}

    if solutionCode:
        result["solutionCode"] = solutionCode
        result["solutionFeatures"] = solutionFeatures

    if givenCode and solutionCode:
        # Calculate the difference by subracting keys present in both.
        difference = {}
        for featureType in ["statements", "functions", "imports", "expressions", "constructs"]:
            difference[featureType] = {k: v for k, v in solutionFeatures.get(
                featureType, {}).items() if k not in givenFeatures.get(featureType, {})}
            difference = simplify(difference)
            result['difference'] = difference
    return result


def lambda_handler(event, context):
    method = event.get('httpMethod', {})
    indexPage = getIndexPage()
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": indexPage
        }

    if method == 'POST':
        bodyContent = event.get('body', {})
        parsedBodyContent = json.loads(bodyContent)
        solFeatures = solution_features(parsedBodyContent)
        print(solFeatures)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(solFeatures)
        }
