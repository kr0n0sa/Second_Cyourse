import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore
from LogInPage import Ui_LogInPage
from SignUpPage import Ui_SignUpPage
from MainPage import Ui_MainPage

# შეაერთე ბაზა
conn = sqlite3.connect('UserInfo.sqlite3')
conn.row_factory = sqlite3.Row
c = conn.cursor()


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = QtWidgets.QMainWindow()
        self.login_ui = Ui_LogInPage()
        self.login_ui.setupUi(self.login_window)

        self.signup_window = QtWidgets.QMainWindow()
        self.signup_ui = Ui_SignUpPage()
        self.signup_ui.setupUi(self.signup_window)

        self.main_window = QtWidgets.QMainWindow()
        self.main_ui = Ui_MainPage()
        self.main_ui.setupUi(self.main_window)

        # ლოგინის ინიციალიზაცია
        self.login_ui.AgreementCheckBox.setEnabled(False)
        self.login_ui.LogInBtn.setEnabled(False)
        self.login_ui.UsernameInput.textChanged.connect(self.check_inputs)
        self.login_ui.PasswordInput.textChanged.connect(self.check_inputs)
        self.login_ui.AgreementCheckBox.stateChanged.connect(self.toggle_login_btn)
        self.login_ui.LogInBtn.clicked.connect(self.Login)
        self.login_ui.SignUpPagebtn.clicked.connect(self.show_signup)

        # რეგისტრაციის ინიციალიზაცია
        self.signup_ui.AgreementCheckBox.stateChanged.connect(self.toggle_signup_btn)
        self.signup_ui.SignUpBtn.clicked.connect(self.SignUp)
        self.signup_ui.LogInbtn.clicked.connect(self.show_login)
        self.signup_ui.AgreementCheckBox.stateChanged.connect(self.toggle_signup_btn)
        self.signup_ui.SignUpBtn.setEnabled(False)

        self.login_window.show()

    def check_inputs(self):
        username = self.login_ui.UsernameInput.text()
        password = self.login_ui.PasswordInput.text()
        enable = bool(username and password)
        self.login_ui.AgreementCheckBox.setEnabled(enable)
        if not enable:
            self.login_ui.LogInBtn.setEnabled(False)
            self.login_ui.AgreementCheckBox.blockSignals(True)
            self.login_ui.AgreementCheckBox.setChecked(False)
            self.login_ui.AgreementCheckBox.blockSignals(False)

    def toggle_login_btn(self, state):
        self.login_ui.LogInBtn.setEnabled(state == QtCore.Qt.Checked)

    def toggle_signup_btn(self, state):
        self.signup_ui.SignUpBtn.setEnabled(state == QtCore.Qt.Checked)


    def LoginPageReset(self, wrong_type):
        if wrong_type == "username":
            self.login_ui.ErrorLabel.setText("Wrong username")
        else:
            self.login_ui.ErrorLabel.setText("Wrong password")
        self.login_ui.AgreementCheckBox.setEnabled(False)
        self.login_ui.LogInBtn.setEnabled(False)
        self.login_ui.UsernameInput.setText("")
        self.login_ui.PasswordInput.setText("")

    def Login(self):
        username = self.login_ui.UsernameInput.text()
        password = self.login_ui.PasswordInput.text()
        try:
            result = c.execute('SELECT Password FROM UserInformation WHERE Username = ?', (username,)).fetchone()
            if result:
                if password == result['Password']:
                    print(f"{username} login successful")
                    self.login_window.close()
                    self.main_window.show()
                else:
                    print("wrong password")
                    self.LoginPageReset("password")
            else:
                print("wrong username")
                self.LoginPageReset("username")
        except Exception as e:
            print(f"Login error: {e}")
            self.login_ui.ErrorLabel.setText("An error occurred")

    def show_signup(self):
        self.login_window.close()
        self.signup_window.show()

    def show_login(self):
        self.signup_window.close()
        self.login_window.show()

    def SignUp(self):
        username = self.signup_ui.NewUsernameInput.text()
        password = self.signup_ui.NewPasswordInput.text()
        retype = self.signup_ui.RetypePasswordInput.text()

        if not username or not password:
            self.signup_ui.ErrorLabel.setText("Please fill all fields")
            return

        if password != retype:
            self.signup_ui.ErrorLabel.setText("Passwords do not match")
            return

        existing = c.execute('SELECT Username FROM UserInformation WHERE Username = ?', (username,)).fetchone()
        if existing:
            self.signup_ui.ErrorLabel.setText("User already exists")
            return

        try:
            c.execute('INSERT INTO UserInformation (Username, Password) VALUES (?, ?)', (username, password))
            conn.commit()
            self.signup_ui.ErrorLabel.setText("Registration successful!")
            self.signup_window.close()
            self.login_window.show()
        except Exception as e:
            self.signup_ui.ErrorLabel.setText("Error during registration")
            print(f"SignUp error: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec_())
