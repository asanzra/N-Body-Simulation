import numpy as np

#!!--------------------###--------------------!!--------------------###--------------------------!!
#######THIS FILE almost the same AS THE OTHERS WITH THE SAME NAME IN OTHER FOLDERS, but G=1#######
#!!--------------------###--------------------!!--------------------###--------------------------!!

# Definition of base units
METER = 1
KG = 1
SECOND = 1

# Definition of other units
G = 1
AU = 1.496e11 * METER
KM = 1e3 * METER
SUN_MASS = 1.989e30 * KG
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
YEAR = 365 * DAY

#Easy access to methods by variable, to avoid mistypes.
ODEINT = "odeint"
SOLVE_IVP = "solve_ivp"
METHODS = [ODEINT, SOLVE_IVP]