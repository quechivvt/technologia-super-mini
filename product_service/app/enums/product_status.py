from enum import Enum


class ProductStatus(str, Enum):
    COMING_SOON = "COMING_SOON"
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    DISCONTINUED = "DISCONTINUED"
    