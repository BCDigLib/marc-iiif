# this script takes a binary MARC file and a folder full of JP2s to produce a IIIF-compliant JSON manifest
# usage: |manifest.py records.mrc hdl_passwd| where records.mrc is a binary marc file containing bibliographic records
# for the items for which you're creating manifests and hdl_passwd is the Handle password. This script must be run from
# within a folder containing all of the relevant images formatted as JP2s, and the images must also be uploaded to the
# library IIIF server before running the script.

import json
import os
from datetime import datetime

from pymarc import MARCReader, Field
import requests
import sys

base_url = 'https://iiif.bc.edu/iiif/2/'


def main():
    check_requirements()

    hdl_create_statements = []
    hdl_passwd = sys.argv[2]

    with open(sys.argv[1], 'rb') as bibs:
        reader = MARCReader(bibs)
        # initial for-loop lets you process a collection with multiple records if necessary
        for record in reader:
            # gather file / record identifiers
            long_identifier = str(record['001'])
            identifier = long_identifier[6:len(long_identifier)]
            # create a list  of jp2s in the jp2 directory that contain the identifier for the record in question
            # this list gets passed into the json building functions.
            file_list = []
            for file in os.listdir('jp2s/'):
                if identifier in file:
                    file_list.append(file)
            # this list will be unordered, so sort it
            file_list.sort()
            # figure out which library it's from and route it to the proper function

            try:
                manifest = build_law_metadata(file_list, record, identifier) if "BCLL RBR" in record['510'][
                    'a'] else build_burns_metadata(file_list, record, identifier)
            except KeyError:
                manifest = build_burns_metadata(file_list, record, identifier)

            # add if statement to look for cartographic records, determined by an 'e' in the 6th position of the LDR

            write_manifest_file(identifier, manifest)

            view = build_view(identifier, record)
            write_view_file(identifier, view)

            hdl_create_statements.append(build_handles(identifier, hdl_passwd))
    bibs.close()

    write_hdl_batchfile(hdl_create_statements)


def write_view_file(identifier, view):
    view_file = open('view/' + identifier, 'w')
    view_file.write(view)
    view_file.close()


def write_manifest_file(identifier, manifest):
    manifest_file = open('manifests/' + identifier + '.json', 'w')
    manifest_file.write(json.dumps(manifest))
    manifest_file.close()


def write_hdl_batchfile(hdl_create_statements):
    hdl_file_title = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    hdl_out = open('hdl/handles-' + hdl_file_title + '.txt', 'w')
    all_hdl_create_statements = '\n'.join(hdl_create_statements)
    hdl_out.write(all_hdl_create_statements)
    hdl_out.close()


def build_law_metadata(file_list, record, identifier):
    # gather metadata
    title = record.title
    attribution = "Though the copyright interests have not been transferred to Boston College, all of the items in the " \
                  "collection are in the public domain."
    publication_year = record.pubyear
    date = publication_year if publication_year is not None else ''

    room = record['510']['a']
    if record['510']['c'] is not None:
        room = str(record['510']['a']) + " " + str(record['510']['c'])
    citation = str(title) + ", " + str(
        date) + ", " + room + ", Daniel R. Coquillette Rare Book Room, Boston College Law Library, http://hdl.handle.net/2345.2/" + identifier + "."
    # build all the json
    blob = {'@context': 'http://iiif.io/api/presentation/2/context.json',
            '@id': 'https://library.bc.edu/iiif/manifests/'
                   + identifier + '.json', '@type': 'sc:Manifest', 'label': str(title),
            'thumbnail': base_url + identifier
                         + '_0001.jp2/full/!200,200/0/default.jpg', 'viewingHint': 'paged', 'attribution': attribution,
            'metadata': [
                {'handle': 'http://hdl.handle.net/2345.2/' + identifier},
                {'label': 'Preferred Citation', 'value': citation}],
            'sequences': build_sequence(file_list), 'structures': build_structures(file_list)}
    return blob


def build_burns_metadata(file_list, record, identifier):
    # gather metadata
    print(type(record))
    print(record)
    title = record.title
    attribution = "Though the copyright interests have not been transferred to Boston College, all of the items in the " \
                  "collection are in the public domain."
    publication_year = record.pubyear
    date = publication_year if publication_year is not None else ''

    citation = title + ", " + date + ", " + ", John J. Burns Library, Boston College, http://hdl.handle.net/2345.2/" \
               + identifier + "."
    # build all the json
    blob = {'@context': 'http://iiif.io/api/presentation/2/context.json',
            '@id': 'https://library.bc.edu/iiif/manifests/'
                   + identifier + '.json', '@type': 'sc:Manifest', 'label': title,
            'thumbnail': base_url + identifier
                         + '_0001.jp2/full/!200,200/0/default.jpg', 'viewingHint': 'paged', 'attribution': attribution,
            'metadata': [
                {'handle': '"http://hdl.handle.net/2345.2/' + identifier},
                {'label': 'Preferred Citation', 'value': citation}],
            'sequences': build_sequence(file_list), 'structures': build_structures(file_list)}
    return blob


# eventually need to add a new function, build_cartographic_metadata. Information on metadata formatting to be provided
# by Burns Public Services.

def build_sequence(file_list):
    sequence = [{'@type': 'sc:Sequence', 'canvases': []}]
    for file in file_list:
        short_name = file[0:file.index('.')]
        counter = short_name[len(short_name) - 4:len(short_name)]
        cui = short_name[0:len(short_name) - 5]
        url = base_url + file + '/info.json'
        print(url)
        call = requests.get(url)
        info = call.json()
        try:
            height = info['height']
            width = info['width']
            blob = {'@id': base_url + cui + '/canvas/' + counter, '@type': 'sc:Canvas',
                    'label': short_name, 'width': width,
                    'height': height, 'images': [{'@id': base_url + cui + '/' + counter + '/annotation/1',
                                                  '@type': 'oa:Annotation',
                                                  'on': base_url + cui + '/canvas/' + counter,
                                                  'motivation': 'sc:painting',
                                                  'resource': {
                                                      '@id': base_url + file + '/full/full/0/default.jpg',
                                                      '@type': 'dctypes:Image',
                                                      'format': 'image/jpeg', 'width': width, 'height': height,
                                                      'service': {'@context': 'http://iiif.io/api/image/2/context.json',
                                                                  '@id': base_url + file,
                                                                  'profile': 'http://iiif.io/api/image/2/level2.json'}}}]}
            sequence[0]['canvases'].append(blob)
        except KeyError:
            print(file + ' is not on the server or the server is otherwise not responding as expected.')
            continue
    return sequence


def build_structures(file_list):
    structures = []
    index = 0
    for file in file_list:
        short_name = file[0:file.index('.')]
        counter = short_name[len(short_name) - 4:len(short_name)]
        cui = short_name[0:len(short_name) - 5]
        blob = {'@id': base_url + cui + '/range/r-' + str(index), '@type': 'sc:Range',
                'label': short_name,
                'canvases': [base_url + cui + '/canvas/' + counter]}
        index += 1
        structures.append(blob)
    return structures


def build_view(identifier, record):
    title = record.title
    blob = '<!DOCTYPE html>\n<html>\n<head>\n<script async src="https://www.googletagmanager.com/gtag/js?id=UA-3008279-23"></script>' \
           '\n<script src="/iiif/bc-mirador/gtag.js"></script>\n<title>' + identifier + '</title>\n' \
                                                                                        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' \
                                                                                        '<link rel="stylesheet" type="text/css" href="/iiif/build/mirador/css/mirador-combined.css"></link>\n' \
                                                                                        '<link rel="stylesheet" type="text/css" href="/iiif/bc-mirador/mirador-bc.css"></link>\n' \
                                                                                        '<link rel="stylesheet" type="text/css" href="/iiif/bc-mirador/slicknav.css"></link>\n' \
                                                                                        '<script type="text/javascript" src="/iiif/build/mirador/mirador.js"></script>\n' \
                                                                                        '<script type="text/javascript" src="/iiif/bc-mirador/jquery.slicknav.min.js"></script>\n' \
                                                                                        '<script type="text/javascript" src="/iiif/bc-mirador/downloadMenu.js"></script>\n' \
                                                                                        '</head>\n<body>\n<div id="viewer"></div>\n<script type="text/javascript">\nwindow.mdObj = {MIRADOR_DATA: [' \
                                                                                        '{"manifestUri": "https://library.bc.edu/iiif/manifests/' + identifier + '.json","location": "Boston College",' \
                                                                                                                                                                 '"title":"' + title + '"}],MIRADOR_WOBJECTS: [{"canvasID": "' + base_url + identifier + '/canvas/0001",' \
                                                                                                                                                                                                                                                         '"loadedManifest": "https://library.bc.edu/iiif/manifests/' + identifier + '.json","viewType": "ImageView"}],' \
                                                                                                                                                                                                                                                                                                                                    'MIRADOR_BUTTONS: [{"label": "View Library Record","iconClass": "fa fa-external-link","attributes": {' \
                                                                                                                                                                                                                                                                                                                                    '"class": "handle","href": "http://hdl.handle.net/2345.2/' + identifier + '","target": "_blank"}}]};\n' \
                                                                                                                                                                                                                                                                                                                                                                                                              '</script>\n<script type="text/javascript" src="/iiif/bc-mirador/bcViewer.js"></script>\n' \
                                                                                                                                                                                                                                                                                                                                                                                                              '</body>\n</html>'
    return blob


def build_handles(identifier, hdl_password):
    return f'CREATE 2345.2/{identifier}\n' \
           f'100 HS_ADMIN 86400 1110 ADMIN 300:111111111111:2345.2/{identifier}\n' \
           f'300 HS_SECKEY 86400 1100 UTF8 {hdl_password}\n' \
           f'201 URL 86400 1110 UTF8 https://bclib.bc.edu/libsearch/bc/mms/{identifier}\n'


def check_requirements():
    # Uses Literal String Interpolation, available only in Python 3.6+
    if sys.version_info < (3, 6):
        raise Exception('Requires python 3.6 or higher')


main()
