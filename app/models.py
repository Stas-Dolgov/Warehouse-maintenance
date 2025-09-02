from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
db = SQLAlchemy()


# Поставщики
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_code = db.Column(db.String(64), index=True, unique=True, nullable=False)
    supplier_name = db.Column(db.String(128), nullable=False)
    tin = db.Column(db.String(12), unique=True, nullable=False)  # ИНН

    # Юридический адрес
    legal_postal_code = db.Column(db.String(10))
    legal_city = db.Column(db.String(128))
    legal_street = db.Column(db.String(256))
    legal_house = db.Column(db.String(32))

    # Банковские реквизиты
    bank_account_number = db.Column(db.String(64), nullable=False)
    bank_postal_code = db.Column(db.String(10), nullable=False)
    bank_city = db.Column(db.String(128))
    bank_street = db.Column(db.String(256))
    bank_house = db.Column(db.String(32))

    storage_units = db.relationship('StorageUnit', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return f'<Supplier {self.supplier_name}>'


# Материалы
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_code = db.Column(db.String(64), index=True, unique=True, nullable=False)
    material_class_code = db.Column(db.String(64), nullable=False)
    material_group_code = db.Column(db.String(64), nullable=False)
    material_name = db.Column(db.String(128), nullable=False)

    storage_units = db.relationship('StorageUnit', backref='material', lazy='dynamic')

    def __repr__(self):
        return f'<Material {self.material_name}>'


# Единицы измерения
class UnitOfMeasurement(db.Model):
    __tablename__ = 'unit_of_measurement'

    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(64), unique=True, nullable=False)

    storage_units = db.relationship('StorageUnit', backref='unit', lazy='dynamic')

    def __repr__(self):
        return f'<Unit {self.unit_name}>'


# Единицы хранения
class StorageUnit(db.Model):
    __tablename__ = 'storage_unit'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, index=True, default=lambda: datetime.now(timezone.utc))
    balance_account = db.Column(db.String(64), nullable=False)
    accompanying_document_code = db.Column(db.String(64))
    accompanying_document_number = db.Column(db.String(128))
    material_account = db.Column(db.String(64), nullable=False)
    quantity_received = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    # Внешние ключи
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'), nullable=False)

    def __repr__(self):
        return f'<StorageUnit Order {self.order_number}>'
