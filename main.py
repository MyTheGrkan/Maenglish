import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import google.generativeai as genai

# Google Cloud API anahtarınızı buraya ekleyin
API_KEY = "your-google-cloud-api-key"
genai.configure(api_key=API_KEY)

# Gemini modelini yükle
model = genai.GenerativeModel('gemini-2.0-flash')

# Sınıf seviyesine göre soru oluşturma fonksiyonu
def generate_question(grade):
    prompt = f"Generate a simple English question suitable for {grade}th grade students. The question can be about vocabulary, basic grammar, or simple dialogues. Provide the question and the correct answer."
    response = model.generate_content(prompt)
    return response.text

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("İngilizce Quiz Uygulaması 🎀")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #fff0f5;  /* Pembe tonu */
            }
            QLabel {
                font-size: 24px;
                color: #ff69b4;  /* Pembe */
                font-weight: bold;
            }
            QPushButton {
                font-size: 18px;
                padding: 15px 25px;
                background-color: #ff69b4;  /* Pembe */
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff1493;  /* Daha koyu pembe */
            }
        """)

        # Ana layout
        main_layout = QVBoxLayout()

        # Başlık
        title_label = QLabel("Sınıf Seviyesi Seçin 🌸", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Comic Sans MS", 24, QFont.Weight.Bold))
        main_layout.addWidget(title_label)

        # Sınıf butonları için grid layout
        grid_layout = QGridLayout()

        # Sınıf butonları
        grades = ["1. Sınıf", "2. Sınıf", "3. Sınıf", "4. Sınıf", "5. Sınıf", 
                  "6. Sınıf", "7. Sınıf", "8. Sınıf", "9. Sınıf", "10. Sınıf", 
                  "11. Sınıf", "12. Sınıf"]
        positions = [(i // 3, i % 3) for i in range(len(grades))]  # 3 sütunlu grid

        for position, grade in zip(positions, grades):
            button = QPushButton(grade, self)
            button.clicked.connect(lambda _, g=grade: self.start_quiz(g))
            grid_layout.addWidget(button, *position)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def start_quiz(self, grade):
        self.hide()  # Ana menüyü gizle
        self.quiz_app = QuizApp(grade)  # Seçilen sınıfa göre quiz başlat
        self.quiz_app.show()

class QuizApp(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self.score = 0  # Skor takibi
        self.initUI()
        self.new_question()

    def initUI(self):
        self.setWindowTitle(f"{self.grade} İngilizce Quiz Uygulaması 🎀")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #fff0f5;  /* Pembe tonu */
            }
            QLabel {
                font-size: 20px;
                color: #ff69b4;  /* Pembe */
                font-weight: bold;
            }
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #ff69b4;
                border-radius: 10px;
                background-color: #fff;
            }
            QPushButton {
                font-size: 18px;
                padding: 10px 20px;
                background-color: #ff69b4;  /* Pembe */
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff1493;  /* Daha koyu pembe */
            }
            QPushButton#next {
                background-color: #ffa07a;  /* Açık turuncu */
            }
            QPushButton#next:hover {
                background-color: #ff7f50;  /* Daha koyu turuncu */
            }
        """)

        # Ana layout
        main_layout = QVBoxLayout()

        # Skor alanı
        self.score_label = QLabel(f"Skor: {self.score} 🏆", self)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QFont("Comic Sans MS", 24, QFont.Weight.Bold))
        main_layout.addWidget(self.score_label)

        # Soru alanı
        self.question_label = QLabel("Soru burada görünecek 🎀", self)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setFont(QFont("Comic Sans MS", 20))
        self.question_label.setWordWrap(True)
        main_layout.addWidget(self.question_label)

        # Cevap girişi
        self.answer_input = QLineEdit(self)
        self.answer_input.setPlaceholderText("Cevabınızı buraya yazın... ✏️")
        main_layout.addWidget(self.answer_input)

        # Butonlar için yatay layout
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Cevapla 🎯", self)
        self.submit_button.clicked.connect(self.check_answer)
        button_layout.addWidget(self.submit_button)

        self.next_button = QPushButton("Sonraki Soru 🌸", self)
        self.next_button.setObjectName("next")
        self.next_button.clicked.connect(self.new_question)
        button_layout.addWidget(self.next_button)

        main_layout.addLayout(button_layout)

        # Tatlı bir ikon ekleyelim
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap("heart.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))  # Kalp ikonu
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.icon_label)

        self.setLayout(main_layout)

    def new_question(self):
        # Yeni bir soru oluştur
        self.current_question = generate_question(self.grade.split()[0])  # Sınıf seviyesini al (örneğin, "1. Sınıf" -> "1")
        self.question_label.setText(self.current_question)
        self.answer_input.clear()

    def check_answer(self):
        user_answer = self.answer_input.text().strip()
        if user_answer == "":
            QMessageBox.warning(self, "Uyarı", "Lütfen bir cevap girin. 🎀")
            return

        # Gemini'ye kullanıcının cevabını kontrol ettir
        prompt = f"Soru: {self.current_question}\nKullanıcının cevabı: {user_answer}\nBu cevap doğru mu? Değilse doğru cevabı söyle."
        response = model.generate_content(prompt)
        result = response.text

        # Skor güncelleme
        if "doğru" in result.lower() or "correct" in result.lower():
            self.score += 1
            self.score_label.setText(f"Skor: {self.score} 🏆")
            self.icon_label.setPixmap(QPixmap("heart.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))  # Kalp ikonu
            QMessageBox.information(self, "Tebrikler! 🎉", "Doğru cevap! 🎀\n\n" + result)
        else:
            self.icon_label.setPixmap(QPixmap("sad.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))  # Üzgün ikon
            QMessageBox.information(self, "Sonuç", result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
