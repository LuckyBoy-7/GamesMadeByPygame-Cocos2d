import os


def copy_file(name):
    with open(name, mode="r", encoding="utf-8") as f:
        if not os.path.exists("storage"):
            os.mkdir("storage")

        spliced_name = os.path.join("storage", name)
        path_, file = os.path.split(spliced_name)
        if not os.path.exists(path_):
            os.makedirs(path_)

        with open(spliced_name, "w") as aim_file:
            aim_file.write(f.read())


def traverse_dirs(name):
    for n in os.listdir(name):
        spliced_name = os.path.join(name, n)
        if os.path.isdir(spliced_name):
            traverse_dirs(spliced_name)
        else:
            copy_file(spliced_name)


traverse_dirs("target_file")
