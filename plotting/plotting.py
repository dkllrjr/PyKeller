#Created: Sat Aug  3 20:30:50 2019
#By: mach

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import PyKeller.signal_processing.signal_analysis as sa
import numpy as np

def plot_bar(bins,hist):
    
    bins_mid = sa.midpoint(bins)
    plt.bar(bins_mid,hist)
    plt.show()
    
def plot_3_in_1(x,y,xlabel,ylabel,label,xticks_step,file_path,top_adj=1,r_adj=1.05,figsize=(6,6)):
    
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    
    fig, host = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top = top_adj)
    fig.dpi=200
    
    par1 = host.twinx()
    par2 = host.twinx()
    
    par2.spines["right"].set_position(("axes", r_adj))
    make_patch_spines_invisible(par2)
    par2.spines["right"].set_visible(True)
    
    p1, = host.plot(x, y[0], color = "b", label=label[0])
    p2, = par1.plot(x, y[1], color = "r", label=label[1])
    p3, = par2.plot(x, y[2], color = "purple", label=label[2])
    
    host.set_xticks(x[::xticks_step])
    host.set_xticks(x[::int(xticks_step/2)],minor=True)
    host.set_xlim([x[0],x[-1]])
    
    host.set_ylabel(ylabel[0],fontsize=14)
    par1.set_ylabel(ylabel[1],fontsize=14)
    par2.set_ylabel(ylabel[2],fontsize=14)
    host.set_xlabel(xlabel,fontsize=14)
    
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    
    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    
    host.tick_params(axis='x', **tkw)
    
    lines = [p1, p2, p3]
    
    host.legend(lines, [l.get_label() for l in lines],ncol=3,loc='upper center')
    
    plt.tight_layout()
    plt.savefig(file_path)
        
    return

def plot_2_in_1(x,y,xlabel,ylabel,label,xticks_step,file_path,top_adj=1,r_adj=1.05,figsize=(6,6)):
    
    fig, host = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top = top_adj)
    fig.dpi=200
    
    par1 = host.twinx()
    
    p1, = host.plot(x, y[0], color = "b", label=label[0])
    p2, = par1.plot(x, y[1], color = "r", label=label[1])
    
    host.set_xticks(x[::xticks_step],fontsize=12)
    host.set_xticks(x[::int(xticks_step/2)],minor=True)
    host.set_xlim([x[0],x[-1]])
    
    host.set_ylabel(ylabel[0],fontsize=14)
    par1.set_ylabel(ylabel[1],fontsize=14)
    host.set_xlabel(xlabel,fontsize=14)
    
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    
    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw,fontsize=12)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw,fontsize=12)
    
    host.tick_params(axis='x', **tkw)
    
    lines = [p1, p2]
    
    host.legend(lines, [l.get_label() for l in lines],ncol=2,loc='upper center')
    
    plt.tight_layout()
    plt.savefig(file_path)
        
    return

def hist_3d(x,y,bins=25,rangexy=None,save_path=None):
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    h,xe,ye = np.histogram2d(x,y,bins=bins,range=rangexy)
    
    x = sa.midpoint(xe)
    y = sa.midpoint(ye)
    
    xg,yg = np.meshgrid(x,y)
    h = np.flip(np.rot90(h,axes=(1,0)),axis=1)
    
    xp,yp = xg.flatten(),yg.flatten()
    zp = np.zeros_like(xp)
    
    dx = x[1]-x[0]
    dy = y[1]-y[0]
    dz = h.flatten()
    
    min_h = np.min(dz)
    max_h = np.max(dz)
    
    cmap = cm.get_cmap('jet')
    rgb = [cmap((k-min_h)/max_h) for k in dz]
    
    ax.bar3d(xp,yp,zp,dx,dy,dz,color=rgb,zsort='average')
    
    if save_path!=None:
        fig.savefig(save_path)
        
    plt.show()