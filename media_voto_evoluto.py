import os


def main():
    # Lista per memorizzare i voti
    voti = []

    # Chiediamo all'utente di inserire i voti
    while True:
        try:
            voto = input("Inserisci un voto tra 0 e 30 (o 'fine' per terminare): ")
            if voto.lower() == 'fine':
                break

            voto = float(voto)

            # Controllo se il voto è valido
            if 0 <= voto <= 30:
                voti.append(voto)
            else:
                print("Il voto deve essere tra 0 e 30.")
        except ValueError:
            print("Inserisci un numero valido o 'fine' per terminare.")

    # Calcoliamo la media se ci sono voti
    if voti:
        media = sum(voti) / len(voti)
        print(f"La media dei voti è: {media:.2f}")

        # Chiediamo all'utente dove salvare il file
        salva_pagina_web(voti, media)
    else:
        print("Nessun voto inserito.")


def salva_pagina_web(voti, media):
    # Chiediamo all'utente dove vuole salvare il file
    percorso = input(
        "Inserisci il percorso completo dove vuoi salvare il file (includi il nome del file e l'estensione .html): ")

    # Verifica se il percorso è valido
    if not percorso.endswith('.html'):
        print("Il file deve avere l'estensione .html. Aggiungiamo '.html' al percorso.")
        percorso += '.html'

    # Creiamo il contenuto HTML
    voti_list = ''.join(f'<li>{voto:.2f}</li>' for voto in voti)

    contenuto = f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Media Voti Studente</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #e8f0fe; color: #333; padding: 20px; }}
            h1 {{ color: #4a90e2; text-align: center; }}
            h2 {{ color: #333; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ background: #ffffff; margin: 5px 0; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .media {{ font-size: 1.5em; font-weight: bold; text-align: center; margin-top: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Media Voti Studente</h1>
            <h2>Voti Inseriti:</h2>
            <ul>
                {voti_list}
            </ul>
            <p class="media">La tua media e': <strong>{media:.2f}</strong></p>
        </div>
    </body>
    </html>
    """

    # Salviamo il file HTML
    try:
        with open(percorso, "w") as file:
            file.write(contenuto)
        print(f"La pagina web è stata creata come '{percorso}'. Puoi aprirla nel tuo browser.")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")


if __name__ == "__main__":
    main()
