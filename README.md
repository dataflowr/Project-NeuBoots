# NeuBoots

This repository contains an official implementation of the [Neural Bootstrapper](https://papers.nips.cc/paper/2021/hash/8abfe8ac9ec214d68541fcb888c0b4c3-Abstract.html).

## Prerequsites

- python==3.7
- pytorch==1.2
- torchvision
- tqdm
- PIL

## Configuration script

Before running `main.py`, please make an `ini` script file under the `script` folder for configurations. 
<!-- For detail config, refer to `script/example.ini`. -->
Example of `ini_file`:

```ini
[default]

dataset = cifar100
output_dir = outs
num_epoch = 200
dist = False
phase = train
cpus = 4
gpus = '2'
model = resnet34
is_nbs = True
num_classes = 100
lr = 0.1
weight_decay = 0.0005
optim = sgd
batch_size = 128
n_a = 400
num_bs = 100
dropout_rate = 0.
scheduler = cosine
epoch_th = 30
```

## Run
#### CIFAR-10
```sh
➜ python main.py cutout/cifar10
```
#### CIFAR-100
```sh
➜ python main.py cutout/cifar100
```
#### SVHN
```sh
➜ python main.py cutout/svhn
```

## Citation
```
@inproceedings{neuboots2021,
  title={Neural Bootstrapper},
  author={Shin, Minsuk and Cho, Hyungjoo and Min, Hyun-seok and Lim, Sungbin},
  booktitle={Thirty-Fifth Conference on Neural Information Processing Systems},
  year={2021}
}
```
