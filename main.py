#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

from vertex import *
from tree import *
from invariants import *
from html_parsing import *
from xml_parsing import *
from generate import *

import argparse
import subprocess


def compare_2_files(xml_filename, html_filename):
    tree = etree.parse(xml_filename)
    root = tree.getroot()

    body = tree.find('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body')
    text = body[0]
    xml_tree = get_tree_from_xml_text(text)

    f = open(html_filename)
    html_doc = f.read()
    f.close()

    soup = BeautifulSoup(html_doc, 'html5lib')
    html_tree = get_tree_from_html_text(soup.body)

    print('-' * 10, 'Trace html:')
    html_tree.trace()

    print('\n')
    print('-' * 10, 'Trace xml:')
    xml_tree.trace()

    if Tree.equal_trees(xml_tree, html_tree):
        print('Lists are consistent')
    else:
        print('Lists aren\'t consistent')


def main_compare(args):
    compare_2_files('/home/zhigan/Workspace/libre/5/example.odt_FILES/content.xml', '/home/zhigan/Workspace/libre/5/sample.html')


def process_odt(filename):
    subprocess.call(['/home/zhigan/Workspace/instdir/program/soffice', '--headless', \
                     '--convert-to', 'html', filename])
    dir_name = filename[filename.rfind('/') + 1 :] + '_FILES'
    subprocess.call(['unzip', '-d', dir_name, filename])

    html_filename = filename[filename.rfind('/') + 1 :filename.rfind('.')] + '.html'
    # print(html_filename)

    compare_2_files(dir_name + '/content.xml', html_filename)
    subprocess.call(['rm', '-r', dir_name])
    subprocess.call(['rm', html_filename])


def process_html(filename):
    subprocess.call(['/home/zhigan/Workspace/instdir/program/soffice', '--headless', \
                     '--convert-to', 'html', filename])
    dir_name = filename[filename.rfind('/') + 1 :] + '_FILES'
    subprocess.call(['unzip', '-d', dir_name, filename])

    html_filename = filename[filename.rfind('/') + 1 :filename.rfind('.')] + '.html'
    # print(html_filename)

    compare_2_files(dir_name + '/content.xml', html_filename)
    subprocess.call(['rm', '-r', 'document'])
    subprocess.call(['rm', html_filename])

def main_convert(args):
    if args.filename:
        if args.filename.endswith('odt'):
            process_odt(args.filename)
        elif args.filename.endswith('html'):
            process_html(args.filename)
        else:
            print('Acceptable only ODT and HTML files')
    else:
        print('Please specify filename with --filename')


def get_odt_file(tree):
    subprocess.call(['mkdir', 'odt_dir'])
    subprocess.call(['cp', '-r', 'patterns/test.odt_FILES', 'odt_dir'])

    SUFFIX = '</office:text></office:body></office:document-content>'
    f = open('odt_dir/test.odt_FILES/content.xml', 'a')
    f.write(generate_xml_from_tree(tree))
    f.write(SUFFIX)
    f.close()

    subprocess.call(['zip', '-0', '-X', 'odt_dir/doc.odt', 'odt_dir/test.odt_FILES/mimetype'])
    subprocess.call(['/home/zhigan/Workspace/instdir/program/soffice', '--headless', \
                     '--convert-to', 'html', 'odt_dir/doc.odt', '--outdir', 'odt_dir'])
    # exit(0)
    subprocess.call(['rm', '-r', 'odt_dir'])


# tree = get_random_tree([nested_list_depth_2], [])
# tree.trace()
# get_odt_file(tree)
# exit(0)


def main_generate(args):
    predicates = [nested_list_depth_2, paragraph_interrupts_list]

    cnt = 0
    for subset, indexes in zip(powerset(predicates), powerset(list([i for i in range(len(predicates) + 1)]))):
        tree = get_random_tree(subset, [])
        tree.trace()
        Tree.equal_trees(tree, tree)
        print('Test number {}'.format(cnt))
        print('for indexes', indexes)
        if Tree.equal_trees(tree, tree):
            print('Lists are consistent')
        else:
            print('Lists aren\'t consistent')
        cnt += 1


def main():
    # print(Tree.equal_trees(xml_tree, html_tree))
    #
    # tree1 = Tree(Vertex('paragraph'))
    # cur_tree = tree1
    # cur_tree.outerEdge = Tree(Vertex('list'))
    #
    # cur_tree.outerEdge.innerEdge = Tree(Vertex('list_item', 1))
    # cur_tree.outerEdge.innerEdge.outerEdge = Tree(Vertex('list_item', 2))
    #
    # print(XML_TAGS_FROM_TYPE_NAMES)
    # print(generate_xml_from_tree(tree1))
    # tree = get_random_tree([nested_list_depth_2], [])
    # tree.trace()
    #
    # print('traced')
    #
    # print(nested_list_depth_2(tree))

    parser = argparse.ArgumentParser(description='Testing system for convertion.')
    parser.add_argument('--mode', action='store', choices=['compare', 'convert', 'generate'], required=True)
    parser.add_argument('--filename', action='store')
    args = parser.parse_args()

    modes = {
        'compare'  : main_compare,
        'convert'  : main_convert,
        'generate' : main_generate
    }

    modes[args.mode](args)


if __name__ == '__main__':
    main()
