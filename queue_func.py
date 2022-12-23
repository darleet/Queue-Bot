import random


def in_queue(user_id):
    for filepath in ("queue.txt", "static_queue.txt"):
        counter = 1
        try:
            with open(filepath, "r") as f:
                for line in f:
                    items = line.split(",")
                    q_user_id, q_username, q_name = items[0], items[1], items[2]
                    if str(user_id) == q_user_id or str(user_id) == q_username:
                        return [counter, filepath]
                    counter += 1
        except IOError:
            open(filepath, "w")
    return False


def queue_enqueue(user_id, username, name, position=None):
    if in_queue(user_id):
        return False

    if position is None:
        with open("queue.txt", "a") as f:
            f.write(f"{user_id},{username},{name}\n")
        return True

    try:
        with open("static_queue.txt", "r") as f:
            data = f.readlines()
            data.insert(position-1, f"{user_id},{username},{name}\n")
        with open("static_queue.txt", "w") as f:
            f.writelines(data)
        return True
    except IOError:
        open("static_queue.txt", "w")
    return False


def queue_dequeue(username):
    data = in_queue(username)
    if data:
        index = data[0]-1
        filepath = data[1]
        try:
            with open(filepath, "r") as f:
                queue_data = f.readlines()
                queue_data.pop(index)
            with open(filepath, "w") as f:
                f.writelines(queue_data)
            return True
        except IOError:
            open(filepath, "r")
    return False


def queue_show():
    try:
        with open("static_queue.txt", "r") as f:
            str_data = "Очередь в данный момент:\n\n"
            counter = 0
            for line in f:
                counter += 1
                items = line.split(",")
                username, name = items[1], items[2].strip()
                str_data += f"{counter}. {name} (@{username})\n"
            if counter == 0:
                str_data = "Очередь пуста!\n"
            else:
                str_data += "\n"
    except IOError:
        open("static_queue.txt", "w")
        return "Ошибка файловой системы! (Internal Server Error 500)"

    try:
        with open("queue.txt", "r") as f:
            str_temp_data = "Скоро будут распределены в очередь:\n"
            empty = True
            for line in f:
                empty = False
                items = line.split(",")
                name = items[2].strip()
                str_temp_data += f"{name}, "
            if empty:
                return str_data
            return str_data + str_temp_data[:-2] + "."
    except IOError:
        return "Ошибка файловой системы! (Internal Server Error 500)"


def queue_form():
    data = []

    try:
        with open("queue.txt", "r+") as f:
            for line in f:
                items = line.split(",")
                user_id, username, name = items[0], items[1], items[2].strip()
                data.append([user_id, username, name])
            random.shuffle(data)
            f.truncate(0)
    except IOError: # Добавить обработку ошибки файловой системы
        pass

    with open("static_queue.txt", "a") as f:
        for user in data:
            user_id, username, name = user[0], user[1], user[2]
            f.write(f"{user_id},{username},{name}\n")


def next_student():
    try:
        with open("static_queue.txt", "r") as f:
            data = f.readlines()
            if len(data) == 1:
                data.pop(0)
                with open("static_queue.txt", "w") as f:
                    f.writelines(data)
                return False
            if len(data) == 0:
                return False
            else:
                data.pop(0)
                student = data[0].split(",")[1]
                with open("static_queue.txt", "w") as f:
                    f.writelines(data)
                return student
    except IOError:
        return False


def is_next(username, user_id):
    try:
        with open("static_queue.txt", "r") as f:
            data = f.readline()
            if user_id == data.split(",")[0] or username == data.split(",")[1]:
                return True
    except IOError:
        return False
    return False
