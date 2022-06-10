"""contains different typedefs"""
from enum import Enum


class MailType(Enum):
    """ENUM for all mail types"""
    MASS_MAIL = 0
    PERSONALIZED_MAIL = 1
    TEMPLATE_MAIL = 2
