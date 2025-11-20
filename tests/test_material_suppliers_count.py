from app import models


def test_material_supplier_count(sample_data, app):
    m1, m2 = sample_data["materials"]

    with app.app_context():
        count_m1 = (
            m1.storage_units.with_entities(models.StorageUnit.supplier_id)
            .distinct()
            .count()
        )
        count_m2 = (
            m2.storage_units.with_entities(models.StorageUnit.supplier_id)
            .distinct()
            .count()
        )

        assert count_m1 == 2
        assert count_m2 == 1

