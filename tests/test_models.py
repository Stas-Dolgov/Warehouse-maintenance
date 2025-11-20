from app.models import Supplier, Material, UnitOfMeasurement, db


def test_supplier_to_dict(app):
    with app.app_context():
        supplier = Supplier(
            supplier_code="SUP10",
            supplier_name="Тестовый поставщик",
            tin="2222222222",
            legal_city="Москва",
        )
        db.session.add(supplier)
        db.session.commit()

        data = supplier.to_dict()
        assert data["supplier_code"] == "SUP10"
        assert data["supplier_name"] == "Тестовый поставщик"
        assert data["tin"] == "2222222222"
        assert data["bank_city"] is None


def test_material_to_dict_and_repr(app):
    with app.app_context():
        material = Material(
            material_code="MATX",
            material_class_code="C",
            material_group_code="G",
            material_name="Тестовый материал",
        )
        db.session.add(material)
        db.session.commit()

        data = material.to_dict()
        assert data["material_code"] == "MATX"
        assert data["material_name"] == "Тестовый материал"
        assert "Тестовый материал" in repr(material)


def test_unit_of_measurement_unique(app):
    with app.app_context():
        u1 = UnitOfMeasurement(unit_name="литр")
        db.session.add(u1)
        db.session.commit()

        u2 = UnitOfMeasurement(unit_name="литр")
        db.session.add(u2)

        caught = False
        try:
            db.session.commit()
        except Exception:
            caught = True
            db.session.rollback()

        assert caught is True

