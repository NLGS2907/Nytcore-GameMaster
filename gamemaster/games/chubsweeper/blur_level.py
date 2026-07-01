from enum import IntEnum


class BlurLevel(IntEnum):
    """Level of blur obfuscation to use for images.
    
    The values are specifically the radius to use in a Gaussian Blur algorithm.
    """

    MILD = 30
    MEDIUM = 50
    STRONG = 100
    VERY_STRONG = 250

    # Not really blur anymore
    NONE = 0
    OPAQUE = -1
