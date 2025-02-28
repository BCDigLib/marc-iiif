import logging
import re

import paramiko
import os
import fnmatch

from paramiko import SFTPClient


class SSHConnection:
    """
    SSH connection to the IIIF server
    """
    image_dir: str
    sftp: SFTPClient
    files: list

    def __init__(self, connection_string: str, image_dir: str):
        """
        Constructor

        :type connection_string : object
        :type image_dir : str
        """
        connection_string_parts = connection_string.split('@')
        username = connection_string_parts[0]
        host = connection_string_parts[1]
        ssh = paramiko.client.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username)
        self.sftp = ssh.open_sftp()
        self.image_dir = image_dir
        self.files = self.sftp.listdir(self.image_dir)

    def upload_images(self, local_filepaths: list[str]) -> None:
        """
        Upload image files to remote directory

        :type local_filepaths: list[str] the local files to upload
        """
        for local_filepath in local_filepaths:
            file_name = os.path.split(local_filepath)
            self.sftp.put(local_filepath, f'{self.image_dir}/{file_name}')

    def list_images(self, image_base: str) -> list[str]:
        """
        List image files in remote directory

        Iterate through several variations on possible image file name bases if necessary.

        :type image_base: str the base of the filename to look for (e.g. ms-2020-020-142452)
        :rtype: list[str] a list of jp2 files in the image directory that match our image base
        """
        image_files = []

        # First try the bare image base.
        logging.info(f'Looking for {image_base}')
        image_files = self._list_files(image_base)
        if len(image_files) > 0:
            return image_files

        # No results? Try everything lowercased.
        image_base = image_base.lower()
        logging.info(f'Looking for {image_base}')
        image_files = self._list_files(image_base)
        if len(image_files) > 0:
            return image_files

        # Still no results? Add strategic dashes.
        image_base = re.sub(r'^([a-z]+)(\d+)',r'\1-\2', image_base)
        logging.info(f'Looking for {image_base}')
        image_files = self._list_files(image_base)
        if len(image_files) > 0:
            return image_files

        # Still no results? Convert underscores to dashes.
        image_base = image_base.replace('_','-')
        logging.info(f'Looking for {image_base}')
        image_files = self._list_files(image_base)
        if len(image_files) > 0:
            return image_files

        # Still nothing? Convert dashes to underscores.
        image_base = image_base.replace('-','_')
        logging.info(f'Looking for {image_base}')
        image_files = self._list_files(image_base)
        if len(image_files) > 0:
            return image_files

        # Still nada? Give up.
        return []

    def _list_files(self, image_base)->list[str]:
        image_files = []
        for file in self.files:
            if fnmatch.fnmatch(file, f'{image_base}*'):
                image_files.append(file)
        image_files.sort()
        return image_files