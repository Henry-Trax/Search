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
                    repo["thread_on"] = 0
                    return


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

    threads = []

    for item in items_at_path:
        new_path = f"{path}\\{item}"
        th = threading.Thread(target=look_at_path, args=[new_path, repo])
        th.start()
        threads.append(th)

    for thread in threads:
        thread.join()


def main():
    # directory = input("Location (C:\\ to search drive): ")
    # search_conditions = input("Search:")
    directory = "A:\\"
    search_conditions = "LICENSE"

    repository = {"verification": [], "thread_on": 1, "verification_on": 1, "results": []}

    look_at_path(path=directory, repo=repository)

    thread = threading.Thread(target=verification, args=[search_conditions, repository])
    thread.start()
    thread.join()
    repository["verification_on"] = 0

if __name__ == "__main__":
    now = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - now)
