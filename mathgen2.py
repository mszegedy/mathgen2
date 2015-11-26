#!/usr/bin/python

import sys,random

class func:
    '''Stores a mathematical operator, and a list of arguments it's acting on.'''
    def __init__(self,op,args=[]):
        self.op   = op   # the operator that is acting on the list of arguments; a string
        self.args = args # the list of arguments to the operator
    def arg_error_message(self):
        if self.op == 'sign':
            return "The sign function is unary."
        elif self.op == 'x':
            return "x is not supposed to have any args."
        elif self.op == 'abs':
            return "abs is unary."
        elif self.op == '-':
            return "Minus is unary."
        elif self.op == '/':
            return "Division is unary. It's 1/x."
        elif self.op == '^':
            return "Exponentiation is 2-ary. The first argument is the base, and the second argument is the exponent."
        elif self.op == 'exp':
            return "exp is unary."
        elif self.op == 'ln':
            return "ln is unary."
        else:
            return "arg_error_message() was used inappropriately."
    def latex(self):
        '''Returns a LaTeX string that corresponds to the content of the expression.'''
        if self.op == 'sign':
            assert len(self.args) == 0, self.arg_error_message()
            retstring = "\\mathrm{sgn}\\left("
            if isinstance(self.args[0],int):
                retstring += str(self.args[0])
            elif isinstance(self.args[0],func):
                retrstring += self.args[0].latex()
            return retstring+"\\right)"
        elif self.op == 'x':
            assert len(self.args) == 0, self.arg_error_message()
            return "x"
        elif self.op == 'abs':
            assert len(self.args) == 0, self.arg_error_message()
            retstr = "\\left\\|"
            if isinstance(self.args[0],int):
                retstr += str(self.args[0])
            elif isinstance(self.args[0],func):
                retstr += self.args[0].latex()
            return retstr+"\\right\\|"
        elif self.op == '+':
            retstr = ''
            for arg in self.args:
                if isinstance(arg,int):
                    retstr += '+ '+str(arg)
                elif isinstance(arg,func):
                    if arg.op == '-':
                        assert len(arg.args) == 1, arg.arg_error_message()
                        if isinstance(arg.args[0],int):
                            retstr += '- ',str(arg.args[0])
                        elif isinstance(arg.args[0],func):
                            retstr += '- ',arg.args[0].latex()
                    else:
                        retstr += '+ '+arg.latex()
                return retstr[2:]
        elif self.op == '-':
            assert len(self.args) == 1, self.arg_error_message()
            if isinstance(self.args[0],int):
                return '-'+str(self.args[0])
            elif isinstance(self.args[0],func):
                return '-'+self.args[0].latex()
        elif self.op == '*':
            retstr = ''
            dividends = [arg for arg in self.args if isinstance(arg,int)]+[funcarg for funcarg in [arg for arg in self.args if isinstance(arg,func)] if funcarg.op != '/'] # Every argument that isn't a func with an op of '/'
            divisors = [funcarg for funcarg in [arg for arg in self.args if isinstance(arg,func)] if funcarg.op == '/'] # Every argument that is a func with an op of '/'
            if len(divisors) != 0:
                retstr += '\\frac{'
            for arg in dividends:
                if isinstance(arg,int):
                    retstr += str(arg)
                elif isinstance(arg,func):
                    retstr += '\\left('+arg.latex()+'\\right)'
            if len(divisors) != 0:
                retstr += '}{'
                for arg in divisors:
                    assert isinstance(arg,func), "There aren't supposed to be any non-func objects in divisors."
                    assert len(arg.args) == 1, arg.arg_error_message()
                    if isinstance(arg.args[0],int):
                        retstr += str(arg.args[0])
                    elif isinstance(arg.args[0],func):
                        retstr += '\\left('+arg.args[0].latex()+'\\right)'
                retstr += '}'
            return retstr
        elif self.op == '/':
            assert len(self.args) == 1, self.arg_error_message()
            if isinstance(self.args[0],int):
                return '\\frac{1}{'+str(self.args[0])+'}'
            elif isinstance(self.args[0],func):
                return '\\frac{1}{'+self.args[0].latex()+'}'
        elif self.op == 'sqrt':
            assert len(self.args) == 1, self.arg_error_message()
            retstr = '\\sqrt{'
            if isinstance(self.args[0],int):
                retstr += str(self.args[0])
            elif isinstance(self.args[0],func):
                retstr += self.args[0].latex()
            return retstr+'}'
        elif self.op == '^':
            assert len(self.args) == 2, self.arg_error_message()
            assert isinstance(self.args[1],int), "Exponents must be integers. Sorry."
            if isinstance(self.args[0],int):
                return str(self.args[0]**self.args[1])
            elif isinstance(self.args[0],func):
                return '\\left('+self.args[0].latex()+'\\right)^{'+str(self.args[1])+'}'
        elif self.op == 'exp':
            assert len(self.args) == 1, self.arg_error_message()
            retstr = 'e^{'
            if isinstance(self.args[0],int):
                retstr += str(self.args[0])
            elif isinstance(self.args[0],func):
                retstr += self.args[0].latex()
            return retstr+'}'
        elif self.op == 'ln':
            assert len(self.args) == 1, self.arg_error_message()
            retstr = '\\ln\\left('
            if isinstance(self.args[0],int):
                retstr += str(self.args[0])
            elif isinstance(self.args[0],func):
                retstr += self.args[0].latex()
            return retstr+'\\right)'

def derivative(expr):
    '''Returns the derivative of a mathematical expression.'''
    assert isinstance(expr,func) or isinstance(expr,int), "You can only take a derivative of a func object or an integer."
    try:
        assert expr.op in ('sign','x','abs','+','-','*','/','^','sqrt','exp','ln'), "Expression uses nonexistent operator: "+expr.op
    except AttributeError:
        assert isinstance(expr,int), "You can only take a derivative of a func object or an integer."
    if isinstance(expr,int):
        return 0
    elif expr.op == 'sign':
        assert len(expr.args) == 1, expr.arg_error_message()
        return 0
    elif expr.op == 'x':
        assert len(expr.args) == 0, expr.arg_error_message()
        return 1
    elif expr.op == 'abs':
        assert len(expr.args) == 1, expr.arg_error_message()
        return func('*',[derivative(args[0]),func('sign',[args[0]])])
    elif expr.op == '+':
        return func('+',[derivative(arg) for arg in expr.args])
    elif expr.op == '-': # this is unary minus: it takes only one argument
        assert len(expr.args) == 1, expr.arg_error_message()
        return func('-',[derivative(expr.args[0])])
    elif expr.op == '*':
        return func('+',[func('*',[derivative(expr.args[index])]+[otherarg for otherindex,otherarg in enumerate(expr.args) if index != otherindex]) for index in range(len(expr.args))])
    elif expr.op == '/': # this is unary division (1/whatever): it takes only one argument
        assert len(expr.args) == 1, expr.arg_error_message()
        return func('-',[func('*',[derivative(expr.args[0]),func('/',[func('^',[expr.args[0],2])])])])
    elif expr.op == '^':
        assert len(expr.args) == 2, expr.arg_error_message()
        assert isinstance(expr.args[1],int), "Exponents must be integers. Sorry."
        return func('*',[derivative(expr.args[1]),expr.args[0],func('^',[expr.args[0],expr.args[1]-1])])
    elif expr.op == 'sqrt':
        assert len(expr.args) == 1, expr.arg_error_message()
        return func('-',[func('/',[func('*',[2,func('sqrt',[expr])])])])
    elif expr.op == 'exp':
        assert len(expr.args) == 1, expr.arg_error_message()
        return func('*',[derivative(expr.args[0]),expr])
    elif expr.op == 'ln':
        assert len(expr.args) == 1, expr.arg_error_message()
        return func('*',[derivative(expr.args[0]),func('/',[expr])])
    else:
        print "Sorry, I don't understand the expression."
        sys.exit()
def simplify(expr):
    '''Returns a simplified version of a mathematical expression.'''
    assert isinstance(expr,func) or isinstance(expr,int), "You can only simplify a func object or an integer."
    if isinstance(expr,int):
        return expr
    else:
        assert expr.op in ('x','+','-','*','/','^','sqrt','exp','ln'), "Expression uses nonexistent operator: "+expr.op
        expr.args = [simplify(arg) for arg in expr.args]
        if expr.op == 'sign' and isinstance(expr.args[0],int):
            assert len(expr.args) == 1, expr.arg_error_message()
            if expr.args[0] > 0:
                return 1
            elif expr.args[0] == 0:
                return 0
            elif expr.args[0] < 0:
                return -1
            else:
                print "If you are getting this message, you have tampered with how the sign function is simplified. It was not a wise choice."
                sys.exit()
        elif expr.op == '+' and 0 in expr.args:
            return func('+',[arg for arg in expr.args if arg != 0])
        elif expr.op == 'abs' and 0 in expr.args:
            return 0
        elif expr.op == '-':
            assert len(expr.args) == 1, expr.arg_error_message()
            if isinstance(expr.args[0],int):
                return -expr.args[0]
            elif isinstance(expr.args[0],func):
                if expr.args[0].op == '-':
                    assert len(expr.args[0].args) == 1, expr.arg_error_message()
                    return expr.args[0].args[0]
        elif expr.op == '*':
            if 0 in expr.args:
                return 0
            elif 1 in expr.args:
                return func('*',[arg for arg in expr.args if arg != 1])
            elif -1 in expr.args:
                minuscount = len([arg for arg in expr.args if arg == -1])
                if minuscount % 2:
                    return func('-',[func('*',[arg for arg in expr.args if not arg in (-1,1)])])
                else:
                    return func('*',[arg for arg in expr.args if not arg in (-1,1)])
            elif len([arg for arg in expr.args if isinstance(arg,int)]) > 1:
                return func('*',[reduce(lambda a,b:a*b, [arg for arg in expr.args if isinstance(arg,int)])]+[arg for arg in expr.args if not isinstance(arg,int)])
        elif expr.op == '/':
            assert len(expr.args) == 1, expr.arg_error_message()
            if 0 in expr.args:
                raise ZeroDivisionError
            elif isinstance(expr.args[0],func):
                if expr.args[0].op == '/':
                    assert len(expr.args[0].args) == 1, expr.arg_error_message()
                    return expr.args[0].args[0]
        elif expr.op == '^':
            assert len(expr.args) == 2, expr.arg_error_message()
            assert isinstance(expr.args[1],int), expr.arg_error_message()
            if expr.args[1] == 0:
                return 1
            elif expr.args[1] == 2:
                if isinstance(expr.args[0],func):
                    if expr.args[0].op == 'sqrt':
                        assert len(expr.args[0].args) == 1, expr.arg_error_message()
                        return func('abs',expr.args[0].args[0])
        elif expr.op == 'exp':
            assert len(expr.args) == 1, "exp is unary."
            if 0 in expr.args:
                return 1
            elif isinstance(expr.args[0],func):
                if expr.args[0].op == 'ln':
                    assert len(expr.args[0].args) == 1, expr.arg_error_message()
                    return expr.args[0].args[0]
        elif expr.op == 'ln':
            assert len(expr.args) == 1, expr.arg_error_message()
            if isinstance(expr.args[0],int):
                if expr.args[0] <= 0:
                    raise ValueError
            elif isinstance(expr.args[0],func):
                if expr.args[0].op == 'exp':
                    assert len(expr.args[0].args) == 1, expr.arg_error_message()
                    return expr.args[0].args[0]
        return expr
def compose(a,b):
    '''Composes a with b.'''
    assert isinstance(a,func) and isinstance(b,func), "Both arguments need to be funcs."
    for index,arg in enumerate(a.args):
        if arg == func('x'):
            a.args[index] = b
        elif isinstance(arg,func):
            arg = compose(arg,b)
    return a

try:
    probnum = int(sys.argv[1])
except ValueError:
    print 'The first argument must be the number of problems.'
out = open('problems.tex','w')
out.write('\\documentclass[12pt]{article}\n\\usepackage[margin=2cm]{geometry}\n\\usepackage{microtype}\n\\title{'+str(probnum)+' Math Problems}\\begin{document}\n\\maketitle\n\\begin{enumerate}\n')
for index in xrange(probnum):
    problemtype = random.choice(('invert','differentiate','integrate'))
    if problemtype == 'invert':
        out.write('\\item Invert:\n')
        problem = func('x')
        for jndex in xrange(random.choice(xrange(10,20))):
            problem = compose(random.choice((func('exp',[func('x')]),
                                             func('ln',[func('x')]),
                                             func('*',[random.choice(range(-9,0)+range(1,10)),
                                                       func('x')]),
                                             func('+',[func('x'),
                                                       random.choice(range(-9,0)+range(1,10))]),
                                             func('/',[func('x')]),
                                             func('-',[func('x')]),
                                             func('sqrt',[func('x')]),
                                             func('+',[func('*',[random.choice(range(-9,0)+range(1,10)),
                                                                 func('^',[func('x'),2])]),
                                                       func('*',[random.choice(range(-9,0)+range(1,10)),
                                                                 func('x')]),
                                                       random.choice(range(-9,0)+range(1,10))]))),
                              problem)
        problem = simplify(problem)
        out.write('$\\displaystyle '+problem.latex()+'$\n')
    elif problemtype == 'differentiate':
        out.write('\\item\n')
        problem = func('x')
        for jndex in xrange(random.choice(xrange(10,20))):
            problem = compose(random.choice((func('exp',[func('x')]),
                                             func('ln',[func('x')]),
                                             func('*',[random.choice(range(-9,0)+range(1,10)),
                                                       func('x')]),
                                             func('+',[func('x'),
                                                       random.choice(range(-9,0)+range(1,10))]),
                                             func('/',[func('x')]),
                                             func('-',[func('x')]),
                                             func('sqrt',[func('x')]),
                                             func('+',[func('*',[random.choice(range(-9,0)+range(1,10)),
                                                                 func('^',[func('x'),2])]),
                                                       func('*',[random.choice(range(-9,0)+range(1,10)),
                                                                 func('x')]),
                                                       random.choice(range(-9,0)+range(1,10))]))),
                              problem)
        problem = simplify(problem)
        out.write('$\\displaystyle \\frac{d}{dx} '+problem.latex()+'$\n')
    elif problemtype == 'integrate':
        out.write('\\item Invert:\n')
        problem = func('x')
        for jndex in xrange(random.choice(xrange(10,20))):
            problem = compose(random.choice((func('exp',[func('x')]),
                                             func('ln',[func('x')]),
                                             func('*',[random.choice(range(-9,0)+range(1,10)),
                                                       func('x')]),
                                             func('+',[func('x'),
                                                       random.choice(range(-9,0)+range(1,10))]),
                                             func('/',[func('x')]),
                                             func('-',[func('x')]),
                                             func('sqrt',[func('x')]),
                                             func('+',[func('*',[random.choice(range(-9,0)+range(1,10)),
                                                                 func('^',[func('x'),2])]),
                                                       func('*',[random.choice(range(-9,0)+range(1,10)),
                                                                 func('x')]),
                                                       random.choice(range(-9,0)+range(1,10))]))),
                              problem)
        problem = simplify(derivative(problem))
        out.write('$\\displaystyle \int '+problem.latex()+' dx$\n')
out.write('\\end{enumerate}\n\\end{document}\n')
out.close()
