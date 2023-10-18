from typing import Optional, Protocol, List

from credit_ratings.models import CreditRating, CreditRatingQueryParams


class ICreditRatingService(Protocol):
    def get_credit_ratings_list(
        self, query_params: Optional[CreditRatingQueryParams]
    ) -> List[CreditRating]:
        ...

    def get_credit_rating_by_id(self, id: str) -> CreditRating:
        ...
