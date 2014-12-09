__author__ = 'ckolek'

from enum import Enum


class AudioEncoding(Enum):
    ALAW = 'ALAW'
    PCM_FLOAT = 'PCM_FLOAT'
    PCM_SIGNED = 'PCM_SIGNED'
    PCM_UNSIGNED = 'PCM_UNSIGNED'
    ULAW = 'ULAW'