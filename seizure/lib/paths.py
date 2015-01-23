import os


def generate_path(video):
    """
    Generate a path in which to save the video.

    Saves as '{}_{TIME}.flv'
    :param video:
    :return:
    """
    raise NotImplementedError()


def rename_extension(path, extension):
    head = os.path.splitext(path)[0]
    # os.path.

    raise NotImplementedError()
    return 'foo.mp4'
