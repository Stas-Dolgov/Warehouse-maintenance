def test_suppliers_for_material_route(client, sample_data):
    m1, m2 = sample_data["materials"]
    s1, s2, s3 = sample_data["suppliers"]

    resp = client.get(f"/material/{m1.id}/suppliers")
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert s1.supplier_name in html
    assert s2.supplier_name in html
    assert s3.supplier_name not in html

    resp2 = client.get(f"/material/{m2.id}/suppliers")
    assert resp2.status_code == 200
    html2 = resp2.data.decode("utf-8")
    assert s3.supplier_name in html2
    assert s1.supplier_name not in html2
    assert s2.supplier_name not in html2



