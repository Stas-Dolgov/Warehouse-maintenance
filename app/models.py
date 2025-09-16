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
    bank_account_number = db.Column(db.String(64))
    bank_postal_code = db.Column(db.String(10))
    bank_city = db.Column(db.String(128))
    bank_street = db.Column(db.String(256))
    bank_house = db.Column(db.String(32))

    storage_units = db.relationship('StorageUnit', backref='supplier', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'supplier_code': self.supplier_code,
            'supplier_name': self.supplier_name,
            'tin': self.tin,
            'legal_postal_code': self.legal_postal_code,
            'legal_city': self.legal_city,
            'legal_street': self.legal_street,
            'legal_house': self.legal_house,
            'bank_account_number': self.bank_account_number,
            'bank_postal_code': self.bank_postal_code,
            'bank_city': self.bank_city,
            'bank_street': self.bank_street,
            'bank_house': self.bank_house
        }

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

    def to_dict(self):
        return {
            'id': self.id,
            'material_code': self.material_code,
            'material_class_code': self.material_class_code,
            'material_group_code': self.material_group_code,
            'material_name': self.material_name
        }

    def __repr__(self):
        return f'<Material {self.material_name}>'


# Единицы измерения
class UnitOfMeasurement(db.Model):
    __tablename__ = 'unit_of_measurement'

    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(64), unique=True, nullable=False)

    storage_units = db.relationship('StorageUnit', backref='unit', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'unit_name': self.unit_name
        }
    
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'date': self.date.isoformat() if self.date else None,  # Преобразуем дату в строку
            'balance_account': self.balance_account,
            'accompanying_document_code': self.accompanying_document_code,
            'accompanying_document_number': self.accompanying_document_number,
            'material_account': self.material_account,
            'quantity_received': self.quantity_received,
            'unit_price': self.unit_price,
            'supplier_id': self.supplier_id,
            'material_id': self.material_id,
            'unit_id': self.unit_id
        }
    
    def __repr__(self):
        return f'<StorageUnit Order {self.order_number}>'
