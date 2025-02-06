import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from typing import Any
# from resnet import ResNet18
from resnet import ResNet14
from config import *
import torch.multiprocessing as mp  # type: ignore
mp.set_start_method('fork', force=True)

NUM_CLASSES = 10  

# CIFAR-10 데이터셋 로드
transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

train_dataset = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
test_dataset = datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, pin_memory=True, num_workers=4)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, pin_memory=True, num_workers=4)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# resnet 18 선언하기
# model = ResNet18().to(device)
model = ResNet14().to(device)


criterion: nn.CrossEntropyLoss = nn.CrossEntropyLoss()
optimizer: optim.SGD = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=MOMENTUM, weight_decay=WEIGHT_DECAY)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=40, gamma=0.1)

# 학습 
def train(model: nn.Module, loader: DataLoader, criterion: nn.Module, optimizer: optim.Optimizer, device: torch.device) -> None:
    model.train()
    total_loss: float = 0
    correct: int = 0
    total: int = 0

    for batch_idx, (inputs, targets) in enumerate(loader):
        inputs, targets = inputs.to(device), targets.to(device)

        outputs = model(inputs)
        loss = criterion(outputs, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        # 학습 진행 출력 (10% 단위로 출력)
        if (batch_idx + 1) % (len(loader) // 10) == 0:
            print(f"Batch {batch_idx + 1}/{len(loader)} - Loss: {loss.item():.4f}")

    accuracy: float = 100. * correct / total
    print(f"Train Loss: {total_loss / len(loader):.4f}, Accuracy: {accuracy:.2f}%")

# 평가 
def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module, device: torch.device) -> None:
    model.eval()
    total_loss: float = 0
    correct: int = 0
    total: int = 0

    with torch.no_grad():
        for batch_idx, (inputs, targets) in enumerate(loader):
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    accuracy: float = 100. * correct / total
    print(f"Test Loss: {total_loss / len(loader):.4f}, Accuracy: {accuracy:.2f}%")

# 학습 및 평가 루프
for epoch in range(EPOCHS):
    print(f"Epoch {epoch + 1}/{EPOCHS} 시작")
    train(model, train_loader, criterion, optimizer, device)
    evaluate(model, test_loader, criterion, device)
    scheduler.step()

# 모델 저장
torch.save(model.state_dict(), "resnet14_checkpoint.pth")
print(f"Model saved to resnet14_checkpoint.pth")
