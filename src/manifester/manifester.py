"""
Produce a IIIF-compliant JSON manifest from a binary MARC file and a folder full of JP2s
"""
import json
import os.path
from datetime import datetime
from time import sleep
from typing import Optional, List

from pymarc import MARCReader
import urllib3
import sys
import logging as log

from manifester.alma_record import AlmaRecord
from manifester.aspace_client import lookup
from manifester.aspace_lookup import ASpaceLookup
from manifester.config import load_config
from manifester.image import Image
from manifester.manifest_builder import build_manifest
from manifester.ssh_connection import SSHConnection
from manifester.xlsx_reader import read_excel

src_path = os.path.dirname(__file__)
http = urllib3.PoolManager()

# Load the input we need to finish the process from CLI args, env files, and possibly
# user input during runtime.
config = load_config()

if config.verbosity:
    log.basicConfig(format="%(levelname)s: %(message)s", level=config.verbosity)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")

# Build a connection for SFTPing files if they entered an SSH connection string.
log.info(f'Opening SSH connection as {config.ssh}')
if config.ssh:
    remote_dir = SSHConnection(config.ssh, config.image_dir)
else:
    remote_dir = None


def main():
    """
    Main process
    """
    check_requirements()

    log.info(f'Reading {config.source_record}')

    # For now, anything that ends in '.mrc' is a binary MARC file, while everything else is a
    # ASpace record.
    # @todo figure out a better way to identify record types
    if config.source_record.endswith('.mrc'):
        source_records = read_marc_file(config.source_record, config.image_base)
    elif config.source_record.endswith('.xlsx'):
        source_records = read_excel(config.source_record)
    elif config.source_record.endswith('.csv'):
        source_records = read_marc_file(config.source_record, config.image_base)
    else:
        aspace_response = lookup(config.source_record, 'admin', config.aspace_passwd)
        source_records = [ASpaceLookup(aspace_response, config.image_base)]

    for source_record in source_records:
        process_record(source_record)


def process_record(source_record):
    # List the local image files, if requested. If they just provided SSH credentials, look
    # for the images on that server.
    image_base = config.image_base if config.image_base else source_record.identifier
    log.info(f'Globbing {config.ssh}{config.image_dir}/{image_base}...')
    if remote_dir:
        image_filenames = remote_dir.list_images(image_base)
    else:
        log.debug('No remote directory found')
        # @todo get a list of files directly from Cantaloupe
        image_filenames = []
    if len(image_filenames) == 0:
        raise Exception(f'Found no images for {image_base}')

    image_filenames.sort()
    log.info(f'Found {len(image_filenames)} image files. Looking up dimensions...')
    images = []
    for filename in image_filenames:
        images.append(build_image(filename))
    log.info(f'Build {len(images)} images')

    # Determine handle.
    handle = config.handle_url if config.handle_url else source_record.identifier
    handle_url = f'http://hdl.handle.net/2345.2/{handle}'
    log.info(f'Found {source_record.identifier}. Building manifest...')
    manifest = build_manifest(images, source_record, handle_url)
    write_manifest_file(source_record.identifier, manifest)
    log.info(f'Building view...')
    first_canvas = images[0].canvas_url
    view = build_view(source_record.identifier, source_record, handle_url, first_canvas)
    write_view_file(source_record.identifier, view)
    log.info(f'Building handles...')
    hdl_create_statements = [build_handles(source_record.identifier, config.handle_passwd, source_record.identifier)]
    log.info('Writing handle...')
    write_hdl_batchfile(hdl_create_statements)


def read_marc_file(marc_file: str, identifier: Optional[str]) -> List[AlmaRecord]:
    """
    Extract the source file from a binary MARC record

    :param marc_file: str full path to the MARC file
    :param identifier: Optional[str] the records identifier; if None, the MMS will be used
    :return: [AlmaRecord] the records in the file
    """
    with open(marc_file, 'rb') as bibs:
        reader = MARCReader(bibs)
        return [AlmaRecord(source_record, identifier=identifier) for source_record in reader]


def build_image(filename: str) -> Image:
    """
    Build a single image

    :param filename: str the filename of the image
    :return: Image the image file
    """
    image = Image(filename, config.iiif_base_url)

    log.info(f'...fetching {image.info_url}')
    r = http.request('GET', image.info_url)
    info = json.loads(r.data.decode('utf-8'))

    image.height = info['height']
    image.width = info['width']
    log.info(f'{image.short_name} - {image.height}x{image.width}')
    sleep(.5)
    return image


def write_view_file(identifier: str, view: str) -> None:
    """
    Write a single view file

    :param identifier: str the identifier
    :param view: str the view file contents
    :return: None
    """
    filename = f'{config.view_filename}' if config.view_filename else f'{identifier}.html'
    fh = open(filename, 'w')
    fh.write(view)
    fh.close()


def write_manifest_file(identifier: str, manifest: dict):
    """
    Write the manifest to a file
    :param identifier: str record identifier
    :param manifest: dict the manifest values
    :return:
    """
    filename = f'{config.manifest_filename}' if config.manifest_filename else f'{identifier}.json'
    fh = open(filename, 'w')
    fh.write(json.dumps(manifest))
    fh.close()


def write_hdl_batchfile(hdl_create_statements: List[str]):
    """
    Write the handle create statements to a file
    :param hdl_create_statements: list the list of handle create statements
    :return:
    """
    hdl_file_title = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    fh = open(f'handles-{hdl_file_title}-hdl.txt', 'w')
    all_hdl_create_statements = '\n'.join(hdl_create_statements)
    fh.write(all_hdl_create_statements)
    fh.close()


def build_view(identifier: str, record: object, handle_url: str, first_canvas: str):
    """
    Build view file text

    :param identifier: str the identifier
    :param record: object the MARC record
    :param first_canvas: str the Canvas of the first image
    :param handle_url: str the full URL of the handle
    :return:str the text of the view file
    """
    # Build from an HTML template.
    with open(f'{src_path}/view-template.html') as fh:
        html = fh.read()
    html = html.replace('__RECORD_TITLE__', record.title)
    html = html.replace('__RECORD_IDENTIFIER__', identifier)
    html = html.replace('__HANDLE_URL__', handle_url)
    html = html.replace('__FIRST_CANVAS__', first_canvas)
    return html


def build_handles(identifier, hdl_password, mms: str):
    """
    Build Handle bulk file

    :param identifier: str the identifier
    :param hdl_password: str the Handle server password
    :param mms: str the MMS number of the MARC record
    :return: str the text of the Hanlde bulk file
    """
    # Build from a text template.
    with open(f'{src_path}/handle-template.txt') as fh:
        hdl_text = fh.read()
    hdl_text = hdl_text.replace('__RECORD_IDENTIFIER__', identifier)
    hdl_text = hdl_text.replace('__RECORD_MMS__', mms)
    hdl_text = hdl_text.replace('__HANDLE_PASSWORD__', hdl_password)
    return hdl_text


def check_requirements():
    """
    Throw an error if something is amiss

    :return: None
    """
    # Uses Literal String Interpolation, available only in Python 3.6+
    if sys.version_info < (3, 6):
        raise Exception('Requires python 3.6 or higher')
