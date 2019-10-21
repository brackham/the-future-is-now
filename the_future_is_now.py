import os


def fix_bad_print(line):
    bad_strs = ['print \'', 'print \"']
    good_strs = ['print(\'', 'print(\"']
    for bad, good in zip(bad_strs, good_strs):
        if bad in line:
            line = line.replace(bad, good)
            if ' # ' in line:
                idx = line.find(' # ')
                line = line[:idx] + ')  ' + line[idx:]
                print(line)
                print('')
                print('')
            else:
                line += ')'
    return line


def main(path):
    python_files = []
    for root, subdirs, files in os.walk(path):
        for file in files:
            if file == 'the_future_is_now.py':
                continue
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    bad_strs = ['print \'', 'print \"']
    offenders = []
    for file in python_files:
        with open(file, 'r') as f:
            if any(bad_str in f.read() for bad_str in bad_strs):
                offenders.append(file)

    print('Messed with these files:')
    for file in offenders:
        print(file)
        with open(file, 'r') as f:
            lines = f.readlines()

        new_file = file.replace('.py', '_NEW.py')
        with open(new_file, 'w') as f:
            print('from __future__ import print_function', file=f)
            print('', file=f)
            for line in lines:
                line = line.rstrip('\n')
                if any(bad_str in line for bad_str in bad_strs):
                    line = fix_bad_print(line)
                    # print(line.rstrip('\n'))
                if line.endswith('\\)'):
                    line = line.rstrip('\\)')
                print(line, file=f)

    for file in offenders:
        with open(file, 'r') as f:
            for line in f:
                if 'print ' in line:
                    print('Found a problem still in: ', file)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Fix old print statements')
    parser.add_argument('-path', type=str, default=None, help='path')

    args = parser.parse_args()

    if args.path is None:
        sys.exit('Add a path to search with the -path flag.')

    main(args.path)
