import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')

# Load data
dfV = pd.read_csv("C:/edgar/EDAN/4080V1.txt", sep="\t", usecols=[0])
dfI1 = pd.read_csv("C:/edgar/EDAN/4080V1.txt", sep="\t", usecols=[1])
dfI2 = pd.read_csv("C:/edgar/EDAN/120240V1.txt", sep="\t", usecols=[1])

#Define the fitting function
def getlin(x, a, b, c):  # x = VGS; a = K; b = Vt; c = n
    return np.piecewise(x,[x < 0.22, x >= 0.22],[lambda x: 0, lambda x: 0.5 * a * np.power(np.maximum(x - b, 0), c)])
# def getlin(x, a, b, c):  # x = VGS; a = K; b = Vt; c = n
#     return 0.5 * a * np.power(np.maximum(x - b, b-x), c)

# Bounds for the parameters (now fixed to be two lists: lower and upper bounds)
param_bounds = ([0, 0, 0], [np.inf, 1, 2])  # K >= 0, Vt up to 0.04, n up to 2

# Perform curve fitting for dfI1
[K, Vt, n1], pcov = curve_fit(getlin, dfV.to_numpy().flatten(), dfI1.to_numpy().flatten(), bounds=param_bounds)

# Output the fitted parameters
print("K =", K)
print("Vt =", Vt)
print("n1 =", n1)

plt.figure(1)
# Generate fitted curve for dfV based on the fitted parameters
newy1 = getlin(dfV.to_numpy(), K, Vt, n1)

# Plot the voltage (dfV) against the current data (dfI1 and dfI2)
plt.plot(dfV, 1000 * dfI1.values, label="L40 W80 [nm]")

# Plot the fitted curve for dfI1
plt.plot(dfV, 1000 * newy1, label="Fitted curve (L40 W80 [nm])", linestyle='--')

# Customize the plot
plt.title("")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (mA)")
plt.legend()  # Add the legend
plt.grid(True)  # Add a grid
###########################################################################################
# Perform curve fitting for dfI2
[K, Vt, n2], pcov = curve_fit(getlin, dfV.to_numpy().flatten(), dfI2.to_numpy().flatten(), bounds=param_bounds)

# Output the fitted parameters
print("K =", K)
print("Vt =", Vt)
print("n2 =", n2)

# Generate fitted curve for dfV based on the fitted parameters
newy2 = getlin(dfV.to_numpy(), K, Vt, n2)

plt.plot(dfV, 1000 * dfI2.values, label="L120 W240 [nm]")
# Plot the fitted curve for dfI2
plt.plot(dfV, 1000 * newy2, label="Fitted curve (L120 W240 [nm])", linestyle='--')

# Customize the plot
plt.title("")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (mA)")
plt.legend()  # Add the legend
plt.grid(True)  # Add a grid
plt.show()

erro1 = ((-dfI1.iloc[:, 0].values + newy1[:,0])*100)/(dfI1.iloc[:, 0].values)
erro2 = ((-dfI2.iloc[:, 0].values + newy2[:,0])*100)/(dfI2.iloc[:, 0].values)

  ## iloc porque como sao panda data frames precisam de ser autorizzado indexcação
  ## .Values para ser convertido em um array da biblioteca numpy

plt.figure(2)

plt.plot(dfV,erro1, label="erro relativo1")
plt.plot(dfV,erro2, label="erro relativo2")

# Customize the plot
plt.title("Erro")
plt.xlabel("Voltage (V)")
plt.ylabel("% erro")
plt.legend()  # Add the legend
plt.grid(True)  # Add a grid
plt.show()


