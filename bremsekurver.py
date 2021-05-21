# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt



# atc førerpanel
tilsetningstid = 9 # [s]
bremsekraft = 109


# strekning
linjehastighet = 70 # [km/t] utgangshastighet
målhastighet = 40 # [km/t]
fall = 35 # [promille] stigning angis med negativt fortegn


# til beregning
v_0 = linjehastighet / 3.6
v_mål = målhastighet / 3.6

b_f = bremsekraft / 100
k = 0.01
G = 0 - fall

atc_retardasjon = b_f + k * G
trv_retardasjon = 0 - fall / 100 + 0.7

handbok_bremselengde = round((v_0**2 - v_mål**2) / (2 * atc_retardasjon))
trv_bremselengde = round((v_0**2 - v_mål**2) / (2 * trv_retardasjon))


# v = at 

# def L3(t):
#     return v_0 * t - 1/2 * atc_retardasjon * t**2

# def v(s):
#     return [sqrt(v_0**2 - 2 * atc_retardasjon * i) for i in s]



# hastighet som en funksjon av avstand
def v(s, T):
    v_list = []
    for i in s:
        if (i < v_0 * T):
            v_list.append(v_0)
        else:
            v_list.append(sqrt(v_0**2 - 2 * atc_retardasjon * i))
    return v_list

def handbok_bremsekurve(T):
    ventetid = [v_0] * int(v_0 * T)
    kurve = [sqrt(v_0**2 - 2 * atc_retardasjon * s) for s in range(handbok_bremselengde)]
    return ventetid + kurve
    
def trv_bremsekurve(T):
    ventetid = [v_0] * int(v_0 * T)
    kurve = [sqrt(v_0**2 - 2 * trv_retardasjon * s) for s in range(trv_bremselengde)]
    return ventetid + kurve


y0 = trv_bremsekurve(13)

interval_A = handbok_bremsekurve(13 + tilsetningstid)
interval_B = handbok_bremsekurve(8 + tilsetningstid)
interval_C = handbok_bremsekurve(3 + tilsetningstid)
interval_D = handbok_bremsekurve(0 + tilsetningstid)


plt.plot(np.arange(len(y0)), y0, label='Målavstand TRV')
plt.plot(np.arange(len(interval_A)), interval_A, label='Interval A')
plt.plot(np.arange(len(interval_B)), interval_B, label='Interval B')
plt.plot(np.arange(len(interval_C)), interval_C, label='Interval C')
plt.plot(np.arange(len(interval_D)), interval_D, label='Interval D')
# plt.plot(x, x, label='Lineær')

plt.xlabel('meter')
plt.ylabel('m/s')

plt.title("Bremsekurver")

plt.legend()

plt.show()