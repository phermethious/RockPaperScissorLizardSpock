from cryptography.fernet import Fernet
from PyQt5 import QtCore, QtGui, QtWidgets
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Set window title
        MainWindow.setWindowTitle("Rock Paper Scissors Lizard Spock")

        # Initialize scores
        self.player_score = 0
        self.computer_score = 0
        self.tie_game = 0

        # Generate a secret key for encryption/decryption
        self.secret_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.secret_key)

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Game Name
        self.game_name_label = QtWidgets.QLabel(self.centralwidget)
        self.game_name_label.setGeometry(QtCore.QRect(0, 10, 800, 40))
        self.game_name_label.setObjectName("game_name_label")
        self.game_name_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the text
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.game_name_label.setFont(font)
        self.game_name_label.setText("Rock Paper Scissors Lizard Spock")

        # Games Played Label
        self.games_played_label = QtWidgets.QLabel(self.centralwidget)
        self.games_played_label.setGeometry(QtCore.QRect(0, 60, 800, 20))
        self.games_played_label.setObjectName("games_played_label")
        self.games_played_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.games_played_label.setFont(font)
        self.games_played_label.setText("Games Played: 0")  # Initial value
        
        # Results Label
        self.results_label = QtWidgets.QLabel(self.centralwidget)
        self.results_label.setGeometry(QtCore.QRect(20, 80, 750, 20))
        self.results_label.setObjectName("results_label")
        self.results_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.results_label.setFont(font)
        self.results_label.setText(f"Player Score: {self.player_score} | Computer Score: {self.computer_score} | Tie games: {self.tie_game}")
        
        # Funny sayings label
        self.funny_sayings = QtWidgets.QLabel(self.centralwidget)
        self.funny_sayings.setGeometry(QtCore.QRect(0, 250, 800, 35))
        self.funny_sayings.setObjectName("funny_sayings")
        self.funny_sayings.setAlignment(QtCore.Qt.AlignCenter)
        self.funny_sayings.setText("")
        font = QtGui.QFont()
        font.setPointSize(18)
        self.funny_sayings.setFont(font)
        self.funny_sayings.setStyleSheet("color: red")

        # Outcome label
        self.outcome_label = QtWidgets.QLabel(self.centralwidget)
        self.outcome_label.setGeometry(QtCore.QRect(120, 90, 581, 211))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.outcome_label.setFont(font)
        self.outcome_label.setObjectName("label")

        # Button Splitter
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(140, 500, 561, 23))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.splitter.setFont(font)
        self.splitter.setObjectName("splitter")

        # Win Percentage Label
        self.win_percentage_label = QtWidgets.QLabel(self.centralwidget)
        self.win_percentage_label.setGeometry(QtCore.QRect(0, 100, 800, 20))
        self.win_percentage_label.setObjectName("win_percentage_label")
        self.win_percentage_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.win_percentage_label.setFont(font)
        self.win_percentage_label.setText("Win Percentage: 0.00%")  # Initial value
        
        # Buttons
        button_info = {"Rock": "Gray", "Paper": "White", "Scissors": "Silver", "Lizard": "Green", "Spock": "Blue"}

        self.buttons = []
        for name, color in button_info.items():
            button = QtWidgets.QPushButton(name, self.splitter)
            button.setObjectName(name)
            text_color = "black" if name in ["Paper", "Scissors"] else "white"
            button.setStyleSheet(f"background-color: {color}; color: {text_color}")
            self.buttons.append(button)

        # Set Central Widget
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")

        # File Menu
        self.menuFile = self.menubar.addMenu("File")
        self.actionSave = self.menuFile.addAction("Save")
        self.actionLoad = self.menuFile.addAction("Load")
        self.actionReset = self.menuFile.addAction("Reset")
        self.actionExit = self.menuFile.addAction("Exit")
        self.actionExit.triggered.connect(MainWindow.close)
        
        # Connect the reset_game method to the Reset menu action
        self.actionReset.triggered.connect(self.reset_game)
        
        # Connect the save_game method to the Save menu action
        self.actionLoad.triggered.connect(self.load_game)
        
        # Connect the load_game method to the Load menu action
        self.actionSave.triggered.connect(self.save_game)
        
        # Help Menu
        self.menuHelp = self.menubar.addMenu("Help")
        self.actionAbout = self.menuHelp.addAction("About")
        self.actionAbout.triggered.connect(lambda: self.show_about_dialog(MainWindow))

        # Set Menu Bar
        MainWindow.setMenuBar(self.menubar)

        # Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Connect buttons to game logic functions
        for button in self.buttons:
            button.clicked.connect(lambda checked, btn=button: self.play(btn))

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Rock Paper Scissors Lizard Spock"))
            self.results_label.setText(_translate("MainWindow", ""))

    def play(self, button):
        player_choice = button.text()
        choices = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]
        computer_choice = random.choice(choices)
        
        # Funny sayings
        sayings = {
            1: "Rock crushes Lizard...",
            2: "Scissors cuts Paper...",
            3: "Paper covers Rock...",
            4: "Lizard Poisons Spock...",
            5: "Spock smashes Scissors...",
            6: "Scissors decapitates Lizard...",
            7: "Lizard eats Paper...",
            8: "Paper disproves Spock...",
            9: "Spock vaporizes Rock...",
            10: "Rock crushes Scissors...",
            11: "Tie Game!"} 
        
        if (player_choice == 'Rock' and computer_choice == 'Lizard') or (computer_choice == 'Rock' and player_choice == 'Lizard'):
            display = sayings[1]
        elif (player_choice == 'Scissors' and computer_choice == 'Paper') or (computer_choice == 'Scissors' and player_choice == 'Paper'):
            display = sayings[2]
        elif (player_choice == 'Paper' and computer_choice == 'Rock') or (computer_choice == 'Paper' and player_choice == 'Rock'):
            display = sayings[3]
        elif (player_choice == 'Lizard' and computer_choice == 'Spock') or (computer_choice == 'Lizard' and player_choice == 'Spock'):
            display = sayings[4]
        elif (player_choice == 'Spock' and computer_choice == 'Scissors') or (computer_choice == 'Spock' and player_choice == 'Scissors'):
            display = sayings[5]
        elif (player_choice == 'Scissors' and computer_choice == 'Lizard') or (computer_choice == 'Scissors' and player_choice == 'Lizard'):
            display = sayings[6]
        elif (player_choice == 'Lizard' and computer_choice == 'Paper') or (computer_choice == 'Lizard' and player_choice == 'Paper'):
            display = sayings[7]
        elif (player_choice == 'Paper' and computer_choice == 'Spock') or (computer_choice == 'Paper' and player_choice == 'Spock'):
            display = sayings[8]
        elif (player_choice == 'Spock' and computer_choice == 'Rock') or (computer_choice == 'Spock' and player_choice == 'Rock'):
            display = sayings[9]
        elif (player_choice == 'Rock' and computer_choice == 'Scissors') or (computer_choice == 'Rock' and player_choice == 'Scissors'):
            display = sayings[10]
        elif player_choice == computer_choice:
            display = sayings[11]

        self.funny_sayings.setText(display)
        
        # Game logic remains unchanged
        # Determine winner
        winner = self.determine_winner(player_choice, computer_choice)

        # Update scores and labels
        if winner == "Player":
            self.player_score += 1
            result_text = "Player wins!"
        elif winner == "Computer":
            self.computer_score += 1
            result_text = "Computer wins!"
        else:
            self.tie_game += 1
            result_text = "It's a tie!"

        total_games = self.player_score + self.computer_score + self.tie_game
        self.games_played_label.setText(f"Games Played: {total_games}")

        player_wins = self.player_score
        com_wins = self.computer_score
        tied_game = self.tie_game
        self.results_label.setText(f"Player Score: {player_wins} | Computer Score: {com_wins} | Tie games: {tied_game}")
        label_text = f"{result_text} You picked {player_choice}. The computer picked {computer_choice}."
        
        # Center label text
        self.outcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.outcome_label.setText(label_text)
        win_percentage = (self.player_score / total_games * 100) if total_games > 0 else 0
        self.win_percentage_label.setText(f"Win Percentage: {win_percentage:.2f}%")

        self.outcome_label.setText(label_text)
    
    def determine_winner(self, player_choice, computer_choice):
        # Win conditions for player
        win_conditions = {
            "Rock": ["Scissors", "Lizard"],
            "Paper": ["Rock", "Spock"],
            "Scissors": ["Paper", "Lizard"],
            "Lizard": ["Spock", "Paper"],
            "Spock": ["Scissors", "Rock"]
        }
        
        if player_choice == computer_choice:
            return "Tie"
        elif computer_choice in win_conditions[player_choice]:
            return "Player"
        else:
            return "Computer"

     # Config About menu    
    def show_about_dialog(self, MainWindow):
        QtWidgets.QMessageBox.about(
            MainWindow,
            "About",
            "This Rock Paper Scissor Lizard Spock game \nwas programmed by Brian Wall \n\nCopyright: \xa9 2023. \nLast updated: 7/16/2024"
        )

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.tie_game = 0
        self.games_played_label.setText("Games Played: 0")
        self.results_label.setText(f"Player Score: 0 | Computer Score: 0 | Tie games: 0")
        self.win_percentage_label.setText("Win Percentage: 0.00%")
        self.funny_sayings.setText("")
        self.outcome_label.setText("")

    def save_game(self):
        # Open a file dialog for the user to choose the file to save
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName()

        if file_path:
            try:
                # Prepare the data to be saved
                data = f"Player Score: {self.player_score}\n"
                data += f"Computer Score: {self.computer_score}\n"
                data += f"Tie games: {self.tie_game}\n"
                data += f"Win Percentage: {(self.player_score / (self.player_score + self.computer_score + self.tie_game) * 100) if (self.player_score + self.computer_score + self.tie_game) > 0 else 0:.2f}\n"
                
                # Encrypt the data
                encrypted_data = self.cipher_suite.encrypt(data.encode())
                
                with open(file_path, 'wb') as file:
                    # Save the encrypted data to the file
                    file.write(encrypted_data)
                
                QtWidgets.QMessageBox.information(None, "Game Saved", "Game saved successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error saving game: {str(e)}")
                
    def load_game(self):
        # Open a file dialog for the user to choose the file to load
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName()

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    # Read the encrypted data from the file
                    encrypted_data = file.read()

                # Decrypt the data
                decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
                
                # Parse the decrypted data
                lines = decrypted_data.split('\n')
                player_score = int(lines[0].split(":")[1].strip())
                computer_score = int(lines[1].split(":")[1].strip())
                tie_game = int(lines[2].split(":")[1].strip())
                win_percent = float(lines[3].split(":")[1].strip())
                
                # Update the game state with the loaded data
                self.player_score = player_score
                self.computer_score = computer_score
                self.tie_game = tie_game

                # Update UI labels
                total_games = self.player_score + self.computer_score + self.tie_game
                self.games_played_label.setText(f"Games Played: {total_games}")

                player_wins = self.player_score
                com_wins = self.computer_score
                tied_game = self.tie_game
                self.results_label.setText(f"Player Score: {player_wins} | Computer Score: {com_wins} | Tie games: {tied_game}")
                self.win_percentage_label.setText(f"Win Percentage: {win_percent:.2f}%")

                QtWidgets.QMessageBox.information(None, "Game Loaded", "Game loaded successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error loading game: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
