from src.utilitiesaccounting.schemas.category_dto import CategoryDTO
from src.utilitiesaccounting.schemas.provider_dto import ProviderDTO


class ProviderCategoryDTO(ProviderDTO):
    category: 'CategoryDTO'
