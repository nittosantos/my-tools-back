from datetime import date, timedelta
from decimal import Decimal

import pytest
from model_bakery import baker

from marketplace.models import Rental, Tool


@pytest.mark.django_db
def test_tool_str_representation():
    tool = baker.make(Tool, title="Furadeira X1000")
    assert str(tool) == "Furadeira X1000"


@pytest.mark.django_db
def test_rental_str_representation(user):
    tool = baker.make(Tool, owner=user, title="Serra Circular")
    rental = baker.make(Rental, tool=tool, renter=user)
    assert str(rental) == f"{tool.title} - {user.username}"


@pytest.mark.django_db
def test_rental_total_price_is_decimal(user):
    tool = baker.make(Tool, owner=user, price_per_day=Decimal("15.50"))
    start = date.today()
    end = start + timedelta(days=2)
    rental = Rental.objects.create(
        tool=tool,
        renter=user,
        start_date=start,
        end_date=end,
        total_price=Decimal("46.50"),
    )
    assert isinstance(rental.total_price, Decimal)

