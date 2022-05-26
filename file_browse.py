import os
import fnmatch

def menu():
    print("[1] Change the directory: ")
    print("[2] Look for a specific file type(.mp3,.mp4,.wav,etc.): ")
    print("[3] Move up a directory: ")
    print("[4] Move down a directory: ")
    print("[5] Select a file: ")
    selection = int(input("Enter a number: "))
    if selection == 1:
        cd()
    elif selection == 2:
        file_type()
    elif selection == 3:
        up_dir()
    # elif selection == 4:
    # elif selection == 5:
    elif selection == 6:
        exit()
    else:
        print("Enter a valid selection: ")
        menu()


def cd():
    print("Enter the directory you want to browse(if you press space and enter you will be in the working directory): ")
    directory = input()
    if directory == " ":
        directory = "./"
    return directory

def file_type():
    print("Enter the file extension type: ")
    ext = input()
    if fnmatch.fnmatch(ext, '.*'):
        return ext
    else:
        print("The file type must start with a . ")
        print("Try again!")
        file_type()
def up_dir():
    pwd = cd()
    for dirs, files in os.walk(pwd):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = os.sep + file
            print(filepath)


cd()
menu()
pwd = cd()
type = file_type()
dirList = os.listdir("%s" % pwd)  # current directory
for subdir, dirs, files in os.walk(pwd):
    for file in files:
        # print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(type):
            print(filepath)
