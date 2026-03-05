The motivation for this repository is that it was extremely hard to find a preprocessed ModelNet10/40 dataset as most of the links available online were broken. 

This repo contributes to further research using multi-view/multi-camera ModelNet.

# Step-by-step

1. Download the dataset from: https://modelnet.cs.princeton.edu/
   1. Specifically, I did: `curl -L -O http://3dvision.princeton.edu/projects/2014/3DShapeNets/ModelNet10.zip`
   1. Then unzip: `unzip ModelNet10.zip`
   1. Delete tehe __MACOSX.
2. Run modelnet_2D_gen.py to generate 2D views: `python modelnet_2D_gen.py`

My structure ended as: 

./ 
    ./ModenNet10 
        ./bathtub
            ./test
            ./train
                bathtub_0001.off
                bathtub_0002.off
                ...
        ...
        ./bookshelf
    ./ModelNet10_views
    ./modelnet40_2Dgen.py
    
