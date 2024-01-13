# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:17:02 2024

Esercizi 3.1 e 3.2: Cinematica dell'evoluzione di tonneau

@author: ppolisi
"""

import conversioni as conv
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Chiudi tutte le figure precedenti
plt.close('all')
# Configura la modalità di visualizzazione dei plot in una finestra separata
plt.switch_backend('Qt5Agg')

#Dati
t_fin = 130  #tempo finale della simulazione

#velocità iniziale
u0 = conv.convvel(380,'km/h','m/s')
#Quota e posizione iniziale
h0 = 100 #quota iniziale in m
x0 = 0
y0 = 0
z0 = -h0

#Definizione dei valori max e dei punti su cui poi applicare
#interpolante cubica.
q_max = np.radians(2);
p_max = np.radians(4); 

tq_points = np.arange(0,1.001,0.075)*t_fin #14 istanti t
q_points = np.array([0, 0.2*q_max, 0.5*q_max, 0.9*q_max, q_max,
                      q_max, q_max, q_max, q_max, 0.9*q_max, 0.72*q_max,
                      0, 0, 0])
#     #si è costruita con un processo trial and error

tp_points = np.arange(0,1.001,0.075)*t_fin #14 istanti t
p_points = np.array([0, 0.2*p_max, 0.5*p_max, 0.9*p_max, p_max,
                      p_max, p_max, p_max, p_max, p_max, 0.65*p_max,
                      0, 0, 0])

tu_points = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,0.8, 1])*t_fin
u_points = np.array([u0, 0.7*u0, 0.9*u0, 0.95*u0, 0.98*u0, u0, u0, 
                     u0, u0, u0])

# Definizione della funzione q(t) con interpolazione pchip
q = lambda t: PchipInterpolator(tq_points, q_points)(t)
p = lambda t: PchipInterpolator(tp_points, p_points)(t)
r = lambda t: t*0

# Definizione della funzione q(t) con interpolazione pchip
u = lambda t: PchipInterpolator(tu_points, u_points)(t)
v = lambda t: t*0
w = lambda t: t*0

#vettore dei tempi
v_time = np.linspace(0,t_fin,200)

angular_velocity_q = q(v_time)
angular_velocity_p = p(v_time)
angular_velocity_r = r(v_time)
# Conversione dell'angolo da radianti al secondo a gradi al secondo
angular_velocity_q_deg = np.degrees(angular_velocity_q)
angular_velocity_p_deg = np.degrees(angular_velocity_p)

# Creazione del grafico
plt.figure()
plt.plot(v_time, angular_velocity_q_deg, label='q(t)', linewidth=1.5)
plt.plot(v_time, angular_velocity_p_deg, label='p(t)', linewidth=1.5)
plt.plot(v_time, angular_velocity_r, label='r(t)', linewidth=1.5)
# Personalizzazione del grafico
plt.grid(True)
plt.xlabel('t (s)')
plt.text(1.6, 50, 'q(t)')
plt.text(3, 5, 'p(t)')
plt.text(6, 5, 'r(t)')
plt.legend()
plt.ylim([-20, 20])

# Mostra il grafico
plt.show()

# Salva la figura come JPEG
plt.savefig('angular_velocity_plot_tonneau.jpg', dpi=300, bbox_inches='tight')

plt.figure()
plt.plot(v_time, u(v_time), label='u(t)', linewidth=1.5)
plt.plot(v_time, v(v_time), label='u(t)', linewidth=1.5)
plt.plot(v_time, w(v_time), label='u(t)', linewidth=1.5)
plt.grid(True)
plt.xlabel('t(s)')
plt.legend()

plt.show()

# Salva la figura come JPEG
plt.savefig('velocity_plot_tonneau.jpg', dpi=300, bbox_inches='tight')

# RISOLUZIONE
#Si risolvono le equazioni del quaternione con ode45

#Angoli di Eulero iniziali: volo ad ali livellate,
#fus. orizzontale e prua in direzione Nord
# Condizioni iniziali per gli angoli di Eulero
psi0, theta0, phi0 = 0, 0, 0

# Conversione agli angoli di Eulero a quaternione
from scipy.spatial.transform import Rotation
Q_0 = Rotation.from_euler('zyx', [psi0, theta0, phi0], degrees=True).as_quat()


# Funzione per l'ODE
def dQuatdt(t, Q):
    return 0.5 * np.array([
        [0, -p(t), -q(t), -r(t)],
        [p(t), 0, r(t), -q(t)],
        [q(t), -r(t), 0, p(t)],
        [r(t), q(t), -p(t), 0]
    ]).dot(Q)

# Risoluzione dell'ODE per il quaternione
sol_quat = solve_ivp(dQuatdt, [0, t_fin], Q_0, t_eval=v_time, method='RK45')

# Estrazione delle componenti del quaternione
q0, q1, q2, q3 = sol_quat.y

# Plot del quaternione
plt.figure()
plt.plot(v_time, q0, label='$q_{0(t)}$')
plt.plot(v_time, q1, label='$q_{x(t)}$')
plt.plot(v_time, q2, label='$q_{y(t)}$')
plt.plot(v_time, q3, label='$q_{z(t)}$')
plt.legend(loc='best')
plt.xlabel('t (s)')
plt.ylabel('q')
plt.grid(True)
plt.ylim([-1.1, 1.1])
plt.xlim([0, t_fin])
plt.show()

# Salva la figura come JPEG
plt.savefig('quaternion_plot_tonneau.jpg', dpi=300, bbox_inches='tight')

# Ricavare gli angoli di Eulero
r = Rotation.from_quat(np.column_stack((q1, q2, q3, q0)))
angles_euler = r.as_euler('zyx', degrees=True)

# Plot degli angoli di Eulero
plt.figure()
plt.plot(v_time, angles_euler[:, 2], label='$\phi$')
plt.plot(v_time, angles_euler[:, 1], label='$\\theta$')
plt.plot(v_time, angles_euler[:, 0], label='$\psi$')
plt.legend(loc='best')
plt.xlabel('t (s)')
plt.ylabel('($^{\circ}$)')
plt.grid(True)
plt.axis([0, t_fin, -200, 200])
plt.show()

# Salva la figura come JPEG
plt.savefig('euler_angles_plot_tonneau.jpg', dpi=300, bbox_inches='tight')

# Risoluzione dell'ODE per la posizione
# Funzione per l'ODE della posizione
def dPositionEdt(t, position):
    quat_interp = Rotation.from_quat([np.interp(t, sol_quat.t, sol_quat.y[i]) for i in range(4)])
    rotation_matrix = quat_interp.as_matrix()
    return rotation_matrix.T.dot([u(t), v(t), w(t)])

# Condizioni iniziali per la posizione
x0, y0, z0 = 0, 0, 0

# Risoluzione dell'ODE per la posizione
sol_position = solve_ivp(dPositionEdt, [0, t_fin], [x0, y0, z0], t_eval=v_time, method='RK45')

# Plot della posizione
plt.figure()
plt.plot(v_time, sol_position.y[0], label='$x_{E,G}$')
plt.plot(v_time, sol_position.y[1], label='$y_{E,G}$')
plt.plot(v_time, sol_position.y[2], label='$z_{E,G}$')
plt.legend(loc='best')
plt.xlabel('t (s)')
plt.ylabel('(m)')
plt.grid(True)
plt.axis([0, t_fin, -4000, 13000])

plt.show()

# Salva la figura come JPEG
plt.savefig('position_plot_tonneau.jpg', dpi=300, bbox_inches='tight')