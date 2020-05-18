from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
from torchvision.datasets import MNIST, CIFAR10, CIFAR100, SVHN

from math import ceil
from sklearn.model_selection import StratifiedShuffleSplit

from data.block_sampler import BlockSampler, BlockSubsetSampler
from utils.preprocessing import transform_train, transform_test


def _get_split_indices(trainset, p, seed):
    train_targets = [label for img, label in trainset]
    splitter = StratifiedShuffleSplit(1, test_size=0.2, random_state=0)
    indices = range(len(trainset))
    return next(splitter.split(indices, train_targets))


class GbsDataLoader(object):
    def __init__(self, dataset, batch_size, n_a, sub_size, cpus, seed=0):
        self.dataset = self._get_dataset(dataset)
        self.split_indices = _get_split_indices(self.dataset['train'],
                                                0.2, seed)
        self.p = self.dataset['train'][0][0].nelement()
        self.sub_size = sub_size
        self.n_a = n_a
        self.n_train = len(self.split_indices[0])
        self.n_val = len(self.split_indices[1])
        self.n_test = len(self.dataset['test'])
        self.n_b = self.n_train // n_a
        self.batch_size = batch_size
        self.cpus = cpus

    def load(self, phase):
        _f = {'train': lambda: self._train(),
              'val': lambda: self._val(),
              'test': lambda: self._test()}
        try:  # lambda for lazy evaluation
            loader = _f[phase]()
            return loader
        except:
            raise ValueError('Dataset should be one of [train, val, test]')

    def _train(self):
        self.len = ceil(self.n_train / self.batch_size)
        sampler = SubsetRandomSampler(self.split_indices[0])
        loader = DataLoader(self.dataset['train'], batch_size=self.batch_size,
                            sampler=sampler, num_workers=self.cpus,
                            pin_memory=True)
        return loader

    def _val(self):
        sampler = SubsetRandomSampler(self.split_indices[1])
        loader = DataLoader(self.dataset['train'], batch_size=self.batch_size,
                            sampler=sampler, num_workers=self.cpus,
                            pin_memory=True)
        return loader

    def _test(self):
        loader = DataLoader(self.dataset['test'], batch_size=self.batch_size,
                            num_workers=self.cpus, pin_memory=True)
        return loader

    def _get_dataset(self, dataset):
        _d = {'cifar10': lambda: self._load_cifar10(),
              'cifar100': lambda: self._load_cifar100(),
              'mnist': lambda: self._load_mnist(),
              'svhn': lambda: self._load_svhn(),
              'svhn_extra': lambda: self._load_svhn(use_extra=True)}
        try:
            _dataset = _d[dataset]()
            return _dataset
        except:
            raise ValueError(
                'Dataset should be one of [mnist, cifar10, cifar100, svhn]'
                )

    def _load_mnist(self):
        trainset = MNIST(root='.mnist', train=True, download=True,
                         transform=transforms.ToTensor())
        testset = MNIST(root='.mnist', train=False, download=True,
                        transform=transforms.ToTensor())
        return {'train': trainset, 'test': testset}

    def _load_cifar10(self):
        trainset = CIFAR10(root='.cifar10', train=True, download=True,
                           transform=transform_train)
        testset = CIFAR10(root='.cifar10', train=False, download=True,
                          transform=transform_test)
        return {'train': trainset, 'test': testset}

    def _load_cifar100(self):
        trainset = CIFAR100(root='.cifar100', train=True, download=True,
                            transform=transform_train)
        testset = CIFAR100(root='.cifar100', train=False, download=True,
                           transform=transform_test)
        return {'train': trainset, 'test': testset}

    def _load_svhn(self, use_extra=False):
        trainset = SVHN(root='.svhn', split='train', download=True,
                        transform=transform_train)
        extraset = SVHN(root='.svhn', split='extra', download=True,
                        transform=transform_train)
        testset = SVHN(root='.svhn', split='test', download=True,
                       transform=transform_test)
        if use_extra:
            return {'train': trainset + extraset, 'test': testset}
        else:
            return {'train': trainset, 'test': testset}
