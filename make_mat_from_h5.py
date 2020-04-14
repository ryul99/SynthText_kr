"""
make mat file from h5 format file
data format: http://www.robots.ox.ac.uk/~vgg/data/scenetext/readme.txt
data is loaded from h5 data-bases
"""
from __future__ import division
import os
import os.path as osp
import numpy as np
from scipy import io

import h5py 
from common import *
import itertools

def main(db_fname):
    global wordBB
    global charBB
    db = h5py.File(db_fname, 'r')
    dsets = sorted(db['data'].keys())
    print("total number of images : ", colorize(Color.RED, len(dsets), highlight=True))

    # arrays for matlab format output
    out_imnames = np.array([[None for _ in range(len(dsets))]]) # numpy: 1 x num_image
    out_txt = np.array([[None for _ in range(len(dsets))]]) # numpy: 1 x num_image
    out_wordBB = np.array([[None for _ in range(len(dsets))]]) # numpy: 1 x num_image
    out_charBB = np.array([[None for _ in range(len(dsets))]]) # numpy: 1 x num_image

    for idx, k in enumerate(dsets):
        rgb = db['data'][k][...]
        charBB = db['data'][k].attrs['charBB']
        wordBB = db['data'][k].attrs['wordBB']
        txt = db['data'][k].attrs['txt']
        
        print("image name        : ", colorize(Color.RED, k, bold=True))
        print("  ** no. of chars : ", colorize(Color.YELLOW, charBB.shape[-1]))
        print("  ** no. of words : ", colorize(Color.YELLOW, wordBB.shape[-1]))
        print("  ** text         : ", colorize(Color.GREEN, txt))

        out_imnames[0][idx] = k[:-2]
        out_txt[0][idx] = txt.tolist()
        out_charBB[0][idx] = charBB
        out_wordBB[0][idx] = wordBB
    db.close()
    return out_imnames, out_txt, out_charBB, out_wordBB

if __name__=='__main__':
    print('Loading Data...')
    out_imnames, out_txt, out_charBB, out_wordBB = main('gen/dset_kr.h5')
    print("Saving Data...")
    io.savemat('result.mat', mdict={'imnames': out_imnames, 'charBB': out_charBB, 'wordBB': out_wordBB, 'txt': out_txt})
    print('Data saved')
