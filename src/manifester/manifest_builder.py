from manifester.image import Image
from manifester.source_record import SourceRecord


def build_manifest(image_list: list[Image], source: SourceRecord) -> dict:
    """
    Build the manifest

    :param image_list: list[Image] the images to deliver
    :param source: SourceRecord the source record
    :return:
    """
    print(image_list[0])

    attribution = f'<p>{source.attribution}</p><p>Takedown notice: <a href="https://library.bc.edu/takedown-notice">https://library.bc.edu/takedown-notice</a></p>'

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
                'value': source.citation + ' ' + source.handle_url
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
    """
    Build a single sc:Canvas

    :param image: Image the image contained in the Canvas
    :return:
    """
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
    """
    Build a single structure

    :param image: Image the represented image
    :return:
    """
    return {
        '@id': image.range_url,
        '@type': 'sc:Range',
        'label': image.short_name,
        'canvases': [
            image.canvas_url
        ]
    }
