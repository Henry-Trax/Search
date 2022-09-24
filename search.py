import datetime
import os
import threading


def verification(search, repo):
    while repo["verification_on"] == 1:
        if len(repo["verification"]) > 0:
            file = repo["verification"].pop()
            print(file)
            if search in file:
                repo["results"].append(search)

                if input("Enter To Continue, x to exit") == "x":
                    repo["verification_on"] = 0
                    repo["thread_on"] = 0


def look_at_path(path, repo):
    if "thread_on" == 0:
        return

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


def main():
    directory = input("Location (C:\\ to search drive): ")
    search_conditions = input("Search:")

    repository = {"threads": [], "verification": [], "thread_on": 1, "verification_on": 1, "results": []}

    look_at_path(path=directory, repo=repository)

    threading.Thread(target=verification, args=[search_conditions, repository]).start()

    while len(repository["threads"]) > 0:
        repository["threads"].pop().join()

    repository["verification_on"] = 0
    for item in repository["results"]:
        print(item)


if __name__ == "__main__":
    now = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - now)
