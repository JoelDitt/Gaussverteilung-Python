import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Konstanten in eV
k_B_eV = 8.617e-5  # Boltzmann-Konstante in eV/K
mu_eV = 0.55       # Chemisches Potential (Fermi-Energie) in eV
E_minus_mu = np.linspace(-0.1, 0.25, 1000)  # Energie relativ zu µ (ε - µ) in eV
T_values = np.exp(np.linspace(np.log(7), np.log(500), 50))  # Temperaturbereich (K)

# Funktion für Bose-Einstein-Verteilung
def bose_einstein(E_minus_mu, T, k_B):
    # Berechne die Besetzung
    exp_term = np.exp(E_minus_mu / (k_B * T))
    n = 1 / (exp_term - 1)
    # Behandlung für den Fall ε - μ = 0 (maximale Besetzung bei T > 0)
    n[0] = 1 / (k_B * T)
    return n

# Setup der Figur und Achsen
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlabel(r"Energy $(\epsilon - \mu)$ in eV", fontsize=14)
ax.set_ylabel(r"$<n(\epsilon)>$", fontsize=14)
ax.set_xlim(-0.005, 0.15)  # Bereich für ε-µ
ax.set_ylim(0, 2.5)   # Anfangswert für die y-Achse
ax.grid(alpha=0.3)

# Passe das Layout an, um Platz für Achsenbeschriftungen zu schaffen
plt.subplots_adjust(bottom=0.2)

# Linie und Text für die Animation
line, = ax.plot([], [], color="dodgerblue", lw=2)
fill = None  # Placeholder für die Fläche
temp_text = ax.text(0.1, 2, "", ha="center", fontsize=14)

# Initialisierungsfunktion
def init():
    global fill
    line.set_data([], [])
    if fill:
        fill.remove()  # Entferne alte Fläche, falls vorhanden
    temp_text.set_text("")
    return line, temp_text

# Update-Funktion für die Animation
def update(frame):
    global fill
    T = frame  # Aktuelle Temperatur
    y = bose_einstein(E_minus_mu, T, k_B_eV)
    line.set_data(E_minus_mu, y)
    if fill:
        fill.remove()  # Entferne alte Fläche
    fill = ax.fill_between(E_minus_mu, 0, y, color="dodgerblue", alpha=0.3)  # Aktualisiere Fläche
    temp_text.set_text(r"$T = {:.1f} \, \mathrm{{K}}$".format(T))
    return line, temp_text, fill

# Animation erstellen
ani = FuncAnimation(fig, update, frames=np.concatenate([T_values, T_values[::-1]]),
                    init_func=init, blit=False, interval=100)

# Speichern als GIF
gif_path = "bose_einstein_e_minus_mu_corrected.gif"
ani.save(gif_path, writer="pillow", fps=10)

print(f"Animation wurde erfolgreich gespeichert unter: {gif_path}")
