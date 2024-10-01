from enum import Enum

class RestyleStatus(Enum):
    NOT_STARTED = 0
    ACTIVE = 1
    FINISHED = 2

restyling_status_msg_map = {
    RestyleStatus.NOT_STARTED.value: ('Restyle Not Started Yet', '#e4f2c7'),
    RestyleStatus.ACTIVE.value: ('Restyling in Progress - Please Wait', '#f268a4'),
    RestyleStatus.FINISHED.value: ('Restyling Finished', '#50f258'),
}

THRESHOLD_PARAM = 11
BLUR_KERNEL_SIZE = 5

CONTENT_LAYERS = ['block5_conv2']

STYLE_LAYERS = [
                'block1_conv1',
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1'
                ]

TOTAL_VARIATION_WEIGHT = 30
STYLE_WEIGHT = 1e-2
CONTENT_WEIGHT = 1e4

MAX_IMG_DIM = 512
MAX_ITER_NO = 21
STEPS_PER_EPOCH = 10

SEG_DEF_HEIGHT, SEG_DEF_WIDTH = 128, 128
SEG_DEFAULT_MODEL = 'UNet_model.h5'
SEG_DEFAULT_MODEL_DIR = 'UNet_model'
