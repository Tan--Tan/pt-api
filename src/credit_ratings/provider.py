import json
import math
from typing import Any, List, Optional
import pandas as pd

from credit_ratings.models import (
    Coords,
    CreditRatingFilters,
    CreditRatingStatus,
    CreditRatingsResponse,
    Registry,
    Source,
    Vintage,
    Accreditation,
)


class CreditRatingsProvider:
    data: pd.DataFrame

    def __init__(self, data_csv="data/verra_projects_sample.csv"):
        # Initialize the CreditRatingsProvider with data from a CSV file
        self.data = pd.read_csv(data_csv)

        # Map string values in the "STATUS" column to CreditRatingStatus enums
        self.data["STATUS"] = self.data["STATUS"].map(CreditRatingStatus)

        # Parse JSON strings in specific columns to Python objects
        self.data["LOCATIONS"] = self.data["LOCATIONS"].apply(lambda x: json.loads(x))
        self.data["SOURCE"] = self.data["SOURCE"].apply(lambda x: json.loads(x))
        self.data["REGISTRY_OBJECT"] = self.data["REGISTRY_OBJECT"].apply(
            lambda x: json.loads(x)
        )

    def get_credit_ratings(
        self, filters: Optional[CreditRatingFilters], limit: int, offset: int
    ) -> List[CreditRatingsResponse]:
        # Copy the original DataFrame to avoid modifying the original data
        result = self.data.copy(deep=True)

        # Apply filters if provided
        if filters is not None:
            if filters.country:
                result = result.loc[result["COUNTRY"].isin(filters.country)]
            if filters.registry_name:
                result = result.loc[
                    result["REGISTRY_OBJECT"].apply(
                        lambda x: x.get("name", "") in filters.registry_name
                    )
                ]
            if filters.status:
                result = result.loc[result["STATUS"].isin(filters.status)]

        # Extract a subset of the DataFrame based on limit and offset  
        data_dict_list = result[offset : offset + limit].to_dict(orient="records")
        
        # Map the subset to CreditRatingsResponse objects
        return [self._map_response_to_model(item) for item in data_dict_list]

    def get_credit_rating_item(self, id: str) -> CreditRatingsResponse | None:
        # Extract the record with the specified ID
        result = self.data[self.data["ID"] == id].to_dict(orient="records")
        
        # Map the record to a CreditRatingsResponse object
        return self._map_response_to_model(result[0])

    def _map_response_to_model(self, input: Any) -> CreditRatingsResponse:
        return CreditRatingsResponse(
            id=input["ID"],
            sylvera_id=input["SYLVERA_ID"],
            url=input["URL"],
            status=input["STATUS"],
            locations=self._get_locations(input["LOCATIONS"]),
            country=input["COUNTRY"],
            source=self._get_source(input["SOURCE"]),
            registry=self._get_registry(input["REGISTRY_OBJECT"]),
            ngeo_eligible=input["IS_NGEO_ELIGIBLE"],
            vintages=self._get_vintage(input["VINTAGES"]),
            accreditations=self._get_accreditation(input["ACCREDITATIONS"]),
        )

    @staticmethod
    def _get_locations(input: str) -> List[Coords]:
        return (
            Coords(latitude=item["latitude"], longitude=item["longitude"])
            for item in input
        )

    @staticmethod
    def _get_source(input: str) -> Optional[Source]:
        if input is None:
            return None

        return Source(
            id=input["id"] if input.get("id") else 0,
            name=input["name"] if input.get("name") else "",
            area_ha=input["area_ha"] if input.get("area_ha") else 0,
            est_annual_emissions_redct_tco2=input["est_annual_emissions_redct_tco2"]
            if input.get("est_annual_emissions_redct_tco2")
            else 0,
            methodologies=input["methodologies"] if input.get("methodologies") else [],
        )

    @staticmethod
    def _get_registry(input: str) -> Registry:
        return Registry(
            berkeley_abbrev=input["berkeley_abbrev"]
            if input.get("berkeley_abbrev")
            else "",
            name=input["name"] if input.get("name") else "",
        )

    @staticmethod
    def _get_vintage(input: str) -> Optional[List[Vintage]]:
        if input is None or (type(input) != str and math.isnan(input)):
            return None

        items = json.loads(input)
        return (
            Vintage(permitted_total=item["permitted_total"], year=item["year"])
            for item in items
        )

    @staticmethod
    def _get_accreditation(input: str) -> Optional[List[Accreditation]]:
        if input is None or (type(input) != str and math.isnan(input)):
            return None

        items = json.loads(input)
        return (
            Accreditation(
                abbreviation=item["abbreviation"] if input.get("abbreviation") else "",
                accredited=item["accredited"] if input.get("full_name") else False,
                full_name=item["full_name"] if input.get("full_name") else "",
            )
            for item in items
        )
