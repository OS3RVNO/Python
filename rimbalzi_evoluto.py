import matplotlib

matplotlib.use('Agg')  # Imposta il backend su Agg
import matplotlib.pyplot as plt
from PIL import Image
import os


def calcola_rimbalzi_gif():
    print("Calcolo dei Rimbalzi della Pallina")

    # Richiesta input con validazione
    h = 0.0
    while h <= 1:
        try:
            h = float(input("Inserire altezza da cui viene lanciata la pallina in cm (h > 1): "))
            if h <= 1:
                print("Errore: l'altezza deve essere maggiore di 1 cm.")
        except ValueError:
            print("Errore: per favore inserisci un numero valido.")

    # Inizializzazione del contatore dei rimbalzi e lista per il grafico
    i = 0
    altezze = [h]  # Lista per memorizzare le altezze
    rimbalzi = [i]  # Lista per memorizzare i numeri di rimbalzo

    # Ciclo per calcolare i rimbalzi finché l'altezza è superiore a 1 cm
    while h > 1:
        h *= 0.8  # Riduzione dell'altezza al 80% ad ogni rimbalzo
        i += 1  # Incremento del contatore di rimbalzi
        altezze.append(h)
        rimbalzi.append(i)
        print(f"Rimbalzo n. {i} - Altezza in cm: {h:.2f}")

    # Stampa del numero totale di rimbalzi e dell'altezza finale
    print(f"\nIl numero totale di rimbalzi è pari a {i}")
    print(f"L'altezza finale è pari a {h:.2f} cm")

    # Creazione dei fotogrammi per la GIF
    frames = []
    for j in range(len(altezze)):
        plt.figure(figsize=(6, 6))
        plt.plot(rimbalzi[:j + 1], altezze[:j + 1], marker='o', linestyle='-', color='b', label='Altezza della pallina')
        plt.xlim(0, len(rimbalzi))
        plt.ylim(0, altezze[0] * 1.1)
        plt.title(f"Rimbalzo n. {j}")
        plt.xlabel("Numero di rimbalzi")
        plt.ylabel("Altezza in cm")
        plt.grid(True)

        # Salva ciascun frame temporaneo
        frame_filename = f"frame_{j}.png"
        plt.savefig(frame_filename)
        frames.append(frame_filename)
        plt.close()

    # Chiedi dove salvare la GIF
    gif_path = input("Inserisci il percorso e il nome del file per salvare la GIF (es. C:/path/to/file.gif): ")

    # Creazione della GIF usando Pillow
    images = [Image.open(f) for f in frames]
    images[0].save(gif_path, save_all=True, append_images=images[1:], loop=0, duration=500)

    # Pulizia dei file temporanei
    for f in frames:
        os.remove(f)

    print(f"\nGIF salvata come '{gif_path}'")


# Chiamata alla funzione
calcola_rimbalzi_gif()
