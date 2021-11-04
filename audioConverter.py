import logging
import os
import soundfile
from pydub import AudioSegment, effects


def main():
    root_path = "D:\\code\\raspiKeys\\src\\res\\backtracks\\processed_wav\\latin"
    out_path = "D:\\code\\raspiKeys\\src\\res\\backtracks\\out_wav"

    for filename in os.listdir(root_path):
        # filename_full = os.path.join(root_path, filename)
        try:
            tmp_file = normalizeAudio(root_path, filename, out_path)
            out_file = os.path.join(out_path, filename)
            convertToWav16PCM(tmp_file, out_file)
            print("File {} converted with success".format(filename))
            os.remove(tmp_file)
        except Exception as e:
            logging.exception(e)


def normalizeAudio(input_dir: str, input_file: str, output_dir):
    filename_full = os.path.join(input_dir, input_file)
    raw_sound = AudioSegment.from_file(filename_full, "wav")
    normalized_sound = effects.normalize(raw_sound)
    out_file = "tmp-" + input_file
    temp_filename = os.path.join(output_dir, out_file)
    normalized_sound.export(temp_filename, format='wav')
    return temp_filename


def convertToWav16PCM(input_file: str, output_file):
    data, sampleRate = soundfile.read(input_file)
    soundfile.write(output_file, data, sampleRate, subtype="PCM_16")


if __name__ == "__main__":
    main()
