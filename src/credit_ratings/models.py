from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class CreditRatingStatus(str, Enum):
    UNDER_DEVELOPMENT = ("Under development",)
    UNDER_VALIDATION = ("Under validation",)
    REGISTRATION_REQUESTED = "Registration requested"
    REGISTERED = ("Registered",)
    ON_HOLD = ("On Hold",)
    INACTIVE = ("Inactive",)
    REJECTED_ADMIN = ("Rejected by Administrator",)
    WITHDRAWN = ("Withdrawn",)
    RAV_APPROVAL_REQUESTED = ("Registration and verification approval requested",)
    CREDITING_PERIOD_RAV_APPROVAL_REQUESTED = (
        "Crediting Period Renewal and Verification Approval Requested"
    )
    CREDITING_PERIOD_RENEWAL_REQUESTED = ("Crediting Period Renewal Requested",)
    TRANSFERRED_FROM_GHG = ("Units Transferred from Approved GHG Program",)
    UNKNOWN = "Unknown"


class CreditRatingQueryParams(BaseModel):
    country_code: Optional[List[str]] = None
    registry_name: Optional[List[str]] = None
    limit: Optional[int] = 5
    offset: Optional[int] = 0


class Coords(BaseModel):
    latitude: float
    longitude: float


class Source(BaseModel):
    area_ha: float
    est_annual_emissions_redct_tco2: int
    id: int
    methodologies: List[str]
    name: str


class Registry(BaseModel):
    berkeley_abbrev: str
    name: str


class Vintage(BaseModel):
    permitted_total: float
    year: int


class Accreditation(BaseModel):
    abbreviation: str
    accredited: bool
    full_name: str


class CreditRating(BaseModel):
    id: str
    sylvera_id: str
    url: str
    status: CreditRatingStatus
    country_code: str
    locations: List[Coords]
    ngeo_eligible: bool
    vintages: Optional[List[Vintage]]
    registry: Registry
    accreditations: Optional[List[Accreditation]]


class CreditRatingFilters(BaseModel):
    status: Optional[List[CreditRatingStatus]] = None
    country: Optional[List[str]] = None
    registry_name: Optional[List[str]] = None


class CreditRatingsResponse(BaseModel):
    id: str
    sylvera_id: str
    url: str
    country: str
    locations: List[Coords]
    source: Source
    ngeo_eligible: bool
    status: CreditRatingStatus
    vintages: Optional[List[Vintage]]
    registry: Registry
    accreditations: Optional[List[Accreditation]]


class CreditRatingsListApiResponse(BaseModel):
    data: List[CreditRating]
    limit: int
    offset: int


class CreditRatingsItemtApiResponse(BaseModel):
    data: CreditRating
