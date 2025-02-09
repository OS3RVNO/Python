import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PIL import Image, ImageDraw, ImageFont

class SimulatoreDadi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_dice_images()  # Creiamo le immagini dei dadi

    def initUI(self):
        """Configura la finestra e gli oggetti dell'interfaccia."""
        # Imposta la finestra dell'app
        self.setWindowTitle("Simulatore di Dadi Animati 🎲")
        self.setGeometry(100, 100, 300, 300)

        # Layout verticale
        self.layout = QVBoxLayout()

        # Etichetta per il dado
        self.label_dado = QLabel(self)
        self.label_dado.setPixmap(QPixmap("dice_1.png"))  # Mostra l'immagine iniziale
        self.label_dado.setScaledContents(True)
        self.label_dado.setFixedSize(150, 150)  # Dimensioni dell'immagine
        self.layout.addWidget(self.label_dado)

        # Bottone per lanciare il dado
        self.btn_lancia = QPushButton("Lancia il dado!")
        self.btn_lancia.clicked.connect(self.start_animation)
        self.layout.addWidget(self.btn_lancia)

        # Imposta il layout
        self.setLayout(self.layout)

        # Timer per l'animazione
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_dice)
        self.animation_frames = 10  # Numero di frame dell'animazione
        self.current_frame = 0
        self.final_result = 1

    def start_animation(self):
        """Inizia l'animazione del dado."""
        self.animation_frames = random.randint(10, 20)  # Numero casuale di cambiamenti di faccia
        self.final_result = random.randint(1, 6)  # Risultato finale del dado
        self.current_frame = 0
        self.timer.start(100)  # Cambia l'immagine ogni 100 ms

    def animate_dice(self):
        """Gestisce l'animazione cambiando rapidamente le facce del dado."""
        self.current_frame += 1
        random_face = random.randint(1, 6)  # Scegli una faccia casuale
        self.label_dado.setPixmap(QPixmap(f"dice_{random_face}.png"))  # Carica l'immagine della faccia

        # Dopo un certo numero di frame, fermati e mostra il risultato finale
        if self.current_frame >= self.animation_frames:
            self.timer.stop()  # Ferma il timer
            self.label_dado.setPixmap(QPixmap(f"dice_{self.final_result}.png"))  # Mostra il risultato finale

    def create_dice_images(self):
        """Crea le immagini delle facce del dado e le salva."""
        # Se non esistono già, crea le immagini delle facce del dado
        for i in range(1, 7):
            self.create_single_dice_image(i)

    def create_single_dice_image(self, number):
        """Crea un'immagine di una singola faccia del dado."""
        # Impostazioni per il dado
        size = 150
        image = Image.new("RGB", (size, size), "#f0f0f0")  # Sfondo grigio chiaro
        draw = ImageDraw.Draw(image)

        # Disegniamo i cerchi per i punti
        self.draw_dice_faces(draw, size, number)

        # Salva l'immagine
        image.save(f"dice_{number}.png")

    def draw_dice_faces(self, draw, size, number):
        """Disegna i punti del dado in base al numero della faccia."""
        radius = 15  # Raggio dei cerchi
        # Calcola le posizioni dei cerchi
        positions = {
            1: [(size // 2, size // 2)],  # Punti al centro per il numero 1
            2: [(size // 4, size // 4), (3 * size // 4, 3 * size // 4)],  # Punti diagonali per il numero 2
            3: [(size // 2, size // 2), (size // 4, size // 4), (3 * size // 4, 3 * size // 4)],  # 3 punti
            4: [(size // 4, size // 4), (3 * size // 4, size // 4), (size // 4, 3 * size // 4), (3 * size // 4, 3 * size // 4)],  # 4 punti agli angoli
            5: [(size // 2, size // 2), (size // 4, size // 4), (3 * size // 4, size // 4), (size // 4, 3 * size // 4), (3 * size // 4, 3 * size // 4)],  # 5 punti
            6: [(size // 4, size // 4), (3 * size // 4, size // 4), (size // 4, size // 2), (3 * size // 4, size // 2), (size // 4, 3 * size // 4), (3 * size // 4, 3 * size // 4)],  # 6 punti
        }

        # Disegna i cerchi nelle posizioni calcolate
        for pos in positions[number]:
            x, y = pos
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="black")

# Avvio dell'applicazione
if __name__ == "__main__":
    # Avvia l'applicazione e mostra la finestra
    app = QApplication(sys.argv)
    simulatore = SimulatoreDadi()
    simulatore.show()
    sys.exit(app.exec_())
