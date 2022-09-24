import os
import threading


def print_function(repo):
    while repo["thread_count"] > 0:
        if len(repo["prints"]) > 0:
            print(repo["prints"].pop())


def verification(search, repo):
    while repo["thread_count"] > 0:
        file = repo["verification"].pop()
        repo["prints"].append(file)
        if search in file:
            input()


def look_at_path(path, repo):
    repository["thread_count"] += 1

    try:
        items_at_path = os.listdir(path)
    except PermissionError:
        return
    except NotADirectoryError:
        repo["verification"].append(path)
        return

    for item in items_at_path:
        new_path = f"{path}\\{item}"
        th = threading.Thread(target=look_at_path, args=[new_path, repo])
        th.start()
        repo["threads"].append(th)

    repository["thread_count"] -= 1


if __name__ == "__main__":
    directory = "A:\\"
    search_conditions = input("Search:")

    repository = {"threads": [], "prints": [], "verification": [], "thread_count": 0}

    look_at_path(path=directory, repo=repository)

    threading.Thread(target=print_function, args=[repository]).start()
    threading.Thread(target=print_function, args=[search_conditions, repository]).start()
