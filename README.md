# PSD25D
A simple Python script that converts a Photoshop file to a p2d5 package used by the [Disguise](https://www.disguise.one) Designer software and media servers.

## Installation

PSD25D depends on [psd-tools](https://github.com/psd-tools/psd-tools) and [Pillow](https://python-pillow.org/), so install those packages using pip3.

`pip3 install psd-tools Pillow`

Make psd2p5d.py executable (this is optional)

`chmod +x psd2p5d.py`

## Usage

PSD25D takes a single argument which is a Photoshop file containing multiple layers.

`./psd2p5d.py example.psd`

### Assumptions

1. The top most layer in the Photoshop file should be the foreground layer;
1. The bottom layer in the Photoshop file should be the background layer;
1. The bottom layer cannot contain any negative (transparent) space;
1. All layers are of equal width and height;

## Limitations

As this is work in progress, there are quite a few limitations still:

1. Field of view is not calculated automatically;
1. Scale and depth are not calculated correctly;



