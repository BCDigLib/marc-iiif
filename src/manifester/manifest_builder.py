from manifester.image import Image
from manifester.source_record import SourceRecord


def build_manifest(image_list: list[Image], source: SourceRecord) -> dict:
    attribution = "Though the copyright interests have not been transferred to Boston College, all of the items in the " \
                  "collection are in the public domain."

    print(image_list[0])
    # Build the JSON
    return {
        '@context': 'http://iiif.io/api/presentation/2/context.json',
        '@id': source.manifest_url,
        '@type': 'sc:Manifest',
        'label': source.title,
        'thumbnail': image_list[0].thumbnail_url,
        'viewingHint': 'paged',
        'attribution': attribution,
        'metadata': [
            {
                'handle': source.handle_url
            },
            {
                'label': 'Preferred Citation',
                'value': source.citation
            }

        ],
        'sequences':
            [
                {
                    '@type': 'sc:Sequence',
                    'canvases': [build_canvas(image) for image in image_list]
                }
            ],
        'structures': [build_structure(image) for image in image_list]
    }


def build_canvas(image: Image):
    return {
        '@id': image.canvas_url,
        '@type': 'sc:Canvas',
        'label': image.short_name,
        'width': image.width,
        'height': image.height,
        'images': [
            {
                '@id': image.annotation_url,
                '@type': 'oa:Annotation',
                'on': image.canvas_url,
                'motivation': 'sc:painting',
                'resource': {
                    '@id': f'{image.image_url}/full/full/0/default.jpg',
                    '@type': 'dctypes:Image',
                    'format': 'image/jpeg',
                    'width': image.width,
                    'height': image.height,
                    'service': {
                        '@context': 'http://iiif.io/api/image/2/context.json',
                        '@id': image.image_url,
                        'profile': 'http://iiif.io/api/image/2/level2.json'
                    }
                }
            }
        ]
    }


def build_structure(image: Image):
    return {
        '@id': image.range_url,
        '@type': 'sc:Range',
        'label': image.short_name,
        'canvases': [
            image.canvas_url
        ]
    }


def build_structures(image_list: list[Image]):
    """
    Build the IIIF structures

    :param image_list: the list of image files to process
    :return: list[dict]
    """
    structures = []
    index = 0
    for file in image_list:
        short_name = file[0:file.index('.')]
        counter = short_name[len(short_name) - 4:len(short_name)]
        cui = short_name[0:len(short_name) - 5]
        blob = {'@id': base_url + cui + '/range/r-' + str(index), '@type': 'sc:Range',
                'label': short_name,
                'canvases': [base_url + cui + '/canvas/' + counter]}
        index += 1
        structures.append(blob)
    return structures
