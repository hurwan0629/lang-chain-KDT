from torchvision import datasets
from torchvision.transforms import transforms
from torch.utils.data import DataLoader

data = datasets.MNIST(
  root="data",
  download=False,
  train=True,
  transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
  ])
)

loader = DataLoader(
  data,
  batch_size=32,
  shuffle=False,
)

import matplotlib.pyplot as plt
from torchvision.utils import make_grid

# images, _ = next(iter(loader))

# img = make_grid(images, nrow=8, padding=2)

# plt.imshow(img.permute(1, 2, 0), cmap="gray")
# plt.axis("on")
# plt.show()

