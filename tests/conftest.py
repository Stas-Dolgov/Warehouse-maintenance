import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app, db
from app.models import Supplier, Material, UnitOfMeasurement, StorageUnit
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture()
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_data(app):
    s1 = Supplier(
        supplier_code="SUP1",
        supplier_name="Поставщик 1",
        tin="1234567890",
        bank_postal_code="101000",
        bank_city="Москва",
        bank_street="Тверская",
        bank_house="1",
    )
    s2 = Supplier(
        supplier_code="SUP2",
        supplier_name="Поставщик 2",
        tin="0987654321",
        bank_postal_code="101000",
        bank_city="Москва",
        bank_street="Тверская",
        bank_house="1",
    )
    s3 = Supplier(
        supplier_code="SUP3",
        supplier_name="Поставщик 3",
        tin="1111111111",
        bank_postal_code="190000",
        bank_city="Санкт-Петербург",
        bank_street="Невский",
        bank_house="10",
    )

    m1 = Material(
        material_code="MAT1",
        material_class_code="C1",
        material_group_code="G1",
        material_name="Материал 1",
    )
    m2 = Material(
        material_code="MAT2",
        material_class_code="C1",
        material_group_code="G2",
        material_name="Материал 2",
    )

    u_kg = UnitOfMeasurement(unit_name="кг")

    db.session.add_all([s1, s2, s3, m1, m2, u_kg])
    db.session.commit()

    su1 = StorageUnit(
        order_number="ORD-1",
        balance_account="BA1",
        material_account="MA1",
        quantity_received=10.0,
        unit_price=100.0,
        supplier_id=s1.id,
        material_id=m1.id,
        unit_id=u_kg.id,
    )
    su2 = StorageUnit(
        order_number="ORD-2",
        balance_account="BA1",
        material_account="MA1",
        quantity_received=5.0,
        unit_price=120.0,
        supplier_id=s2.id,
        material_id=m1.id,
        unit_id=u_kg.id,
    )
    su3 = StorageUnit(
        order_number="ORD-3",
        balance_account="BA2",
        material_account="MA2",
        quantity_received=7.0,
        unit_price=90.0,
        supplier_id=s3.id,
        material_id=m2.id,
        unit_id=u_kg.id,
    )

    db.session.add_all([su1, su2, su3])
    db.session.commit()

    return {
        "suppliers": (s1, s2, s3),
        "materials": (m1, m2),
        "unit": u_kg,
        "storage_units": (su1, su2, su3),
    }

