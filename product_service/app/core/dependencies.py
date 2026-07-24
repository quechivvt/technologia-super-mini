from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.cache.product_cache_repository import ProductCacheRepository
from app.cache.cache_repository import CacheRepository
from app.core.redis import redis_client
from app.event.publisher import RedisPublisher
from fastapi import Depends

def get_publisher():
    return RedisPublisher(redis_client)

def get_product_service(publisher = Depends(get_publisher)):
    return ProductService(
        publisher=publisher,
        product_repository=get_product_repository(),
        product_cache_repository=get_product_cache_repository(),
        brand_repository=get_brand_repository(),
        category_repository=get_category_repository(),
    )

def get_product_repository():
    return ProductRepository()

def get_cache():
    return CacheRepository(redis_client)

def get_product_cache_repository():
    return ProductCacheRepository(get_cache())

def get_brand_repository():
    return BrandRepository()

def get_category_repository():
    return CategoryRepository()