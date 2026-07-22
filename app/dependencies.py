from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository

def get_product_service():
    return ProductService(
        product_repository=get_product_repository(),
        brand_repository=get_brand_repository(),
        category_repository=get_category_repository(),
    )

def get_product_repository():
    return ProductRepository()

def get_brand_repository():
    return BrandRepository()

def get_category_repository():
    return CategoryRepository()