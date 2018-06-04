def rm_file(path):   
    """Removes a file from the file system.

    Args:
        path (str): the absolute path of the file to be removed

    Returns:
        True on success
    """

    import os
    from traceback import print_exc

    if os.path.isfile(path):
        try:
            os.remove(path)
            return True
        except:
            print_exc()

    return False

