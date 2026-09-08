import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
PIN_MEMORY = DEVICE == "cuda"

LEARNING_RATE=0.01
WEIGHT_DECAY=1e-4

EPOCHS=5