import datetime
import os
import threading


def verification(search, repo):
    while repo["ver"] == 1:
        if len(repo["verification"]) > 0:
            file = repo["verification"].pop()
            print(file)

            if repo["cap_safe"] != "y" and search.lower() in file.lower():
                repo["results"].append(file)

            elif search in file:
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
        repo["verification"].append(f"Perm Error {path}")
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
    directory = input("Location (C:\\ to search drive):")
    wait = input("pause on result (y / n)      :")
    cap_safe = input("caps sensitive  (y / n)      :")
    search_conditions = input("Search                       :")
    # directory = "A:\\"
    # search_conditions = "LICENSE"
    now = datetime.datetime.now()

    repository = {"verification": [], "thread_on": 1, "results": [], "wait": wait, "ver": 1, "cap_safe": cap_safe}

    thread = threading.Thread(target=look_at_path, args=[directory, repository])
    ver = threading.Thread(target=verification, args=[search_conditions, repository])

    thread.start()
    ver.start()

    thread.join()
    repository["ver"] = 0

    os.system('cls' if os.name == 'nt' else 'clear')

    print(datetime.datetime.now() - now)

    for item in repository["results"]:
        print(item)



if __name__ == "__main__":
    while True:
        main()
