import torch
import torchvision.transforms as transforms
import torch.utils.data as data
import os
import pickle
import numpy as np
import nltk
from PIL import Image
from build_vocab import Vocabulary
import pdb
import pandas as pd
from pycocotools.coco import COCO


class CocoDataset(data.Dataset):
    """COCO Custom Dataset compatible with torch.utils.data.DataLoader."""

    def __init__(self, root, json, vocab, transform=None):
        """Set the path for images, captions and vocabulary wrapper.

        Args:
            root: image directory.
            json: coco annotation file path.
            vocab: vocabulary wrapper.
            transform: image transformer.
        """
        self.root = root
        self.coco = COCO(json)
        self.ids = list(self.coco.anns.keys())
        self.vocab = vocab
        self.transform = transform

    def __getitem__(self, index):
        """Returns one data pair (image and caption)."""
        coco = self.coco
        vocab = self.vocab
        ann_id = self.ids[index]
        caption = coco.anns[ann_id]['caption']
        img_id = coco.anns[ann_id]['image_id']
        path = coco.loadImgs(img_id)[0]['file_name']

        image = Image.open(os.path.join(self.root, path)).convert('RGB')
        if self.transform is not None:
            image = self.transform(image)

        # Convert caption (string) to word ids.
        tokens = nltk.tokenize.word_tokenize(str(caption).lower())
        caption = []
        caption.append(vocab('<start>'))
        caption.extend([vocab(token) for token in tokens])
        caption.append(vocab('<end>'))
        target = torch.Tensor(caption)

        wrong_prob = [1 / (len(self.ids) - 1) if i != index else 0 for i in range(len(self.ids))]
        wrong_index = np.random.choice(range(len(self.ids)), 1, wrong_prob)[0]
        ann_id = self.ids[wrong_index]
        wrong_caption = coco.anns[ann_id]['caption']

        tokens = nltk.tokenize.word_tokenize(str(wrong_caption).lower())
        wrong_caption = []
        wrong_caption.append(vocab('<start>'))
        wrong_caption.extend([vocab(token) for token in tokens])
        wrong_caption.append(vocab('<end>'))
        wrong_target = torch.Tensor(wrong_caption)

        return image, target, wrong_target

    def __len__(self):
        return len(self.ids)


def collate_fn(data):
    """Creates mini-batch tensors from the list of tuples (image, caption).
    
    We should build custom collate_fn rather than using default collate_fn, 
    because merging caption (including padding) is not supported in default.

    Args:
        data: list of tuple (image, caption). 
            - image: torch tensor of shape (3, 256, 256).
            - caption: torch tensor of shape (?); variable length.

    Returns:
        images: torch tensor of shape (batch_size, 3, 256, 256).
        targets: torch tensor of shape (batch_size, padded_length).
        lengths: list; valid length for each padded caption.
    """
    # Sort a data list by caption length (descending order).
    data.sort(key=lambda x: len(x[1]), reverse=True)
    images, captions, wrong_captions = zip(*data)

    wrong_captions = list(wrong_captions)
    wrong_captions.sort(key=lambda x: len(x), reverse=True)

    # Merge images (from tuple of 3D tensor to 4D tensor).
    images = torch.stack(images, 0)

    # Merge captions (from tuple of 1D tensor to 2D tensor).
    lengths = [len(cap) for cap in captions]
    targets = torch.zeros(len(captions), max(lengths)).long()
    for i, cap in enumerate(captions):
        end = lengths[i]
        targets[i, :end] = cap[:end]

    # Getting wrong targets(captions)
    wrong_lengths = [len(cap) for cap in wrong_captions]
    wrong_targets = torch.zeros(len(wrong_captions), max(wrong_lengths)).long()
    for i, cap in enumerate(wrong_captions):
        end = wrong_lengths[i]
        wrong_targets[i, :end] = cap[:end]
    
    return images, targets, lengths, wrong_targets, wrong_lengths


def get_loader(root, captionpath, vocab, transform, batch_size, shuffle, num_workers):
    """Returns torch.utils.data.DataLoader for custom coco dataset."""
    # CUB caption dataset
    cub = CocoDataset(root=root,
                       json=captionpath,
                       vocab=vocab,
                       transform=transform)
    
    # Data loader for CUB dataset
    # This will return (images, captions, lengths) for every iteration.
    # images: tensor of shape (batch_size, 3, 224, 224).
    # captions: tensor of shape (batch_size, padded_length).
    # lengths: list indicating valid length for each caption. length is (batch_size).
    data_loader = torch.utils.data.DataLoader(dataset=cub, 
                                              batch_size=batch_size,
                                              shuffle=shuffle,
                                              num_workers=num_workers,
                                              collate_fn=collate_fn)
    return data_loader
