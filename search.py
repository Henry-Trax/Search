import datetime
import os
import threading


def verification(search, repo):
    while len(repo["threads"]) > 0:
        while len(repo["verification"]) > 0:
            file = repo["verification"].pop()
            print(file)
            if search in file:
                repo["results"].append(file)

                if repo["wait".lower()] == "y" and input("Enter To Continue, x to exit") == "x":
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
        repo["threads"].append(th)
        threads.append(th)

    for thread in threads:
        thread.join()


def main():
    directory = input("Location (C:\\\\ to search drive): ")
    wait = input("pause on result:")
    search_conditions = input("Search:")
    # directory = "A:\\"
    # search_conditions = "LICENSE"

    repository = {"verification": [], "thread_on": 1, "threads": [], "results": [], "wait": wait}

    thread = threading.Thread(target=look_at_path, args=[directory, repository])
    ver = threading.Thread(target=verification, args=[search_conditions, repository])

    repository["threads"].append(thread)

    thread.start()
    ver.start()

    thread.join()
    ver.join()

    for item in repository["results"]:
        print(item)


if __name__ == "__main__":
    main()
    print("over")
