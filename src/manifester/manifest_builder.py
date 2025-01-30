from manifester.image import Image
from manifester.source_record import SourceRecord


def build_manifest(file_list: list[Image], source: SourceRecord) -> dict:
    attribution = "Though the copyright interests have not been transferred to Boston College, all of the items in the " \
                  "collection are in the public domain."

    # build all the json
    first_image = file_list[0];
    return {
        '@context': 'http://iiif.io/api/presentation/2/context.json',
        '@id': source.manifest_url,
        '@type': 'sc:Manifest',
        'label': source.title,
        'thumbnail': first_image.thumbnail_url,
        'viewingHint': 'paged',
        'attribution': attribution,
        'metadata': [
            {
                'handle': source.handle_url,
                {
                    'label': 'Preferred Citation',
                    'value': source.citation
                }
        ],
        'sequences': build_sequence(file_list),
        'structures': build_structures(file_list)
    }


def build_sequence(file_list) -> list[dict]:
    """
    Build a IIIF sequence

    :param file_list: the list of image files to process
    :return: list[dict]
    """
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
                                                      'service': {
                                                          '@context': 'http://iiif.io/api/image/2/context.json',
                                                          '@id': base_url + file,
                                                          'profile': 'http://iiif.io/api/image/2/level2.json'}}}]}
            sequence[0]['canvases'].append(blob)
        except KeyError:
            print(file + ' is not on the server or the server is otherwise not responding as expected.')
            continue
    return sequence


def build_canvas(image: Image):
    blob = {
        '@id': image.image_url,
        '@type': 'sc:Canvas',
        'label': image.short_name,
        'width': image.width,
        'height': image.height,
        'images': [
            {
                '@id': base_url + cui + '/' + counter + '/annotation/1',
                '@type': 'oa:Annotation',
                'on': base_url + cui + '/canvas/' + counter,
                'motivation': 'sc:painting',
                'resource': {
                    '@id': base_url + file + '/full/full/0/default.jpg',
                    '@type': 'dctypes:Image',
                    'format': 'image/jpeg',
                    'width': width,
                    'height': height,
                    'service': {
                        '@context': 'http://iiif.io/api/image/2/context.json',
                        '@id': base_url + file,
                        'profile': 'http://iiif.io/api/image/2/level2.json'
                    }
                }
            }
        ]
    }


def build_structures(file_list):
    """
    Build the IIIF structures

    :param file_list: the list of image files to process
    :return: list[dict]
    """
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
