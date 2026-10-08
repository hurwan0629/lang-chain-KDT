import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


# ============================================================
# 1. Diffusion schedule
# ============================================================
T = 1000

beta = torch.linspace(1e-4, 0.02, T)
alpha = 1.0 - beta
alpha_bar = torch.cumprod(alpha, dim=0)


# ============================================================
# 2. Noise predictor
#    input : noisy image x_t + timestep t
#    output: predicted noise
# ============================================================
class DiffusionModel(nn.Module):
    def __init__(self, timesteps: int = T):
        super().__init__()

        self.time_embed = nn.Embedding(timesteps, 32)

        self.conv1 = nn.Conv2d(1 + 32, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 1, kernel_size=3, padding=1)

    def forward(self, x, t):
        # t: (B,) -> (B, 32)
        time = self.time_embed(t)

        # (B, 32) -> (B, 32, H, W)
        time = time[:, :, None, None]
        time = time.expand(-1, -1, x.shape[2], x.shape[3])

        # noisy image + timestep information
        x = torch.cat([x, time], dim=1)

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))

        # sigmoid 없음: noise 자체를 회귀(regression)
        return self.conv3(x)


# ============================================================
# 3. Forward diffusion
#
# x_t = sqrt(alpha_bar_t) * x_0
#     + sqrt(1 - alpha_bar_t) * epsilon
# ============================================================
def add_noise(x0, t, noise, alpha_bar_device):
    a_bar = alpha_bar_device[t][:, None, None, None]

    xt = (
        torch.sqrt(a_bar) * x0
        + torch.sqrt(1.0 - a_bar) * noise
    )

    return xt


# ============================================================
# 4. Training
# ============================================================
def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # MNIST image range: [-1, 1]
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])

    dataset = datasets.MNIST(
        root="./data",
        train=True,
        download=True,
        transform=transform,
    )

    dataloader = DataLoader(
        dataset,
        batch_size=128,
        shuffle=True,
        num_workers=2,
        pin_memory=torch.cuda.is_available(),
    )

    model = DiffusionModel().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    alpha_bar_device = alpha_bar.to(device)

    epochs = 5

    for epoch in range(epochs):
        model.train()

        for step, (real_images, _) in enumerate(dataloader):
            real_images = real_images.to(device)
            batch_size = real_images.size(0)

            # 1) 이미지마다 랜덤 timestep 선택
            t = torch.randint(
                low=0,
                high=T,
                size=(batch_size,),
                device=device,
            )

            # 2) 정답이 될 Gaussian noise 생성
            noise = torch.randn_like(real_images)

            # 3) 원본 이미지에 해당 timestep만큼 noise 추가
            noisy_images = add_noise(
                real_images,
                t,
                noise,
                alpha_bar_device,
            )

            # 4) 모델이 들어간 noise를 예측
            predicted_noise = model(noisy_images, t)

            # 5) 실제 noise와 예측 noise 비교
            loss = F.mse_loss(predicted_noise, noise)

            # 6) 모델 학습
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if step % 100 == 0:
                print(
                    f"epoch={epoch + 1}/{epochs} "
                    f"step={step:04d} "
                    f"loss={loss.item():.4f}"
                )

    torch.save(model.state_dict(), "diffusion_mnist.pt")
    print("saved: diffusion_mnist.pt")


if __name__ == "__main__":
    train()
