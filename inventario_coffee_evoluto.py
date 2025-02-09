import json
from difflib import get_close_matches  # Per suggerire nomi simili

class MagazzinoCaffe:
    def __init__(self, file_dati="magazzino_caffe.json"):
        """Inizializza il magazzino e carica i dati dal file, se esistente."""
        self.file_dati = file_dati
        try:
            with open(self.file_dati, "r") as file:
                self.inventario = json.load(file)
            print("Dati caricati correttamente dal file.")
        except FileNotFoundError:
            self.inventario = {}
            print("File non trovato, inizializzato nuovo inventario.")
        except json.JSONDecodeError:
            self.inventario = {}
            print("Errore nel caricamento del file, inizializzato nuovo inventario.")

    def salva_dati(self):
        """Salva l'inventario corrente nel file."""
        try:
            with open(self.file_dati, "w") as file:
                json.dump(self.inventario, file, indent=4)
            print("Dati salvati correttamente nel file.")
        except Exception as e:
            print(f"Errore durante il salvataggio dei dati: {e}")

    def aggiungi_caffe(self, nome, quantita):
        """Aggiunge un nuovo tipo di caffè o aggiorna la quantità di uno esistente."""
        if nome in self.inventario:
            self.inventario[nome] += quantita
            print(f"Aggiornata la quantità di {nome}. Ora ce ne sono {self.inventario[nome]} kg.")
        else:
            self.inventario[nome] = quantita
            print(f"Aggiunto nuovo caffè: {nome}, {quantita} kg.")
        self.salva_dati()

    def rimuovi_caffe(self, nome, quantita):
        """Rimuove una certa quantità di caffè. Elimina il caffè se la quantità scende a zero."""
        if nome not in self.inventario:
            print(f"Errore: {nome} non è presente nel magazzino.")
        elif self.inventario[nome] < quantita:
            print(f"Errore: Quantità insufficiente di {nome}. Disponibile: {self.inventario[nome]} kg.")
        else:
            self.inventario[nome] -= quantita
            print(f"Rimossi {quantita} kg di {nome}. Rimangono {self.inventario[nome]} kg.")
            if self.inventario[nome] == 0:
                del self.inventario[nome]
                print(f"{nome} è stato completamente rimosso dal magazzino.")
        self.salva_dati()

    def visualizza_inventario(self):
        """Visualizza l'inventario corrente in ordine alfabetico."""
        if not self.inventario:
            print("Il magazzino è vuoto.")
        else:
            print("Inventario del magazzino:")
            totale = 0
            for nome in sorted(self.inventario.keys()):
                print(f" - {nome}: {self.inventario[nome]} kg")
                totale += self.inventario[nome]
            print(f"Totale caffè in magazzino: {totale} kg")

    def cerca_caffe(self, query):
        """
        Cerca un tipo specifico di caffè nel magazzino.
        Permette di cercare con il nome completo o parte di esso.
        Suggerisce nomi simili in caso di nessun risultato.
        """
        query = query.strip().lower()
        risultati = [nome for nome in self.inventario if query in nome.lower()]

        if risultati:
            print(f"Risultati trovati per '{query}':")
            for nome in risultati:
                print(f" - {nome}: {self.inventario[nome]} kg")
        else:
            print(f"Nessun caffè trovato con '{query}' nel nome.")
            suggerimenti = get_close_matches(query, self.inventario.keys(), n=3, cutoff=0.5)
            if suggerimenti:
                print("Forse intendevi:")
                for nome in suggerimenti:
                    print(f" - {nome}")

# Programma principale con gestione eccezioni
def menu():
    magazzino = MagazzinoCaffe()

    while True:
        try:
            print("\n--- Gestione Magazzino Caffè ---")
            print("1. Aggiungi caffè")
            print("2. Rimuovi caffè")
            print("3. Visualizza inventario")
            print("4. Cerca caffè")
            print("5. Esci")

            scelta = input("Scegli un'opzione: ").strip()

            if scelta == "1":
                nome = input("Inserisci il nome del caffè: ").strip()
                quantita = float(input("Inserisci la quantità (kg): "))
                if quantita <= 0:
                    raise ValueError("La quantità deve essere maggiore di zero.")
                magazzino.aggiungi_caffe(nome, quantita)

            elif scelta == "2":
                nome = input("Inserisci il nome del caffè da rimuovere: ").strip()
                quantita = float(input("Inserisci la quantità da rimuovere (kg): "))
                if quantita <= 0:
                    raise ValueError("La quantità deve essere maggiore di zero.")
                magazzino.rimuovi_caffe(nome, quantita)

            elif scelta == "3":
                magazzino.visualizza_inventario()

            elif scelta == "4":
                query = input("Inserisci il nome (o parte del nome) del caffè da cercare: ").strip()
                magazzino.cerca_caffe(query)

            elif scelta == "5":
                print("Uscita dal programma. Arrivederci!")
                break

            else:
                print("Opzione non valida. Riprova.")

        except ValueError as e:
            print(f"Errore: {e}. Riprova.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}. Riprova.")


# Esegui il menu principale
if __name__ == "__main__":
    menu()
