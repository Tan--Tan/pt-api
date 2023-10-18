from typing import Optional
from fastapi import APIRouter, Depends
from credit_ratings.service import CreditRatingService
from credit_ratings.interfaces import ICreditRatingService
from credit_ratings.models import CreditRatingQueryParams

router = APIRouter()


# Dependency function to get an instance of CreditRatingService
def get_service():
    return CreditRatingService()


"""
    Endpoint to retrieve a list of credit ratings based on the specified parameters.

    Parameters:
    - input: Optional[CreditRatingQueryParams] - Query parameters for filtering credit ratings.
    - service: ICreditRatingService - Dependency injection for the credit rating service.

    Returns:
    - List of credit ratings based on the provided input parameters.
"""


@router.post("", tags=["credit-ratings"])
async def post_get_credit_rating_list(
    input: Optional[CreditRatingQueryParams] = None,
    service: ICreditRatingService = Depends(get_service),
):
    return service.get_credit_ratings_list(input)


"""
    Endpoint to retrieve a specific credit rating by its ID.

    Parameters:
    - id: str - The unique identifier of the credit rating.
    - service: ICreditRatingService - Dependency injection for the credit rating service.

    Returns:
    - The credit rating corresponding to the provided ID.
"""


@router.get("/{id}", tags=["credit-ratings"])
async def get_credit_rating_by_id(
    id: str, service: ICreditRatingService = Depends(get_service)
):
    return service.get_credit_rating_by_id(id)
