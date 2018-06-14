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

def mp3_to_wav(input_path, filename):
    """Transforms an MP3 file to WAV.

    Args:
        input_path (str): Absolute path to MP3 file to be converted
        filename (str): Desired file name of wav file to be saved

    Returns:
        String with absolute path of saved wav file, or None if unsuccessful
    """

    from pydub import AudioSegment
    from traceback import print_exc
    from flask import current_app as app
    import os

    if input_path is None:
        print("to_wav: input_path is None")
        return None

    if filename is None:
        print("to_wav: filename is None")
        return None

    wav_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        song = AudioSegment.from_mp3(input_path)
    except:
        print_exc()
        print("to_wav: unable to load MP3 file")
        return None

    try:
        song.export(wav_path, format="wav")
    except:
        print_exc()
        print("to_wav: unable to convert MP3 file to WAV")
        return None

    return wav_path

def mp4_to_wav(input_path, filename):
    """Transforms an MP4 file to WAV.

    Args:
        input_path (str): Absolute path to MP3 file to be converted
        filename (str): Desired file name of wav file to be saved

    Returns:
        String with absolute path of saved wav file, or None if unsuccessful
    """

    from pydub import AudioSegment
    from traceback import print_exc
    from flask import current_app as app
    import os

    if input_path is None:
        print("to_wav: input_path is None")
        return None

    if filename is None:
        print("to_wav: filename is None")
        return None

    wav_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        song = AudioSegment.from_file(input_path, "mp4")
    except:
        print_exc()
        print("to_wav: unable to load MP4 file")
        return None

    try:
        song.export(wav_path, format="wav")
    except:
        print_exc()
        print("to_wav: unable to convert MP4 file to WAV")
        return None

    return wav_path