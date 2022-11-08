# Uncertainty-Calculator

Help you get rid of Physical Chemistry Experiment in CCME!


# Package Requirements

pip install sympy


# Define equation: 'string = expression'

'string' is the name of what you want to calculate.
'expression' is a formula written in Python format.

eg.

equation = [x.strip() for x in
            'W = (-Q_V*m-Q_N-Q_M)/Dt-rho*V*C'
            .split('=')]


# Define variable: ('symbol = mu +- sigma', 'string')

'symbol' is a temporary abbreviation of each variable, which should be consistent with 'expression', and will not exist in output.
'mu' is the expectation of each variable.
'sigma' is the standard deviation of each variable.
'string' is the name of each variable.

eg.

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


# Set digits of results: {'mu': integer, 'sigma': integer}

eg.

result_digit = {'mu': 4,
                'sigma': 2}


# Set units of results: result_unit = 'unit'

'unit' is a unit written in Python sympy.physics.units format, which should be set to 1 if what you want to calculate is dimensionless.

eg.

result_unit = J/K


# Print separately or integrally: separate = 0 or 1

eg.

separate = 1


# Insert numbers or not: insert = 0 or 1

eg.

insert = 1


# Output

LaTeX code of calculation details, including normal calculation, each partial derivative, total uncertainty combination, and the final result.

\begin{equation}
W=\frac{- C_\ce{H2O} \Delta T V \rho_\ce{H2O} - Q_\text{cotton} - Q_\ce{Ni} - Q_V m}{\Delta T}=\frac{- \left(0.0041824\right) \times \left(1.77\right) \times \left(3000\right) \times \left(0.99865\right) - \left(-0.01\right) - \left(-0.323\right) - \left(-26.414\right) \times \left(0.9547\right)}{\left(1.77\right)}=1.905\ \text{J} / \text{K}
\end{equation}

\begin{equation}
\begin{aligned}
\frac{\partial W }{\partial m }&=- \frac{Q_V}{\Delta T}=- \frac{\left(-26.414\right)}{\left(1.77\right)}=15.0\\
\frac{\partial W }{\partial Q_\ce{Ni} }&=- \frac{1}{\Delta T}=- \frac{1}{\left(1.77\right)}=-0.57\\
\frac{\partial W }{\partial Q_\text{cotton} }&=- \frac{1}{\Delta T}=- \frac{1}{\left(1.77\right)}=-0.57\\
\frac{\partial W }{\partial V }&=- C_\ce{H2O} \rho_\ce{H2O}=- \left(0.0041824\right) \times \left(0.99865\right)=-0.0042\\
\frac{\partial W }{\partial \Delta T }&=\frac{Q_\text{cotton} + Q_\ce{Ni} + Q_V m}{\Delta T^{2}}=\frac{\left(-0.01\right) + \left(-0.323\right) + \left(-26.414\right) \times \left(0.9547\right)}{\left(1.77\right)^{2}}=-8.2\\
\end{aligned}
\end{equation}

\begin{equation}
\begin{aligned}
\sigma_{W}&=\sqrt{\left(\frac{\partial W }{\partial m } \sigma_{m}\right)^2+\left(\frac{\partial W }{\partial Q_\ce{Ni} } \sigma_{Q_\ce{Ni}}\right)^2+\left(\frac{\partial W }{\partial Q_\text{cotton} } \sigma_{Q_\text{cotton}}\right)^2+\left(\frac{\partial W }{\partial V } \sigma_{V}\right)^2+\left(\frac{\partial W }{\partial \Delta T } \sigma_{\Delta T}\right)^2}\\
&=\sqrt{\left(15.0 \times 0.00023\right)^2+\left(-0.57 \times 0.00075\right)^2+\left(-0.57 \times 0.0019\right)^2+\left(-0.0042 \times 0.01\right)^2+\left(-8.2 \times 0.009\right)^2}\\
&=0.073\ \text{J} / \text{K}
\end{aligned}
\end{equation}

\begin{equation}
W=\left (1.905 \pm 0.073 \right )\ \text{J} / \text{K}
\end{equation}


# Acknowledgements
Sympy: https://github.com/sympy/sympy
