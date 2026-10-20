def test_complete_api_smoke_flow(client):
    group_response = client.post(
        "/api/groups",
        json={"name": "Mostar Trip"},
    )

    assert group_response.status_code == 201
    group_id = group_response.json()["id"]

    member_ids = {}

    for name in ["Faris", "Ada", "Amar"]:
        response = client.post(
            f"/api/groups/{group_id}/members",
            json={"name": name},
        )

        assert response.status_code == 201
        member_ids[name] = response.json()["id"]

    expense_response = client.post(
        f"/api/groups/{group_id}/expenses",
        json={
            "payer_member_id": member_ids["Faris"],
            "description": "Apartment",
            "amount": "100.00",
        },
    )

    assert expense_response.status_code == 201

    balances_response = client.get(
        f"/api/groups/{group_id}/balances"
    )

    assert balances_response.status_code == 200

    balances = {
        item["member_name"]: item["balance_cents"]
        for item in balances_response.json()
    }

    assert balances == {
        "Faris": 6666,
        "Ada": -3333,
        "Amar": -3333,
    }

    settlements_response = client.get(
        f"/api/groups/{group_id}/settlements"
    )

    assert settlements_response.status_code == 200

    settlements = settlements_response.json()

    assert len(settlements) == 2
    assert sum(
        item["amount_cents"]
        for item in settlements
    ) == 6666