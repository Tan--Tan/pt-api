import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from credit_ratings.service import CreditRatingService
from credit_ratings.models import (
    CreditRatingQueryParams,
    CreditRatingStatus,
    CreditRatingsListApiResponse,
    CreditRatingsItemtApiResponse,
    CreditRatingsResponse,
)


@pytest.fixture
def mock_provider():
    return Mock()


@pytest.fixture
def credit_rating_service(mock_provider):
    return CreditRatingService(provider=mock_provider)


def test_get_credit_ratings_list(credit_rating_service, mocker):
    # Mock the provider's get_credit_ratings method
    mock_provider_get_credit_ratings = mocker.patch.object(
        credit_rating_service.provider,
        "get_credit_ratings",
        return_value=[mock_credit_rating_response()],
    )

    # Define mock query parameters
    query_params = CreditRatingQueryParams(limit=5, offset=0)

    # Call the service method
    result = credit_rating_service.get_credit_ratings_list(query_params)

    # Assertions
    mock_provider_get_credit_ratings.assert_called_once_with(
        mocker.ANY, query_params.limit, query_params.offset
    )
    assert isinstance(result, CreditRatingsListApiResponse)
    assert len(result.data) == 1  # Assuming we have one mock response

# Helper function to create a mock credit rating response
def mock_credit_rating_response():
    return CreditRatingsResponse(
        id="some_id",
        sylvera_id="some_sylvera_id",
        url="some_url",
        status=CreditRatingStatus.REGISTERED,
        country="United States",
        locations=[{"latitude": -33.55724, "longitude": 23.959725}],
        ngeo_eligible=True,
        vintages=[{"permitted_total": 0, "year": 2021}],
        registry={"berkeley_abbrev": "T", "name": "test"},
        source={
            "area_ha": 0,
            "est_annual_emissions_redct_tco2": 0,
            "id": 1,
            "methodologies": [],
            "name": "test",
        },
        accreditations=[{"abbreviation": "A", "accredited": True, "full_name": "test"}],
    )
