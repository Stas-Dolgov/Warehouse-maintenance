from app import create_app, db
from app.models import Supplier, Material, UnitOfMeasurement, StorageUnit

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Supplier': Supplier,
        'Material': Material,
        'UnitOfMeasurement': UnitOfMeasurement,
        'StorageUnit': StorageUnit
    }