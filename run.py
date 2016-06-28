#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import join
import yaml

__author__ = 'ociepkam'


def load_config():
    with open(join("docs", "config.yaml")) as yaml_file:
        doc = yaml.load(yaml_file)
    return doc


def run():
    config = load_config()

