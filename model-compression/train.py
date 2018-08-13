# Copyright (c) Peking University 2018
#
# The software is released under the Open-Intelligence Open Source License V1.0.
# The copyright owner promises to follow "Open-Intelligence Open Source Platform
# Management Regulation V1.0", which is provided by The New Generation of 
# Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
import os
import time
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy as np
import tqdm
import json
import math
from tensorboardX import SummaryWriter
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import matplotlib.pyplot as plt
from shrink import Model_WeightLoss, Part_WeightLoss

model = nn.DataParallel(models.__dict__['resnet18'](pretrained=True))
model.cuda()

data_batch_size = 128
train_num = 1281168
batches = math.ceil(train_num/data_batch_size)
interval_epoch = 2
in_epoch = 36

# imagenet train dir
traindir = os.path.join('/home/yzy/2018-work/pytorch-example', 'train')

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

train_dataset = datasets.ImageFolder(
        traindir,
        transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ]))


train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=data_batch_size, shuffle=True,
        num_workers=4, pin_memory=True)

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
        
def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res

def train(train_loader, model, criterion, optimizer, epoch, writer,w_cen_end=None):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    loss_reg = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()
    
    reg_alpha = 0.00001
    model.train()

    end = time.time()
    for i, (input, target) in (enumerate(train_loader)):
        data_time.update(time.time() - end)
        input = input.cuda(async=True)
        target = target.cuda(async=True)
        input_var = torch.tensor(input)
        target_var = torch.tensor(target)

        output = model(input_var)
        loss = criterion[0](output, target_var)
        loss_w_reg = criterion[1].forward()
        loss_all = loss + loss_w_reg

        prec1, prec5 = accuracy(output.data, target, topk=(1, 5))
        losses.update(loss_all.item(), input.size(0))
        loss_reg.update(loss_w_reg.item(), input.size(0))
        top1.update(prec1.item(), input.size(0))
        top5.update(prec5.item(), input.size(0))

        optimizer.zero_grad()
        loss_all.backward()

        criterion[1].shrink(i*(epoch%interval_epoch+1)/batches/interval_epoch if i*(epoch%interval_epoch+1)/batches/interval_epoch<1 else 1)
        criterion[1].freeze()
        optimizer.step()
        criterion[1].constrain()
        batch_time.update(time.time() - end)
        end = time.time()

        if i % 50 == 0:
            # criterion[1].update_center()
            writer.add_scalars('data/Prec', {
                                             "Prec@1": top1.avg,
                                             "Prec@5": top5.avg}, i)
            writer.add_scalars('data/Loss', {
                                             "loss_all":losses.avg,
                                             "loss_w_loss":loss_reg.avg}, i)
        if i % 1000==0:
            print('Epoch: [{0}][{1}/{2}]\t, batch_time: {3}'.format(epoch, i, len(train_loader), batch_time.avg))

# Weight centers
with open('res18_cen16.json', 'r') as f:
    modelinit = json.load(f)
nllloss = nn.CrossEntropyLoss().cuda()
class_wl = Model_WeightLoss(model.module, modelinit, loss_weight =0.1)
class_wl.convert2dict()
class_wl.compute_boundary()
class_wl.init_model_criterion()
criterion = [nllloss, class_wl]
optimizer = torch.optim.RMSprop(model.parameters(), lr= 8e-7, momentum=0.5)
writer = SummaryWriter()
up_hist = []
for i in range(in_epoch):
    train(train_loader, model, criterion, optimizer, i, writer, modelinit)
    torch.save(model.state_dict(), './res18_model_cen16/'+str(i)+'.torch')
    if i%interval_epoch == (interval_epoch-1):
        class_wl.phase_shrink()
        up_hist.append(criterion[1].update_phase())
class_wl.counter = 0
class_wl.Traverse_layer(model.children(), cen_dict = class_wl.cen_dict_list, in_func=class_wl.last_prune)
torch.save(model.state_dict(), './res18_model_cen16/compressed.torch')