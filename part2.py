import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')
# Load data
dfV = pd.read_csv("C:/edgar/EDAN/flew/4040V0.9.txt", sep="\t", usecols=[0])
dfI40_40 = pd.read_csv("C:/edgar/EDAN/flew/4040V0.9.txt", sep="\t", usecols=[1])
dfI40_50 = pd.read_csv("C:/edgar/EDAN/flew/4050V0.9.txt", sep="\t", usecols=[1])
dfI40_60 = pd.read_csv("C:/edgar/EDAN/flew/4060V0.9.txt", sep="\t", usecols=[1])
dfI40_70 = pd.read_csv("C:/edgar/EDAN/flew/4070V0.9.txt", sep="\t", usecols=[1])
dfI40_80 = pd.read_csv("C:/edgar/EDAN/flew/4080V0.9.txt", sep="\t", usecols=[1])
dfI40_90 = pd.read_csv("C:/edgar/EDAN/flew/4090V0.9.txt", sep="\t", usecols=[1])
dfI40_100 = pd.read_csv("C:/edgar/EDAN/flew/40100V0.9.txt", sep="\t", usecols=[1])
dfI40_110 = pd.read_csv("C:/edgar/EDAN/flew/40110V0.9.txt", sep="\t", usecols=[1])
dfI40_120 = pd.read_csv("C:/edgar/EDAN/flew/40120V0.9.txt", sep="\t", usecols=[1])

dfI120_120 = pd.read_csv("C:/edgar/EDAN/flew/120120V0.9.txt", sep="\t", usecols=[1])
dfI120_140 = pd.read_csv("C:/edgar/EDAN/flew/120140V0.9.txt", sep="\t", usecols=[1])
dfI120_160 = pd.read_csv("C:/edgar/EDAN/flew/120160V0.9.txt", sep="\t", usecols=[1])
dfI120_180 = pd.read_csv("C:/edgar/EDAN/flew/120180V0.9.txt", sep="\t", usecols=[1])
dfI120_200 = pd.read_csv("C:/edgar/EDAN/flew/120200V0.9.txt", sep="\t", usecols=[1])
dfI120_220 = pd.read_csv("C:/edgar/EDAN/flew/120220V0.9.txt", sep="\t", usecols=[1])
dfI120_240 = pd.read_csv("C:/edgar/EDAN/flew/120240V0.9.txt", sep="\t", usecols=[1])
dfI120_260 = pd.read_csv("C:/edgar/EDAN/flew/120260V0.9.txt", sep="\t", usecols=[1])
dfI120_280 = pd.read_csv("C:/edgar/EDAN/flew/120280V0.9.txt", sep="\t", usecols=[1])
dfI120_300 = pd.read_csv("C:/edgar/EDAN/flew/120300V0.9.txt", sep="\t", usecols=[1])


#fit function
def getlin(x, a, b, c):  # x = VGS; a = K; b = Vt; c = n
    return np.piecewise(x, [x < 0.22, x >= 0.22], 
                        [lambda x: 0, lambda x: 0.5 * a * np.power(np.maximum(x - b, 0), c)])


param_bounds = ([0, 0, 0], [np.inf, 1, 2])  # K >= 0, Vt up to 1, n up to 2
K40 = []
K120 = []
datasets_40 = [dfI40_40, dfI40_50, dfI40_60, dfI40_70, dfI40_80, dfI40_90, dfI40_100, dfI40_110, dfI40_120]
datasets_120 = [dfI120_120, dfI120_140, dfI120_160, dfI120_180, dfI120_200, dfI120_220, dfI120_240, dfI120_260, dfI120_280, dfI120_300]
dataset_labels_40 = ["L40 W40", "L40 W50", "L40 W60", "L40 W70", "L40 W80","L40 W90", "L40 W100", "L40 W110", "L40 W120"]
dataset_labels_120 = ["L120 W120", "L120 W140", "L120 W160", "L120 W180", "L120 W200","L120 W220", "L120 W240", "L120 W260", "L120 W280", "L120 W300"]
W_list_40 = [40, 50, 60, 70, 80, 90, 100, 110, 120]
W_list_120 = [120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
error_matrix_40 = []
error_matrix_120 = []

#  curve fit para L40nm
plt.figure(1)
for i, dfI in enumerate(datasets_40):
    [K, Vt, n], _ = curve_fit(getlin, dfV.to_numpy().flatten(), dfI.to_numpy().flatten(), bounds=param_bounds)
    K40.append(K)  # Store the K value
    
    new_y = getlin(dfV.to_numpy(), K, Vt, n)
    
    # Plot each dataset's original and fitted curves
    plt.plot(dfV, 1000 * dfI.values, label=f"{dataset_labels_40[i]}")
    plt.plot(dfV, 1000 * new_y, label=f"Fitted curve: {dataset_labels_40[i]}", linestyle='--')     
    
    print(f"K  {dataset_labels_40[i]} =", K)
    print(f"Vt {dataset_labels_40[i]} =", Vt)
    print(f"n  {dataset_labels_40[i]} =", n)
        
    #erro calc.
    erro = ((new_y[:, 0] - dfI.iloc[:, 0].values) * 100) / dfI.iloc[:, 0].values
    error_matrix_40.append(erro)

# Plot
plt.title("Different Curves, L=40nm")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (mA)")
plt.legend()  
plt.grid(True) 
plt.show()

#  curve fit para L120nm
plt.figure(2)
for i, dfI in enumerate(datasets_120):
    [K, Vt, n], _ = curve_fit(getlin, dfV.to_numpy().flatten(), dfI.to_numpy().flatten(), bounds=param_bounds)
    K120.append(K)  # Store the K value
    
    new_y = getlin(dfV.to_numpy(), K, Vt, n)
    
    # Plot each dataset's original and fitted curves
    plt.plot(dfV, 1000 * dfI.values, label=f"I {dataset_labels_120[i]}")
    plt.plot(dfV, 1000 * new_y, label=f"Fitted curve I {dataset_labels_120[i]}", linestyle='--')
    
    print(f"K  {dataset_labels_120[i]} =", K)
    print(f"Vt {dataset_labels_120[i]} =", Vt)
    print(f"n  {dataset_labels_120[i]} =", n)
    
    #erro calc.
    erro = ((new_y[:, 0] - dfI.iloc[:, 0].values) * 100) / dfI.iloc[:, 0].values
    error_matrix_120.append(erro)

# Plot
plt.title("Different Curves, L=120nm")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (mA)")
plt.legend()  
plt.grid(True)  
plt.show()

#B finding
B40=[]
B120=[]
for i in range(len(K40)):
    B40.append(K40[i] / ( W_list_40[i]/40))
    
for i in range(len(K120)):
    B120.append(K120[i] / ( W_list_120[i]/120))   
    
plt.figure(3)
plt.plot(W_list_40, B40, marker='o', linestyle='-', color='b', label='B40 vs W_list_40')
plt.xlabel("W (Width) [nm]")
plt.ylabel("B, L=40nm")
plt.title("B vs Width for L=40nm")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(4)
plt.plot(W_list_120, B120, marker='o', linestyle='-', color='b', label='B120 vs W_list_120')
plt.xlabel("W (Width) [nm]")
plt.ylabel("B, L=120nm")
plt.title("B vs Width for L=120nm")
plt.grid(True)
plt.legend()
plt.show()

#Erro
plt.figure(5)
for i, erro in enumerate(error_matrix_40):
    plt.plot(dfV, erro, label=f"Error {dataset_labels_40[i]}",linestyle=':')
plt.title("x")
plt.xlabel("Voltage (V)")
plt.ylabel("Erro [%]")
plt.legend()  
plt.grid(True)  
plt.show()

plt.figure(6)
for i, erro in enumerate(error_matrix_120):
    plt.plot(dfV, erro, label=f"Error {dataset_labels_120[i]}",linestyle=':')
plt.title("x")
plt.xlabel("Voltage (V)")
plt.ylabel("Erro [%]")
plt.legend()  
plt.grid(True)  
plt.show()



# xxx =[]
# for i in range(len(W_list_120)):
#     xxx.append(( W_list_120[i]/120))  
# plt.figure(7)
# plt.plot(W_list_120, xxx, marker='o', linestyle='-', color='b', label='B120 vs W_list_120')
# plt.xlabel("W (Width) [nm]")
# plt.ylabel("B, L=120nm")
# plt.title("B vs Width for L=120nm")
# plt.grid(True)
# plt.legend()
# plt.show()