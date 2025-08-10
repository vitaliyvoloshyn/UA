from src.utilitiesaccounting_v4.schemas.category_dto import CategoryDTO
from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderDTO


class ProviderCategoryDTO(ProviderDTO):
    category: 'CategoryDTO'
