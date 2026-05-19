"""Torch device selection helpers."""

import torch


def get_default_device() -> torch.device:
    """Select the best available local Torch device."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")
