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
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy as np



class Model_WeightLoss(object):
    def __init__(self, model, centers, quan_phase=0, loss_weight=0.1, use_cuda=True):
        super(Model_WeightLoss, self).__init__()
        self.model = model
        self.multi_layer = ['Sequential', 'BasicBlock', 'Bottleneck']
        self.centers = centers
        self.quan_phase = quan_phase
        self.loss_weight = loss_weight
        self.use_cuda = use_cuda
        self.model_criterion = []
        self.cen_dict_list = []
        self.arg_sort = []
        self.convert2dict()
        self.center_out = []
        self.b_shrink = []
        self.b_stop = []
        self.counter = 0
        self.stack = 0
        self.weight_loss_decay = 1
    
    def Traverse_layer(self, block, in_list = None, in_func = None, **kwargs):

        deep_in = self.multi_layer
        for i in block:
            if type(i).__name__ in deep_in:
                self.Traverse_layer(i.children(), in_list, in_func, **kwargs)
                if type(i).__name__ == 'Bottleneck':
                    self.stack += 1

            else:
                if type(i).__name__ not in ['BatchNorm2d', 'ReLU', 'MaxPool2d', 'AvgPool2d', 'Dropout']:
                    if Part_WeightLoss.__name__ == 'Part_WeightLoss':
                        
                        if len(kwargs) > 2:
                            in_list.append(in_func(i, kwargs['center'][self.counter],
                                                 kwargs['b_shrink'][self.counter],
                                                 loss_weight=kwargs['loss_weight']*(self.weight_loss_decay
                                                 **self.stack)).cuda())
                        else:
                            in_func(i, kwargs['cen_dict'][self.counter],len(self.centers[0])
                        self.counter += 1
    def convert2dict(self):
        if self.cen_dict_list != []:
            self.cen_dict_list = []
        for ind,i in enumerate(self.centers):
            ori_dict = dict()
            mid = [(i[x]+i[x+1])/2 for x in range(len(i)-1)]
            for ind_j, j in enumerate(i):
                ori_dict[ind_j]=[j,[mid[ind_j-1] if ind_j!=0 else None, mid[ind_j] if ind_j!=(len(i)-1) else None]]
            self.cen_dict_list.append(ori_dict)

    def init_model_criterion(self): 
        if self.model_criterion != []:
            print('criterion exist')
            return 0
        ind = 0
        self.counter = 0
        self.Traverse_layer(self.model.children(), deep_in = self.multi_layer, 
                            in_list = self.model_criterion, 
                            in_func = Part_WeightLoss,
                            center = self.center_out, b_shrink = self.b_shrink, loss_weight = self.loss_weight
                           )
        self.counter = 0
    
    def compute_boundary(self):
        center_out = []
        b_shrink = []
        b_stop = []
        for ind,i in enumerate(self.centers):
            layer_cen_abs = [-abs(x) for x in self.centers[ind]]
            arg_sort = np.argsort(layer_cen_abs)
            b_shrink.append(self.cen_dict_list[ind][int(arg_sort[self.quan_phase])][1])
            this_cen = self.cen_dict_list[ind][int(arg_sort[self.quan_phase])][0]
            center_out.append(this_cen)
            if self.quan_phase>0:
                min_bound = -1000
                max_bound = 1000
                for j in range(self.quan_phase):
                    temp_cen = self.cen_dict_list[ind][int(arg_sort[j])][0]
                    temp_bon = self.cen_dict_list[ind][int(arg_sort[j])][1]
                    if temp_cen <0:
                        if temp_bon[1] > min_bound:
                            min_bound = temp_bon[1]
                    else:
                        if temp_bon[0] < max_bound:
                            max_bound = temp_bon[0]
                if min_bound == -1000:
                    min_bound = None
                if max_bound == 1000:
                    max_bound = None
                b_stop.append([min_bound, max_bound])
            else:
                b_stop.append([None, None])
            self.center_out = center_out
            self.b_shrink = b_shrink
            self.b_stop = b_stop
        
        return center_out, b_shrink, b_stop
    
    def update_phase(self, new_phase=None, cluster = False):
        ind = 0
        if new_phase is not None:
            if self.quan_phase == new_phase:
                print('Dont need to update phase')
                return 0
            else:
                self.quan_phase = new_phase
        else:
            self.quan_phase = self.quan_phase + 1
        if cluster:
            self.cluster()
        self.compute_boundary()
        
        for i in self.model_criterion:
            i.update_phase(self.center_out[ind], self.b_shrink[ind], b_stop=self.b_stop[ind])
            ind += 1
        
        return [self.center_out, self.b_shrink, self.b_stop]
    
    def forward(self):
        loss = 0
        for i in self.model_criterion:
            loss += i.forward()
        return loss
    
    def shrink(self, thresh_in=0):
        for i in self.model_criterion:
            i.shrink(thresh_per = thresh_in)

    def phase_shrink(self):
        for i in self.model_criterion:
            i.phase_shrink()

    def freeze(self):
        for i in self.model_criterion:
            i.freeze()
    
    def constrain(self):
        for i in self.model_criterion:
            i.constrain()
    
    def update_center(self):
        for ind, i in enumerate(self.model_criterion):
            uped = i.update_center()
            layer_cen_abs = [-abs(x) for x in self.centers[ind]]
            arg_sort = np.argsort(layer_cen_abs)
            self.cen_dict_list[ind][int(arg_sort[self.quan_phase])][0] = uped
            self.centers[ind][int(arg_sort[self.quan_phase])] = uped
            self.center_out[ind] = uped



    def cluster(self):
        model_c_e = []
        ind = 0
        for i in model.children():
            if (type(i).__name__) == 'Sequential':
                for j in i.children():
                    if (type(j).__name__) in ['Conv2d', 'Linear']:
                        layer_cen_abs = [-abs(x) for x in self.centers[ind]]
                        arg_sort = np.argsort(layer_cen_abs)
                        clf = KMeans(n_clusters=len(self.centers[ind])-self.quan_phase)
                        w_np = j.weight.data.cpu().numpy().reshape(-1, 1)
                        w_np_cluster = w_np[(w_np>(self.b_stop[ind][0] if self.b_stop[ind][0] is not None else -1000))&
                                            (w_np<(self.b_stop[ind][1] if self.b_stop[ind][1] is not None else 1000))]
                        w_s = w_np_cluster[np.random.choice(w_np_cluster.shape[0], size=96*100 if w_np_cluster.size > 96*100 else w_np_cluster.size,
                                                            replace=False)].reshape(-1, 1)
                        s = clf.fit(w_s)
                        out = []
                        for k in range(self.quan_phase):
                            out.append(self.centers[ind][int(arg_sort[k])])
                                       
                        for k in range(clf.cluster_centers_.size):
                            out.append(float(clf.cluster_centers_[k]))
                            out.sort()
                            
                        model_c_e.append(out)
                        ind += 1
        self.centers = model_c_e
        self.convert2dict()
        self.compute_boundary()
        return model_c_e

    def last_prune(self, layer, layer_list, centers = 16):
        cens = [i for i,_ in layer_list.values()]
        arg_sort = np.argsort(-np.abs(np.array(cens)))
        for i in arg_sort[:centers]:
            cen = layer_list[i][0]
            min_v = layer_list[i][1][0]
            max_v = layer_list[i][1][1]
            if min_v is None:
                layer.weight.data[layer.weight.data < max_v] = cen
            elif max_v is None:
                layer.weight.data[layer.weight.data > min_v] = cen
            else:
                layer.weight.data[(layer.weight.data > min_v)&(layer.weight.data < max_v)] = cen

class Part_WeightLoss(nn.Module):
    def __init__(self, layer, centers_in, b_shrink, b_stop=[None, None], loss_weight=1.0, use_cuda=True, cen_up_r=0.9):
        super(Part_WeightLoss, self).__init__()
        self.centers_in = centers_in
        self.b_stop = b_stop
        self.b_shrink = b_shrink
        self.layer = layer
        self.loss_weight = loss_weight
        self.use_cuda = use_cuda
        self.cen_up_r = cen_up_r
        if b_stop is not None:
            if len(self.b_stop)==1:
                if self.b_stop < 0:
                    self.m_stop = layer.weight.data<self.b_stop
                else:
                    self.m_stop = layer.weight.data>self.b_stop
            elif len(self.b_stop)==2:
                if (self.b_stop[0] is None) & (self.b_stop[1] is None):
                    self.m_stop = (layer.weight.data>1000)&(layer.weight.data<-1000)
                elif self.b_stop[0] is None:
                    self.m_stop = layer.weight.data>self.b_stop[1]
                elif self.b_stop[1] is None:
                    self.m_stop = layer.weight.data<self.b_stop[0]
                else:
                    self.m_stop = (layer.weight.data>self.b_stop[1])&(layer.weight.data<self.b_stop[0])
            else:
                raise "b_stop error"
        if len(self.b_shrink)==1:
            if self.b_shrink[0] < 0:
                self.m_shrink = layer.weight<self.b_shrink[0]
            else:
                self.m_shrink = layer.weight>self.b_shrink[0]
        elif len(self.b_shrink)==2:
            if (self.b_shrink[0] is None) & (self.b_shrink[1] is None):
                self.m_shrink = (layer.weight>-1000)&(layer.weight<1000)
            elif self.b_shrink[0] is None:
                self.m_shrink = layer.weight<self.b_shrink[1]
            elif self.b_shrink[1] is None:
                self.m_shrink = layer.weight>self.b_shrink[0]
            else:                
                self.m_shrink = (layer.weight>self.b_shrink[0])&(layer.weight<self.b_shrink[1])
        else:
            raise "b_shrink error"
        
        if self.b_shrink[0] == self.b_stop[0]:
            self.b_retrain = [self.b_shrink[1], self.b_stop[1]]
        elif self.b_shrink[0] == self.b_stop[1]:
            raise 'error0'
        elif self.b_shrink[1] == self.b_stop[1]:
            self.b_retrain = [self.b_stop[0], self.b_shrink[0]]
        elif self.b_shrink[1] == self.b_stop[0]:
            raise 'error1'
        else:
            raise 'error2'

        if (self.b_retrain[0] is None) & (self.b_retrain[1] is None):
            self.m_retrain = (layer.weight.data>-1000)&(layer.weight.data<1000)
        elif self.b_retrain[0] is None:
            self.m_retrain = layer.weight.data<self.b_retrain[1]
        elif self.b_retrain[1] is None:
            self.m_retrain = layer.weight.data>self.b_retrain[0]
        else:                
            self.m_retrain = (layer.weight.data>self.b_retrain[0])&(layer.weight.data<self.b_retrain[1])

        
        

    def forward(self):
        layer = self.layer
        diff = self.centers_in - torch.masked_select(layer.weight, self.m_shrink)
        loss = self.loss_weight * torch.abs(diff).sum()
        return loss
    
    def shrink(self, thresh_per=0):
        layer = self.layer
        if self.b_shrink[0] is None:
            weight_min = torch.min(layer.weight.data)
            dis_min = abs(self.centers_in - weight_min)
            dis_max = abs(self.centers_in - self.b_shrink[1])
        elif self.b_shrink[1] is None:
            weight_max = torch.max(layer.weight.data)
            dis_max = abs(self.centers_in - weight_max)
            dis_min = abs(self.centers_in - self.b_shrink[0])
        elif (self.b_shrink[0] is None) & (self.b_shrink[1] is None):
            pass
        else:
            dis_max = abs(self.centers_in - self.b_shrink[1])
            dis_min = abs(self.centers_in - self.b_shrink[0])
        thresh_min = self.centers_in - dis_min*thresh_per
        thresh_max = self.centers_in + dis_max*thresh_per
        if self.b_shrink is not None:
            to_prune = (layer.weight.data > thresh_min) & (layer.weight.data < thresh_max)
            layer.weight.data[to_prune] = self.centers_in
            shrink_freeze = layer.weight.data==self.centers_in
            layer.weight.grad[shrink_freeze] = 0
    
    def phase_shrink(self):
        self.layer.weight.data[self.m_shrink.data] = self.centers_in
    
    def freeze(self):
        layer = self.layer
        if self.b_stop is not None:
            layer.weight.grad[self.m_stop.detach()] = 0
    def constrain(self):
        layer = self.layer
        if self.b_retrain[0] is None:
            layer.weight.data[self.m_retrain].clamp_(max = self.b_retrain[1])
        elif self.b_retrain[1] is None:
            layer.weight.data[self.m_retrain].clamp_(min = self.b_retrain[0])
        else:
            layer.weight.data[self.m_retrain].clamp_(min = self.b_retrain[0], max = self.b_retrain[1])

    def update_center(self):
        to_cluster = torch.masked_select(self.layer.weight, self.m_shrink).data.cpu().numpy()
        clf = KMeans(n_clusters=1)
        w_np = to_cluster.reshape(-1, 1)
        w_s = w_np[np.random.choice(w_np.shape[0], size=4096*500 if w_np.size > 4096*500 else w_np.size, replace=False),:]#w_np[np.random.randint(w_np.size, size=round(w_np.size/100)), :]
        s = clf.fit(w_s)
        self.centers_in = float(self.centers_in * self.cen_up_r + clf.cluster_centers_[0][0] * (1 - self.cen_up_r))
        return self.centers_in


    def update_phase(self, centers_in, b_shrink, b_stop=None):
        layer = self.layer
        self.centers_in = centers_in
        self.b_shrink = b_shrink
        self.b_stop = b_stop
        if self.b_stop is not None:
            if len(self.b_stop)==1:
                if self.b_stop < 0:
                    self.m_stop = layer.weight.data<self.b_stop
                else:
                    self.m_stop = layer.weight.data>self.b_stop
            elif len(self.b_stop)==2:
                if (self.b_stop[0] is None) & (self.b_stop[1] is None):
                    self.m_stop = (layer.weight.data>1000)&(layer.weight.data<-1000)
                elif self.b_stop[0] is None:
                    self.m_stop = layer.weight.data>self.b_stop[1]
                elif self.b_stop[1] is None:
                    self.m_stop = layer.weight.data<self.b_stop[0]
                else:
                    self.m_stop = (layer.weight.data>b_stop[1])|(layer.weight.data<b_stop[0])
                
            else:
                raise "b_stop error"
        
        if len(self.b_shrink)==1:
            if self.b_shrink[0] < 0:
                self.m_shrink = layer.weight<self.b_shrink[0]
            else:
                self.m_shrink = layer.weight>self.b_shrink[0]
        elif len(self.b_shrink)==2:
            if (self.b_shrink[0] is None) & (self.b_shrink[1] is None):
                self.m_shrink = (layer.weight>-1000)&(layer.weight<1000)
            elif self.b_shrink[0] is None:
                self.m_shrink = layer.weight<self.b_shrink[1]
            elif self.b_shrink[1] is None:
                self.m_shrink = layer.weight>self.b_shrink[0]
            else:                
                self.m_shrink = (layer.weight>self.b_shrink[0])&(layer.weight<self.b_shrink[1])
        else:
            raise "b_shrink error"
        if self.b_shrink[0] == self.b_stop[0]:
            self.b_retrain = [self.b_shrink[1], self.b_stop[1]]
        elif self.b_shrink[0] == self.b_stop[1]:
            raise 'error0'
        elif self.b_shrink[1] == self.b_stop[1]:
            self.b_retrain = [self.b_stop[0], self.b_shrink[0]]
        elif self.b_shrink[1] == self.b_stop[0]:
            raise 'error1'
        else:
            raise 'error2'

        if (self.b_retrain[0] is None) & (self.b_retrain[1] is None):
            self.m_retrain = (layer.weight.data>-1000)&(layer.weight.data<1000)
        elif self.b_retrain[0] is None:
            self.m_retrain = layer.weight.data<self.b_retrain[1]
        elif self.b_retrain[1] is None:
            self.m_retrain = layer.weight.data>self.b_retrain[0]
        else:                
            self.m_retrain = (layer.weight.data>self.b_retrain[0])&(layer.weight.data<self.b_retrain[1])
    
    def cuda(self, device_id=None):
        self.use_cuda = True
        return self._apply(lambda t: t.cuda(device_id))