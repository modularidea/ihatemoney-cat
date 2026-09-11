"""Web UI tests for the fork's extras: project categories, payment modes,
repeating bills."""

import datetime
import re

from ihatemoney import models
from ihatemoney.tests.common.ihatemoney_testcase import IhatemoneyTestCase


class TestForkWeb(IhatemoneyTestCase):
    def _project_with_members(self):
        self.post_project("raclette")
        self.client.post("/raclette/members/add", data={"name": "zorglub"})
        self.client.post("/raclette/members/add", data={"name": "jeanne"})
        return [m.id for m in self.get_project("raclette").members]

    def _bill_data(self, member_ids, **extra):
        data = {
            "date": "2011-08-10",
            "what": "fromage",
            "payer": member_ids[0],
            "payed_for": member_ids,
            "bill_type": "Expense",
            "amount": "25",
        }
        data.update(extra)
        return data

    def test_categories_page_and_crud(self):
        member_ids = self._project_with_members()

        resp = self.client.get("/raclette/categories")
        self.assertStatus(200, resp)
        page = resp.data.decode("utf-8")
        assert "Credit card" in page  # seeded payment mode
        assert "Grocery" in page  # built-in global category

        resp = self.client.post(
            "/raclette/categories/add",
            data={"name": "Kids", "icon": "🧸", "color": "#ff8800"},
            follow_redirects=True,
        )
        self.assertStatus(200, resp)
        assert "Kids" in resp.data.decode("utf-8")
        category = models.Category.query.one()
        assert category.project_id == "raclette"

        resp = self.client.get(f"/raclette/categories/{category.id}/edit")
        self.assertStatus(200, resp)
        assert 'value="Kids"' in resp.data.decode("utf-8")
        self.client.post(
            f"/raclette/categories/{category.id}/edit",
            data={"name": "Children", "icon": "🧸", "color": "#ff8800", "order": "2"},
        )
        category = models.Category.query.one()
        assert category.name == "Children"
        assert category.order == 2

        # bill using the project category, a payment mode and a repeat rule
        pm = self.get_project("raclette").payment_modes[0]
        self.client.post(
            "/raclette/add",
            data=self._bill_data(
                member_ids,
                # today: listing the bills would otherwise materialize copies
                date=datetime.date.today().isoformat(),
                categoryid=category.id,
                paymentmodeid=pm.id,
                repeat="m",
                repeatfreq="2",
                repeatuntil="",
            ),
        )
        bill = models.Bill.query.one()
        assert bill.category_id == category.id
        assert bill.payment_mode_id == pm.id
        assert bill.repeat == "m"
        assert bill.repeat_freq == 2
        assert bill.repeat_until is None

        resp = self.client.get("/raclette/")
        page = resp.data.decode("utf-8")
        assert "🧸 Children" in page
        assert pm.icon in page
        assert "Repeating bill" in page

        resp = self.client.get(f"/raclette/edit/{bill.id}")
        page = resp.data.decode("utf-8")
        assert re.search(r'<option[^>]*selected[^>]*value="m"|<option[^>]*value="m"[^>]*selected', page)
        assert re.search(rf'<option[^>]*selected[^>]*value="{category.id}"|<option[^>]*value="{category.id}"[^>]*selected', page)

        # deleting the category detaches it from the bill
        self.client.post(f"/raclette/categories/{category.id}/delete")
        assert models.Category.query.count() == 0
        assert models.Bill.query.one().category_id is None

        # payment modes: add + delete
        resp = self.client.post(
            "/raclette/paymentmodes/add",
            data={"name": "Voucher", "icon": "🎟", "color": "#00ff00"},
            follow_redirects=True,
        )
        assert "Voucher" in resp.data.decode("utf-8")
        self.client.post(f"/raclette/paymentmodes/{pm.id}/delete")
        assert models.Bill.query.one().payment_mode_id is None
        assert models.PaymentMode.query.filter_by(id=pm.id).count() == 0

    def test_invalid_category_rejected(self):
        member_ids = self._project_with_members()
        resp = self.client.post("/raclette/add", data=self._bill_data(member_ids, categoryid="999"))
        self.assertStatus(200, resp)  # form re-rendered with errors
        assert models.Bill.query.count() == 0

    def test_repeating_bills_materialize_on_listing(self):
        member_ids = self._project_with_members()
        start = (datetime.date.today() - datetime.timedelta(days=61)).replace(day=1)
        self.client.post(
            "/raclette/add",
            data=self._bill_data(member_ids, date=start.isoformat(), what="rent", repeat="m"),
        )
        assert models.Bill.query.count() == 1
        resp = self.client.get("/raclette/")
        self.assertStatus(200, resp)
        assert models.Bill.query.count() == 3
        repeating = models.Bill.query.filter(models.Bill.repeat != "n").all()
        assert len(repeating) == 1
        assert repeating[0].date == max(b.date for b in models.Bill.query.all())
