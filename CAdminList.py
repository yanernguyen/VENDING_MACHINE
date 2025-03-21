from CAdmin import *
import random
import string
import json
import os

class AdminList:
    FILE_PATH = "data/admin_data.json"

    def __init__(self):
        self.admins = []
        self.load_admins()

    def load_admins(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.admins = [Admin(**admin) for admin in data]

    def save_admins(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([admin.to_dict() for admin in self.admins], file, indent=4)

    def add_admin(self, username: str, password: str):

        if self.get_admin(username):
            print("Admin đã tồn tại!")
            return False
        self.admins.append(Admin(username, password))
        self.save_admins()
        return True

    def get_admin(self, username: str):
        for admin in self.admins:
            if admin.username == username:
                return admin
        return None

    def check_login(self, username, password):
        for admin in self.admins:
            if admin.username == username and admin.password == password:
                return True
        return False


