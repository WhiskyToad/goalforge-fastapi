from fastapi import Depends, APIRouter, status
from app.utils.auth import get_user_id_from_token
from app.categories.CategorySchema import (
    CreateCategoryInput,
    CategorySchema,
)
from app.schemas.GenericSchema import SuccessMessage
from app.categories.CategoryService import CategoryService


CategoryRouter = APIRouter(prefix="/api/category", tags=["category"])


@CategoryRouter.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CategorySchema,
)
async def create_category(
    category_input: CreateCategoryInput,
    user_id: str = Depends(get_user_id_from_token),
    category_service: CategoryService = Depends(CategoryService),
):
    return await category_service.create_category(category_input, user_id)


@CategoryRouter.delete(
    "/delete/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_category(
    category_id: int,
    user_id: str = Depends(get_user_id_from_token),
    category_service: CategoryService = Depends(CategoryService),
):
    return await category_service.delete_category(category_id, user_id)


@CategoryRouter.patch(
    "/edit/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategorySchema,
)
async def edit_category(
    category_id: int,
    category_input: CreateCategoryInput,
    user_id: str = Depends(get_user_id_from_token),
    category_service: CategoryService = Depends(CategoryService),
):
    return await category_service.edit_category(category_id, category_input, user_id)


@CategoryRouter.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[CategorySchema],
)
async def get_all_categories(
    user_id: str = Depends(get_user_id_from_token),
    category_service: CategoryService = Depends(CategoryService),
):
    return await category_service.get_all_categories(user_id)
