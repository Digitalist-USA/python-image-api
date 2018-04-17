"""
Inception V3 trained on ImageNet
Mostly taken from:
https://tensorflow.org/tutorials/image_recognition/
"""

import os.path
import re
import sys
import tarfile
import logging

from six.moves import urllib
# pylint: disable=import-error
import numpy as np
import tensorflow as tf

from . import config as cfg

LOGGER = logging.getLogger(__name__)


class NodeLookup(object):
    """Converts integer node ID's to human readable labels."""

    def __init__(self,
                 label_lookup_path=None,
                 uid_lookup_path=None):
        if not label_lookup_path:
            label_lookup_path = os.path.join(
                cfg.MODELS_DIR, 'imagenet_2012_challenge_label_map_proto.pbtxt')
        if not uid_lookup_path:
            uid_lookup_path = os.path.join(
                cfg.MODELS_DIR, 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    @staticmethod
    def load(label_lookup_path, uid_lookup_path):
        """Loads a human readable English name for each softmax node.
        Args:
          label_lookup_path: string UID to integer node ID.
          uid_lookup_path: string UID to human-readable string.
        Returns:
          dict from integer node ID to human-readable string.
        """
        # pylint: disable=too-many-locals
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        parser = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = parser.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        """
        convert id to string
        Args:
            node_id:

        Returns:

        """
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


class InceptionV3(object):
    """
    Inception V3 class
    """
    def __init__(self):
        self.model_dir = cfg.MODELS_DIR
        self.data_url = cfg.INCEPTION_V3_DOWNLOAD_URL
        self.maybe_download_and_extract()
        # self.graph_def = self.create_graph(self.model_dir)

    @staticmethod
    def create_graph(model_dir):
        """Creates a graph from saved GraphDef file and returns a saver."""
        # Creates graph from saved graph_def.pb.
        with tf.gfile.FastGFile(os.path.join(model_dir, 'classify_image_graph_def.pb'), 'rb') \
                as _file:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(_file.read())
            _ = tf.import_graph_def(graph_def, name='')
        return graph_def

    def predict(self, image_file, num_top_predictions=10):
        """Runs inference on an image.
        Args:
          image_file: Image file name.
          num_top_predictions: top N predictions returned
        Returns:
          Nothing
        """
        if not tf.gfile.Exists(image_file):
            tf.logging.fatal('File does not exist %s', image_file)
        image_data = tf.gfile.FastGFile(image_file, 'rb').read()

        # Creates graph from saved GraphDef.
        self.create_graph(self.model_dir)

        with tf.Session() as sess:
            # Some useful tensors:
            # 'softmax:0': A tensor containing the normalized prediction across
            #   1000 labels.
            # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
            #   float description of the image.
            # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
            #   encoding of the image.
            # Runs the softmax tensor by feeding the image_data as input to the graph.
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            # Creates node ID --> English string lookup.
            node_lookup = NodeLookup()
            results = []
            top_k = predictions.argsort()[-num_top_predictions:][::-1]
            for node_id in top_k:
                human_string = node_lookup.id_to_string(node_id)
                score = predictions[node_id]
                prediction = {
                    'class': str(human_string),
                    'score': str(score.squeeze())
                }
                results.append(prediction)
            return results

    def maybe_download_and_extract(self):
        """Download and extract model tar file."""
        dest_directory = self.model_dir
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)
        filename = self.data_url.split('/')[-1]
        filepath = os.path.join(dest_directory, filename)
        if not os.path.exists(filepath):
            LOGGER.info('CNN model does not exist. Downloading...')

            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                    filename, float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()

            filepath, _ = urllib.request.urlretrieve(self.data_url, filepath, _progress)
            statinfo = os.stat(filepath)
            LOGGER.info(f'\nSuccessfully downloaded {filename} {statinfo.st_size} bytes.')
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)
