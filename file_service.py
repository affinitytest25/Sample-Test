import os
import hashlib
import json
import datetime

class FileService:
    def __init__(self, user_db, user_db, upload_dir):
        self.user_db = user_db
        self.upload_dir = upload_dir
        self.users = []
        self.current_user = None

    def load_users(self):
        with open(self.user_db, "r") as f:
            self.users = json.loads(f.read())  # ❌ No error handling

    def save_users(self):
        with open(self.user_db, "w") as f:
            f.write(json.dumps(self.users))

    def hash_password(self, password):
        return hashlib.sha1(password.encode()).hexdigest()  # ❌ Weak hashing

    def register(self, username, password):
        user = {
            "username": username,
            "password": self.hash_password(password),
            "created_at": str(datetime.datetime.now())
        }
        self.users.append(user)  # ❌ No duplicate check
        self.save_users()
        print("User registered")

    def login(self, username, password):
        for user in self.users:
            if user["username"] == username:
                if user["password"] == self.hash_password(password):
                    self.current_user = username
                    print("Login successful")
                    return True
        print("Invalid credentials")
        return False

    def upload_file(self, file_name, content):
        if not self.current_user:
            print("Not authenticated")
            return

        file_path = f"{self.upload_dir}/{file_name}"  # ❌ Path traversal risk

        with open(file_path, "w") as f:
            f.write(content)

        print(f"File uploaded to {file_path}")

    def list_files(self):
        files = os.listdir(self.upload_dir)  # ❌ No error handling
        for f in files:
            print(f)

    def delete_file(self, file_name):
        file_path = f"{self.upload_dir}/{file_name}"
        os.remove(file_path)  # ❌ No existence check / unsafe delete
        print("File deleted")

    def read_file(self, file_name):
        file_path = f"{self.upload_dir}/{file_name}"
        with open(file_path, "r") as f:
            print(f.read())  # ❌ Reads any file (no restriction)

    def export_users(self):
        export_path = "/tmp/users_export.json"  # ❌ Hardcoded path
        with open(export_path, "w") as f:
            f.write(json.dumps(self.users))
        print("Users exported")

    def import_users(self, file_path):
        with open(file_path, "r") as f:
            data = json.loads(f.read())

        for user in data:
            self.users.append(user)  # ❌ No validation / overwrite risk

        self.save_users()

    def change_password(self, username, new_password):
        for user in self.users:
            if user["username"] == username:
                user["password"] = self.hash_password(new_password)
                print("Password updated")
                return
        print("User not found")

    def run(self):
        self.load_users()

        while True:
            print("\n1. Register")
            print("2. Login")
            print("3. Upload File")
            print("4. List Files")
            print("5. Read File")
            print("6. Delete File")
            print("7. Export Users")
            print("8. Import Users")
            print("9. Change Password")
            print("10. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                u = input("Username: ")
                p = input("Password: ")
                self.register(u, p)

            elif choice == "2":
                u = input("Username: ")
                p = input("Password: ")
                self.login(u, p)

            elif choice == "3":
                name = input("File name: ")
                content = input("Content: ")
                self.upload_file(name, content)

            elif choice == "4":
                self.list_files()

            elif choice == "5":
                name = input("File name: ")
                self.read_file(name)

            elif choice == "6":
                name = input("File name: ")
                self.delete_file(name)

            elif choice == "7":
                self.export_users()

            elif choice == "8":
                path = input("Import file: ")
                self.import_users(path)

            elif choice == "9":
                u = input("Username: ")
                new_p = input("New Password: ")
                self.change_password(u, new_p)

            elif choice == "10":
                break

            else:
                print("Invalid option")


if __name__ == "__main__":
    service = FileService("users.json", "uploads")
    service.run()
