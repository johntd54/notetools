"""Files handling"""
import os
import shutil

import arrow

try:
    from google.colab import drive, files
except ImportError as error:
    print('`google.colab` should be accessible, otherwise, use')
    print('`pip install git+https://github.com/googlecolab/colabtools`')
    raise error


MOUNT_POINT = '/gdrive'
BASE_GOOGLE_DRIVE = 'My Drive'
drive.mount(MOUNT_POINT)


class GDrive():
    """Handler to quickly and safely access file

    The most important tenet is: do not delete anything that is not created
    in the session. As a result, any new file will be created in a folder
    /My Drive/Colab/YYYYMMDD-HHmm. Copying, removing methods will assume the
    source or destination inside this sub-folder.
    """

    def __init__(self, sub_folder=None):
        """Initialize the object"""

        sub_folder = sub_folder if sub_folder else arrow.now().format('YYYYMMDD-HHmm')
        self._base_dir = os.path.join(MOUNT_POINT, BASE_GOOGLE_DRIVE)
        self._sub_folder = os.path.join(
            self._base_dir,
            'Colab',
            sub_folder)

        os.makedirs(self._sub_folder, exist_ok=True)
        print('Sub folder {} is created'.format(self._sub_folder))

    def get_base_dir(self):
        """Get the base Google Drive directory"""
        return self._base_dir

    def get_subfolder(self):
        """Get the sub-folder directory"""
        return self._sub_folder

    def from_drive(self, source, destination='', from_subfolder=True):
        """Copy from drive to the current VM destination

        # Arguments
            source [str]: the path to file or folder
            destination [str]: the copy destination
            from_subfolder [bool]: whether the source is relative to subfolder

        # Returns
            [str]: the destination file/folder
        """
        if from_subfolder:
            source = os.path.join(self._sub_folder, source)

        destination = destination if destination else os.getcwd()
        source, destination = os.path.normpath(source), os.path.normpath(destination)
        if os.path.isfile(source):
            shutil.copy(source, destination)
        else:
            if os.path.isfile(destination):
                raise AttributeError('source is folder while destination is a file: {} vs {}'
                                     .format(source, destination))

            if os.path.isdir(destination):
                folder_name = os.path.basename(source)
                destination = os.path.join(destination, folder_name)

            shutil.copytree(source, destination, copy_function=shutil.copy)

        return destination

    def to_drive(self, source, destination=''):
        """Copy from virtual machine to Google drive subfolder

        # Arguments
            source [str]: filepath
            destination [str]: the relative path to sub folder

        # Returns
            [str]: the copy destination
        """
        if destination and destination[0] == '/':
            destination = destination[1:]

        destination = os.path.join(self._sub_folder, destination)
        source, destination = os.path.normpath(source), os.path.normpath(destination)

        if os.path.isfile(source):
            shutil.copy(source, destination)
        else:
            if os.path.isfile(destination):
                raise AttributeError('source is folder while destination is a file: {} vs {}'
                                     .format(source, destination))

            if os.path.isdir(destination):
                folder_name = os.path.basename(source)
                destination = os.path.join(destination, folder_name)

            shutil.copytree(source, destination, copy_function=shutil.copy)

        return destination


def upload_file():
    """Default prompt to upload files

    # Returns
        A map of the form {<filename>: <file contents>} for all uploaded files
    """

    print('Can select multiple files')
    uploaded = files.upload()

    for each_file in uploaded.keys():
        print('User uploaded file "{name}" with length {length} bytes'.format(
            name=each_file, length=len(uploaded[each_file])))

    return uploaded


def download_file(file_path):
    """Download file

    # Arguments
        file_path [str]: the path to file to be downloaded
    """
    files.download(file_path)


def zip_folder(folder_path, save_to_tmp=False):
    """Zip the folder

    # Arguments
        folder_path [str]: the folder to zip
        save_to_tmp [bool]: whether the zip file will be saved to temp folder

    # Returns
        [str]: the path to zipped file
    """
    target_folder = '/tmp' if save_to_tmp else '/content'

    # get associating names
    folder_path = os.path.normpath(folder_path)
    folder_parent = os.path.dirname(folder_path)
    if not folder_parent:
        folder_parent = '.'
    folder_name = os.path.basename(folder_path)

    # zip the folder to /tmp or /content
    archive_name = '{}_{}'.format(folder_name, arrow.now().format('YYYYMMDDHHmmss'))
    target_file = os.path.join(target_folder, archive_name)
    shutil.make_archive(target_file, 'zip', folder_parent, folder_name)

    return target_file + '.zip'
