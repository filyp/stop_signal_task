import os
from psychopy import visual
from pygame import mixer
import codecs
from os.path import join
import yaml


def load_config():
    with open(join("docs", "config.yaml")) as yaml_file:
        doc = yaml.load(yaml_file)
    return doc


def load_data(win, folder_name):
    """
    ladowanie zdjec i dzwiekow
    :param win: visual.Window z psychopy
    :param folder_name: nazwa folderu z ktorego beda ladowane pliki
    """
    mixer.init()

    names = [f for f in os.listdir(folder_name)]
    data = list()
    for name in names:
        try:
            mixer.music.load(os.path.join(folder_name, name))
            data.append(('sound', name.split('.')[0], mixer.music))
        except:
            try:
                image = visual.ImageStim(win, image=os.path.join(folder_name, name),
                                         interpolate=True)
                data.append(('image', name.split('.')[0], image))
            except:
                raise Exception('Error while loading a file ' + name)
    return data


def read_text_from_file(file_name, insert=''):
    """
    Method that read message from text file, and optionally add some
    dynamically generated info.
    :param file_name: Name of file to read
    :param insert: dynamically generated info
    :return: message
    """
    if not isinstance(file_name, str):
        raise TypeError('file_name must be a string')
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)
