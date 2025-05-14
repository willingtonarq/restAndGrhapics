import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from fastapi import FastAPI

paramPais = ""
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hola mundo, servicio activo"}

@app.get("/graficos/{pais}")
def saludo(pais: str):
    df = pd.read_csv("01 renewable-share-energy.csv")    
    df_africa = df[df["Entity"] == pais].copy()
    years = df_africa["Year"].values
    renewables = df_africa["Renewables (% equivalent primary energy)"].values

    fig, ax = plt.subplots()
    ax.set_xlim(years.min(), years.max())
    ax.set_ylim(0, max(renewables) + 5)
    ax.set_title("Energía Renovable en África (1965 en adelante)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Renovables (% energía primaria)")
    ax.grid(True)
    line, = ax.plot([], [], lw=2, color='green')
    text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


    def init():
        line.set_data([], [])
        text.set_text('')
        return line, text
    
    # Función de actualización para cada frame
    def update(frame):
        x = years[:frame+1]
        y = renewables[:frame+1]
        line.set_data(x, y)
        text.set_text(f"Año: {x[-1]}, Renovables: {y[-1]:.2f}%")
        return line, text

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(years), init_func=init, blit=True, interval=150)

    # Guardar como GIF
    nameImage = pais + "_renewables.gif"
    ani.save(nameImage, writer="pillow", fps=5)
    return {"mensaje": f"Grafico Generado para el {pais}"}
 
