import os
from psychopy import visual
import pyglet
import codecs
from os.path import join
import yaml

possible_images_format = ('bmp', 'jpg', 'png')
possible_audio_format = ('mp3')


def load_config():
    with open(join("docs", "config.yaml")) as yaml_file:
        doc = yaml.load(yaml_file)
    return doc


def load_data(win, folder_name):
    """
    ladowanie tekstu, zdjec i dzwiekow
    :param win: visual.Window z psychopy
    :param folder_name: nazwa folderu z ktorego beda ladowane pliki
    """

    names = [f for f in os.listdir(folder_name)]
    data = list()
    for name in names:
        path = os.path.join(folder_name, name)
        try:
            if name[-3:] == 'txt':
                with open(path, 'r') as text_file:
                    for line in text_file:
                        trigger_name = line.split(':')[0]
                        text = line.split(':')[1]
                        text = text.split('\n')[0]
                        data.append(('text', trigger_name, text))
            elif name[-3:] in possible_images_format:
                image = visual.ImageStim(win, image=path, interpolate=True)
                data.append(('image', name.split('.')[0], image))
            elif name[-3:] in possible_audio_format:
                music = pyglet.resource.media(os.path.join(folder_name, name))
                data.append(('sound', name.split('.')[0], music))
            else:
                raise Exception('Error while loading a file ' + name)
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