import os
import torch
from PIL import Image
from typing import Tuple
from torch.utils.data  import Dataset, DataLoader
import albumentations as A
from transformers import AutoTokenizer

import config as cfg


class CLIPDataset(Dataset):
    def __init__(self, images, captions , tokenizer ,transform: A.Compose = None, mode :str="train"):
        self.transform = self._get_transform(mode)
        self.images_path = images
        self.captions =list(captions)

        self.encoded_captions=tokenizer(
            self.captions,
            padding=True,
            truncation=True,
            max_length=cfg.max_length,
            return_tensors="pt"
        )
        
    

    @staticmethod
    def _get_transform(mode) : 
        if mode == "train":
            return A.Compose([
                A.Resize(cfg.size, cfg.size),
                A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        else:
            return A.Compose([
                A.Resize(cfg.size, cfg.size),
                A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])

    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, str]:
        image = self.images_path[idx]
        caption = self.captions[idx]
        image = Image.open(os.path.join(self.images_path, image))
        if self.transform:
            image = self.transform(image)
        return image, caption