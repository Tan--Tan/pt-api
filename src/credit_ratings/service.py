from typing import List, Optional

from fastapi import HTTPException
from credit_ratings.provider import CreditRatingsProvider
from credit_ratings.interfaces import ICreditRatingService
from credit_ratings.models import (
    CreditRatingFilters,
    CreditRatingQueryParams,
    CreditRating,
    CreditRatingStatus,
    CreditRatingsItemtApiResponse,
    CreditRatingsListApiResponse,
    CreditRatingsResponse,
)
from credit_ratings.utils import country_code_to_name, country_name_to_code


class CreditRatingService(ICreditRatingService):
    def __init__(self, provider=CreditRatingsProvider()):
        # Initialize CreditRatingService with a default provider
        self.provider = provider

    def get_credit_ratings_list(
        self, query_params: Optional[CreditRatingQueryParams]
    ) -> CreditRatingsListApiResponse:
        # Set default limit and offset if not provided in query_params
        limit = query_params.limit if query_params else 5
        offset = query_params.offset if query_params else 0

        # Map query parameters to filters
        filters: Optional[CreditRatingFilters] = self._map_query_to_filters(
            query_params
        )

        # Retrieve credit ratings data from the provider
        result: List[CreditRatingsResponse] = self.provider.get_credit_ratings(
            filters, limit, offset
        )

        # Map the result to API response
        return CreditRatingsListApiResponse(
            data=map(self._map_to_api_response, result), limit=limit, offset=offset
        )

    def get_credit_rating_by_id(self, id: str) -> CreditRatingsItemtApiResponse:
        # Retrieve a specific credit rating by ID
        result: CreditRatingsResponse = self.provider.get_credit_rating_item(id=id)
        
        # Raise HTTPException if the result is not found
        if result is None:
            raise HTTPException(status_code=404, detail="Not found")
        
        # Map the result to API response
        return CreditRatingsItemtApiResponse(data=self._map_to_api_response(result))

    @staticmethod
    def _map_query_to_filters(
        query_params: Optional[CreditRatingQueryParams],
    ) -> Optional[CreditRatingFilters]:
        if query_params is None:
            return None

        result: CreditRatingFilters = CreditRatingFilters(
            status=[
                CreditRatingStatus.REGISTERED,
                CreditRatingStatus.UNDER_DEVELOPMENT,
                CreditRatingStatus.TRANSFERRED_FROM_GHG,
            ]
        )
        if query_params.country_code is not None and len(query_params.country_code) > 0:
            result.country = map(country_code_to_name, query_params.country_code)

        if (
            query_params.registry_name is not None
            and len(query_params.registry_name) > 0
        ):
            result.registry_name = query_params.registry_name

        return result

    @staticmethod
    def _map_to_api_response(input: CreditRatingsResponse) -> CreditRating:
        return CreditRating(
            id=input.id,
            sylvera_id=input.sylvera_id,
            url=input.url,
            status=input.status,
            country_code=country_name_to_code(input.country),
            locations=input.locations,
            ngeo_eligible=input.ngeo_eligible,
            vintages=input.vintages,
            registry=input.registry,
            accreditations=input.accreditations,
        )
