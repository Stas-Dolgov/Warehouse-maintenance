from app.models import Supplier, Material, UnitOfMeasurement, StorageUnit, db


def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Приложение для склада" in resp.data.decode("utf-8")


def test_add_supplier_form_post(app, client):
    data = {
        "supplier_code": "SUP100",
        "supplier_name": "ООО Пост-тест",
        "tin": "1234567890",
        "legal_postal_code": "101000",
        "legal_city": "Москва",
        "legal_street": "Тестовая",
        "legal_house": "1",
        "bank_account_number": "40802810000000000001",
        "bank_postal_code": "101000",
        "bank_city": "Москва",
        "bank_street": "Банковская",
        "bank_house": "2",
        "submit": True,
    }
    resp = client.post("/add_supplier", data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert "Поставщик успешно добавлен" in resp.data.decode("utf-8")

    with app.app_context():
        supplier = Supplier.query.filter_by(supplier_code="SUP100").first()
        assert supplier is not None


def test_add_material_and_unit(app, client):
    m_data = {
        "material_code": "MAT500",
        "material_class_code": "C500",
        "material_group_code": "G500",
        "material_name": "Материал для теста",
        "submit": True,
    }
    resp_m = client.post("/add_material", data=m_data, follow_redirects=True)
    assert resp_m.status_code == 200
    assert "Материал успешно добавлен" in resp_m.data.decode("utf-8")

    u_data = {"unit_name": "шт", "submit": True}
    resp_u = client.post("/add_unit", data=u_data, follow_redirects=True)
    assert resp_u.status_code == 200
    assert "Единица измерения добавлена" in resp_u.data.decode("utf-8")

    with app.app_context():
        material = Material.query.filter_by(material_code="MAT500").first()
        unit = UnitOfMeasurement.query.filter_by(unit_name="шт").first()
        assert material is not None
        assert unit is not None


def test_add_storage_unit(app, client):
    with app.app_context():
        supplier = Supplier(
            supplier_code="SUP200",
            supplier_name="Поставщик для склада",
            tin="2222222222",
        )
        material = Material(
            material_code="MAT200",
            material_class_code="C200",
            material_group_code="G200",
            material_name="Материал 200",
        )
        unit = UnitOfMeasurement(unit_name="кг")

        db.session.add_all([supplier, material, unit])
        db.session.commit()

        supplier_id = supplier.id
        material_id = material.id
        unit_id = unit.id

    form_data = {
        "supplier": supplier_id,
        "material": material_id,
        "unit": unit_id,
        "order_number": "ORD-200",
        "balance_account": "BA200",
        "accompanying_document_code": "DOC200",
        "accompanying_document_number": "DOCNUM200",
        "material_account": "MA200",
        "quantity_received": 15.5,
        "unit_price": 200.0,
        "submit": True,
    }

    resp = client.post("/add_storage_unit", data=form_data, follow_redirects=True)
    assert resp.status_code == 200
    assert "Новая складская единица успешно добавлена" in resp.data.decode("utf-8")

    with app.app_context():
        su = StorageUnit.query.filter_by(order_number="ORD-200").first()
        assert su is not None
        assert su.quantity_received == 15.5
        assert su.unit_price == 200.0

