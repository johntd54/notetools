"""View media content inside Google Colab notebook"""

import os
import shutil
import subprocess

from IPython.core.magics.display import HTML

from notetools.colab.constants import PUBLIC_BASE_DIR, PUBLIC_BASE_URL


def transfer_file_to_public_dir(file_path):
    """Transfer file from a private folder to a public folder and keeps the
    file-folder structure

    # Arguments
        file_path [str]: the path to file

    # Returns
        [str]: the destination file path (relative to public base dir)
    """
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    if file_dir in ['', '/', '.']:
        file_dir = ''

    target_dir = os.path.join(PUBLIC_BASE_DIR, file_dir)
    os.makedirs(target_dir, exist_ok=True)

    shutil.copy(file_path, target_dir)
    relative_url = os.path.join(file_dir, file_name)

    return relative_url


def view_image(file_path):
    """View the image file

    # Arguments
        file_path [str]: the path to file

    # Returns
        [HTML Image]: the image prompt pointing to correct file
    """
    relative_url = transfer_file_to_public_dir(file_path)
    url = os.path.join(PUBLIC_BASE_URL, relative_url)

    return HTML('<img src="{}">'.format(url))


def view_video(file_path):
    """View the video file

    # Arguments
        file_path [str]: the path to file

    # Returns
        [HTML Video]: the video prompt pointing to correct file
    """
    relative_url = transfer_file_to_public_dir(file_path)

    # convert to mp4 transferable file
    path, ext = os.path.splitext(relative_url)
    if ext != '.mp4':
        relative_url = path + '.mp4'
        subprocess.run([
            'ffmpeg', '-loglevel', 'error', '-i',
            file_path, os.path.join(PUBLIC_BASE_DIR, relative_url)])

    url = os.path.join(PUBLIC_BASE_URL, relative_url)
    return HTML(
        """
        <video width="640" height="480" controls>
            <source src="{}" type="video/mp4">
        </video>
        """.format(url))
