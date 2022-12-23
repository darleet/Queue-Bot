
def is_admin(user_id):
    user_id = str(user_id)
    with open("admins.txt", "r") as f:
        for line in f:
            if user_id == line.strip():
                return True
        return False


def closeq():
    with open("open_status.txt", "w") as f:
        f.write("1")


def openq():
    with open("open_status.txt", "w") as f:
        f.write("0")


def check_status():
    with open("open_status.txt", "r") as f:
        if f.readline().strip() == "1":
            return True
        else:
            return False
