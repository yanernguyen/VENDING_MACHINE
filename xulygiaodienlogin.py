from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from CAdminList import AdminList



class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)  # Load file login.ui
        self.setWindowTitle("Đăng nhập")
        self.dinhnghianutlenh()


    def dinhnghianutlenh(self):
        self.pushButton_login.clicked.connect(self.login)

    def login(self):
        from xulygiaodienmanager import ManagerWindow

        try:
            admin_list = AdminList()
            username = self.lineEdit_name.text().strip()
            password = self.lineEdit_password.text().strip()
            print(username, password)

            if admin_list.check_login(username, password):
                QMessageBox.information(self, "Success", "Đăng nhập thành công!")
                self.manager_window = ManagerWindow(username)
                self.manager_window.show()
                self.hide()
                return username
            else:
                QMessageBox.warning(self, "Error", "Sai tài khoản hoặc mật khẩu!")

        except Exception :
            print('Lỗi')