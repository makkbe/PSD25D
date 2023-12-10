# PSD25D
A simple Python script that converts a Photoshop file to a p2d5 package used by the Disguise Designer software and media servers.

## Installation

PSD25D depends on psd-tools and Pillow, so install those packages using pip.

`pip install pst-tools Pillow`

## Usage

PSD25D takes a single argument which is a Photoshop file containing multiple layers.

`psd2p5d.py example.psd`

### Assumptions

1. The top most layer in the Photoshop file should be the foreground layer;
1. The bottom layer in the Photoshop file should be the background layer;
1. The bottom layer cannot contain any negative (transparent) space;
1. All layers are of equal width and height;



