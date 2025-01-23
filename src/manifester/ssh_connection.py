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

    def __del__(self):
        """
        Destructor
        """
        self.sftp.close()

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

        :type image_base: str the base of the filename to look for (e.g. ms-2020-020-142452)
        :rtype: list[str] a list of jp2 files in the image directory that match our image base
        """
        files = self.sftp.listdir(self.image_dir)
        image_files = []
        for file in files:
            if fnmatch.fnmatch(file, f'{image_base}*jp2'):
                image_files.append(file)
        return image_files