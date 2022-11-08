# -*- coding:utf-8 -*-
# Copyright @FridrichMethod

from sympy import *


def latex_number(expr):
    return latex(expr, mul_symbol='times')


# Input

# Define equation
equation = [x.strip() for x in
            'W = (-Q_V*m-Q_N-Q_M)/Dt-rho*V*C'
            .split('=')]

# Define variable
variable = [
    ('Q_V = -26.414 +- 0', 'Q_V'),
    ('m = 0.9547 +- 0.0004/sqrt(3)', 'm'),
    ('Q_N = -0.323 +- 3.243*0.0004/sqrt(3)', 'Q_\\ce{Ni}'),
    ('Q_M = -0.01 +- 0.0002*16.736/sqrt(3)', 'Q_\\text{cotton}'),
    ('rho = 0.99865 +- 0', '\\rho_\\ce{H2O}'),
    ('V = 3000 +- 0.01', 'V'),
    ('C = 4.1824e-3 +- 0', 'C_\\ce{H2O}'),
    ('Dt = 1.770 +- 0.009', '\\Delta T')
]

# Set digits of results
result_digit = {'mu': 4,
                'sigma': 2}

# Set units of results
result_unit = '\\text{kJ}/{}^\\circ\\text{C}'

# Print separately or integrally
separate = 1

# Insert numbers or not
insert = 1

# Include equation number or not
include_equation_number = 1

# Parse

input_sym = []
input_unc = []
input_fullsym = []
input_fullunc = []
input_mu = []
input_sigma = []
input_fullmu = []
input_fullsigma = []

for x in variable:
    input_symbol = x[0].split('=')
    input_value = input_symbol[1].split('+-')
    input_sym.append(input_symbol[0].strip())
    input_unc.append(f'sigma_{input_symbol[0].strip()}')
    input_fullsym.append(x[1].strip())
    input_fullunc.append(f'\\sigma_{{{x[1].strip()}}}')
    input_mu.append(input_value[0].strip())
    input_sigma.append(input_value[1].strip())
    input_fullmu.append(f'\\left({latex_number(sympify(input_value[0].strip()))}\\right)')
    input_fullsigma.append(latex_number(sympify(input_value[1].strip()).evalf(2)))

syms = symbols(input_sym)
uncs = symbols(input_unc)
output_symbol = dict(zip(syms + uncs, input_fullsym + input_fullunc))
output_number = dict(zip(syms + uncs, input_mu + input_sigma))
output_value = dict(zip(syms + uncs, input_fullmu + input_fullsigma))
check_unc = dict(zip(syms, sympify(input_sigma)))
equation_left = equation[0]
equation_right = sympify(equation[1])


# Print

def latex_symbol(expr):
    return latex(expr, inv_trig_style='full', ln_notation=True, fold_func_brackets=True, symbol_names=output_symbol)


def latex_value(expr):
    return latex(expr, inv_trig_style='full', ln_notation=True, fold_func_brackets=True, mul_symbol='times',
                 symbol_names=output_value)


if insert:
    if not separate:
        print('''\\begin{equation}
\\begin{aligned}''' if include_equation_number else '''\\begin{equation*}
\\begin{aligned}''')
        print(equation_left, end='&=')
        print(latex_symbol(equation_right), end='=')
        print(latex_value(equation_right), end='=')
        result_mu = latex_number(equation_right.evalf(result_digit['mu'], subs=output_number))
        if result_unit == 1:
            print(result_mu + '\\\\\n\\\\')
        else:
            print(f'{result_mu}\\ ' + result_unit + '\\\\\n\\\\')

        pdv_number = []
        for sym in syms:
            if check_unc[sym]:
                print(f'\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }}', end='&=')
                pdv = simplify(diff(equation_right, sym))
                print(latex_symbol(pdv), end='=')
                print(latex_value(pdv), end='=')
                num = pdv.subs(output_number)
                pdv_number.append(num)
                print(latex_number(num.evalf(2)), end='\\\\\n')
            else:
                pdv_number.append(sympify(0))
        print('\\\\')

        print(f'\\sigma_{{{equation_left}}}&=\\sqrt{{'
              + '+'.join(
            f'\\left(\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }} {fullunc}\\right)^2' for
            sym, fullunc in zip(syms, input_fullunc) if check_unc[sym])
              + '}\\\\')
        print('&=\\sqrt{'
              + '+'.join(f'\\left({latex_number(num.evalf(2))} \\times {output_value[unc]}\\right)^2' for num, unc in
                         zip(pdv_number, uncs) if sympify(output_number[unc]))
              + '}\\\\')
        print('&=\\sqrt{'
              + '+'.join(f'\\left({(num*sympify(output_number[unc])).evalf(2)}\\right)^2' for num, unc in
                         zip(pdv_number, uncs) if sympify(output_number[unc]))
              + '}\\\\')
        result_sigma = latex_number(
            sqrt(sum((num * sympify(sigma)) ** 2 for num, sigma in zip(pdv_number, input_sigma))).evalf(
                result_digit['sigma']))
        print('&=', end='')
        if result_unit == 1:
            print(result_sigma + '\\\\\n\\\\')
        else:
            print(f'{result_sigma}\\ ' + result_unit + '\\\\\n\\\\')


        # Result

        if result_unit == 1:
            print(f'{equation_left}&={result_mu} \\pm {result_sigma}')
        else:
            print(f'{equation_left}&=\\left ({result_mu} \\pm {result_sigma} \\right )\\ ' + result_unit)
        print('''\\end{aligned}
\\end{equation}''' if include_equation_number else'''\\end{aligned}
\\end{equation*}''')

    else:
        print('\\begin{equation}' if include_equation_number else '\\begin{equation*}')
        print(equation_left, end='=')
        print(latex_symbol(equation_right), end='=')
        print(latex_value(equation_right), end='=')
        result_mu = latex_number(equation_right.evalf(result_digit['mu'], subs=output_number))
        if result_unit == 1:
            print(result_mu)
        else:
            print(f'{result_mu}\\ ' + result_unit)
        print('\\end{equation}' if include_equation_number else '\\end{equation*}')

        pdv_number = []
        print('''
\\begin{equation}
\\begin{aligned}''' if include_equation_number else '''
\\begin{equation*}
\\begin{aligned}''')
        for sym in syms:
            if check_unc[sym]:
                print(f'\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }}', end='&=')
                pdv = simplify(diff(equation_right, sym))
                print(latex_symbol(pdv), end='=')
                print(latex_value(pdv), end='=')
                num = pdv.subs(output_number)
                pdv_number.append(num)
                print(latex_number(num.evalf(2)), end='\\\\\n')
            else:
                pdv_number.append(sympify(0))
        print('''\\end{aligned}
\\end{equation}
''' if include_equation_number else '''\\end{aligned}
\\end{equation*}
''')

        print('''\\begin{equation}
\\begin{aligned}''' if include_equation_number else '''\\begin{equation*}
\\begin{aligned}''')
        print(f'\\sigma_{{{equation_left}}}&=\\sqrt{{'
              + '+'.join(
            f'\\left(\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }} {fullunc}\\right)^2' for
            sym, fullunc in zip(syms, input_fullunc) if check_unc[sym])
              + '}\\\\')
        print('&=\\sqrt{'
              + '+'.join(f'\\left({latex_number(num.evalf(2))} \\times {output_value[unc]}\\right)^2' for num, unc in
                         zip(pdv_number, uncs) if sympify(output_number[unc]))
              + '}\\\\')
        print('&=\\sqrt{'
              + '+'.join(f'\\left({(num * sympify(output_number[unc])).evalf(2)}\\right)^2' for num, unc in
                         zip(pdv_number, uncs) if sympify(output_number[unc]))
              + '}\\\\')
        result_sigma = latex_number(
            sqrt(sum((num * sympify(sigma)) ** 2 for num, sigma in zip(pdv_number, input_sigma))).evalf(
                result_digit['sigma']))
        print('&=', end='')
        if result_unit == 1:
            print(result_sigma)
        else:
            print(f'{result_sigma}\\ ' + result_unit)
        print('''\\end{aligned}
\\end{equation}
''' if include_equation_number else '''\\end{aligned}
\\end{equation*}
''')


        # Result

        print('\\begin{equation}' if include_equation_number else '\\begin{equation*}')
        if result_unit == 1:
            print(f'{equation_left}={result_mu} \\pm {result_sigma}')
        else:
            print(f'{equation_left}=\\left ({result_mu} \\pm {result_sigma} \\right )\\ ' + result_unit)
        print('\\end{equation}' if include_equation_number else '\\end{equation}*')

else:
    if not separate:
        print('''\\begin{equation}
\\begin{aligned}''' if include_equation_number else '''\\begin{equation*}
\\begin{aligned}''')
        print(equation_left, end='&=')
        print(latex_symbol(equation_right), end='=')
        result_mu = latex_number(equation_right.evalf(result_digit['mu'], subs=output_number))
        if result_unit == 1:
            print(result_mu + '\\\\\n\\\\')
        else:
            print(f'{result_mu}\\ ' + result_unit + '\\\\\n\\\\')

        pdv_number = []
        for sym in syms:
            if check_unc[sym]:
                print(f'\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }}', end='&=')
                pdv = simplify(diff(equation_right, sym))
                print(latex_symbol(pdv), end='=')
                num = pdv.subs(output_number)
                pdv_number.append(num)
                print(latex_number(num.evalf(2)), end='\\\\\n')
            else:
                pdv_number.append(sympify(0))
        print('\\\\')

        print(f'\\sigma_{{{equation_left}}}&=\\sqrt{{'
              + '+'.join(
            f'\\left(\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }} {fullunc}\\right)^2' for
            sym, fullunc in zip(syms, input_fullunc) if check_unc[sym])
              + '}\\\\')
        print('&=\\sqrt{'
              + '+'.join(f'\\left({(num * sympify(output_number[unc])).evalf(2)}\\right)^2' for num, unc in
                         zip(pdv_number, uncs) if sympify(output_number[unc]))
              + '}\\\\')
        result_sigma = latex_number(
            sqrt(sum((num * sympify(sigma)) ** 2 for num, sigma in zip(pdv_number, input_sigma))).evalf(
                result_digit['sigma']))
        print('&=', end='')
        if result_unit == 1:
            print(result_sigma + '\\\\\n\\\\')
        else:
            print(f'{result_sigma}\\ ' + result_unit + '\\\\\n\\\\')


        # Result

        if result_unit == 1:
            print(f'{equation_left}&={result_mu} \\pm {result_sigma}')
        else:
            print(f'{equation_left}&=\\left ({result_mu} \\pm {result_sigma} \\right )\\ ' + result_unit)
        print('''\\end{aligned}
\\end{equation}''' if include_equation_number else '''\\end{aligned}
\\end{equation*}''')

    else:
        print('\\begin{equation}' if include_equation_number else '\\begin{equation*}')
        print(equation_left, end='=')
        print(latex_symbol(equation_right), end='=')
        result_mu = latex_number(equation_right.evalf(result_digit['mu'], subs=output_number))
        if result_unit == 1:
            print(result_mu)
        else:
            print(f'{result_mu}\\ ' + result_unit)
        print('\\end{equation}' if include_equation_number else '\\end{equation*}')

        pdv_number = []
        print('''
\\begin{equation}
\\begin{aligned}''' if include_equation_number else '''
\\begin{equation*}
\\begin{aligned}''')
        for sym in syms:
            if check_unc[sym]:
                print(f'\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }}', end='&=')
                pdv = simplify(diff(equation_right, sym))
                print(latex_symbol(pdv), end='=')
                num = pdv.subs(output_number)
                pdv_number.append(num)
                print(latex_number(num.evalf(2)), end='\\\\\n')
            else:
                pdv_number.append(sympify(0))
        print('''\\end{aligned}
\\end{equation}
''' if include_equation_number else '''\\end{aligned}
\\end{equation*}
''')

        print('''\\begin{equation}
\\begin{aligned}''' if include_equation_number else '''\\begin{equation*}
\\begin{aligned}''')
        print(f'\\sigma_{{{equation_left}}}&=\\sqrt{{'
              + '+'.join(
            f'\\left(\\frac{{\\partial {equation_left} }}{{\\partial {output_symbol[sym]} }} {fullunc}\\right)^2' for
            sym, fullunc in zip(syms, input_fullunc) if check_unc[sym])
              + '}\\\\')
        print('&=\\sqrt{'
              + '+'.join(f'\\left({(num * sympify(output_number[unc])).evalf(2)}\\right)^2' for num, unc in
                         zip(pdv_number, uncs) if sympify(output_number[unc]))
              + '}\\\\')
        result_sigma = latex_number(
            sqrt(sum((num * sympify(sigma)) ** 2 for num, sigma in zip(pdv_number, input_sigma))).evalf(
                result_digit['sigma']))
        print('&=', end='')
        if result_unit == 1:
            print(result_sigma)
        else:
            print(f'{result_sigma}\\ ' + result_unit)
        print('''\\end{aligned}
\\end{equation}
''' if include_equation_number else '''\\end{aligned}
\\end{equation*}
''')


        # Result

        print('\\begin{equation}' if include_equation_number else '\\begin{equation*}')
        if result_unit == 1:
            print(f'{equation_left}={result_mu} \\pm {result_sigma}')
        else:
            print(f'{equation_left}=\\left ({result_mu} \\pm {result_sigma} \\right )\\ ' + result_unit)
        print('\\end{equation}' if include_equation_number else '\\end{equation*}')
