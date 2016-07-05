import sys
import analyze_data
import os
import shutil
import aye_utils

from_directory, to_directory = sys.argv[1], sys.argv[2]
print("Grouping directory %s into %s" % (from_directory, to_directory))

def parse_label(file_path):
    file_name = analyze_data.split_name(file_path)
    matcher = aye_utils.hostnames_pattern.search(file_name)
    if matcher is None:
        print("Could not parse label from file path %s" % file_path)
        return None
    post_hostname = file_name[matcher.end():]
    return post_hostname.rsplit('t', 1)[0][1:]

def copy_contents_without_test(from_directory, to_directory):
    for file in analyze_data.get_files_in_directory(from_directory):
        if parse_label(file).startswith('test'):
            continue
        if not os.path.isdir(to_directory):
            os.mkdir(to_directory)
        new_file = '/'.join([to_directory, os.path.split(file)[-1]])
        if os.path.exists(new_file):
            print("Ignoring %s because it already exists" % file)
            continue

        shutil.copy2(file, to_directory)


for sequence_directory in analyze_data.get_sequence_directories(from_directory):
    label = parse_label(sequence_directory)
    if label is None or label == "": 
        print "Ignoring %s" % sequence_directory
        continue

    group_directory = '/'.join([to_directory, label])
    if not os.path.isdir(to_directory):
        os.makedirs(to_directory)
    copy_contents_without_test(sequence_directory, group_directory)
    print "Grouped contents of %s into %s" % (sequence_directory, group_directory)




