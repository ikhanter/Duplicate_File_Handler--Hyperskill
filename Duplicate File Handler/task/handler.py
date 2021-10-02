# import argparse
import os
# import string
import sys
import hashlib

filelist = []
arguments = sys.argv
if len(arguments) == 1:
    print('Directory is not specified')
    sys.exit()

root_dir = arguments[1]

file_format = input('Enter file format: ')
print()
selector = False
print('''Size sorting option:
1. Descending
2. Ascending

Enter a sorting option:''')

order_option = input()
while order_option != '1' and order_option != '2':
    print('Wrong option')
    order_option = input()

for root, dirs, files in os.walk(f'{root_dir}', topdown=True):
    for name in files:
        current_file_path = os.path.join(root, name)
        if file_format != '':
            file_ext = os.path.splitext(current_file_path)[-1][1:]
            if file_ext == file_format:
                filelist.append(tuple([current_file_path, os.path.getsize(current_file_path)]))
        else:
            filelist.append(tuple([current_file_path, os.path.getsize(current_file_path)]))

if order_option == '1':
    filelist.sort(key=lambda x: (-x[1], x[0]))
elif order_option == '2':
    filelist.sort(key=lambda x: (x[1], x[0]))

filedict = dict()

for element in filelist:
    if filedict.get(element[1]) is None:
        filedict[element[1]] = []
    filedict[element[1]].append(element[0])

for key, val in filedict.items():
    print(key, 'bytes')
    for i in val:
        print(i)
    print()

print('Check for duplicates?')
duplicate_choice = input()

dict_hashed_files = dict()

while duplicate_choice != 'yes' and duplicate_choice != 'no':
    print('Wrong option')
    duplicate_choice = input()

for key, val in filedict.items():
    for i in val:
        f = open(i, 'rb')
        f_content = f.readline()
        f_hashed = hashlib.md5()
        f_hashed.update(f_content)
        f_hash = f_hashed.hexdigest()
        if dict_hashed_files.get(f_hash) is None:
            dict_hashed_files[f_hash] = []
        dict_hashed_files[f_hash].append(i)
        f.close()

del_list = []
for key, val in dict_hashed_files.items():
    if len(val) == 1:
        del_list.append(key)

for i in del_list:
    del dict_hashed_files[i]

counter = 0
duplicates = []

size_announcer = ''
for key1, val1 in dict_hashed_files.items():
    for key2, val2 in filedict.items():
        if val1[0] in val2:
            if size_announcer != key2:
                size_announcer = key2
                print()
                print(f'{size_announcer} bytes')
            break
    print(f'Hash: {key1}')
    for file in val1:
        counter += 1
        print(f'{counter}. {file}')
        duplicates.append(tuple([counter, file]))

print()
print('Delete files?')
selector = input()
cleared_space = 0

while selector != 'yes' and selector != 'no':
    print('Wrong option')
    selector = input()

if selector == 'yes':
    print()
    files_for_deleting = None
    while files_for_deleting is None:
        print('Enter file numbers to delete:')
        try:
            files_for_deleting = [int(i) for i in input().split()]
            if files_for_deleting == []:
                print('Wrong option')
                files_for_deleting = None
        except:
            print('Wrong option')
            files_for_deleting = None

    while max(files_for_deleting) > counter:
        print('Wrong option')

    for i in files_for_deleting:
        for pair in duplicates:
            if i in pair:
                cleared_space += os.path.getsize(pair[1])
                os.remove(pair[1])
                break

    print(f'Total freed up space: {cleared_space} bytes')
