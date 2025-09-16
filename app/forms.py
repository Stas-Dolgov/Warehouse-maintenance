from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length


class SupplierForm(FlaskForm):
    supplier_code = StringField('Код поставщика', validators=[DataRequired(), Length(max=64)])
    supplier_name = StringField('Наименование поставщика', validators=[DataRequired(), Length(max=128)])
    tin = StringField('ИНН', validators=[DataRequired(), Length(min=10, max=12)])

    legal_postal_code = StringField('Юр. адрес: Индекс', validators=[Length(max=10)])
    legal_city = StringField('Юр. адрес: Город', validators=[Length(max=128)])
    legal_street = StringField('Юр. адрес: Улица', validators=[Length(max=256)])
    legal_house = StringField('Юр. адрес: Дом', validators=[Length(max=32)])

    bank_account_number = StringField('Номер банковского счета', validators=[Length(max=64)])
    bank_postal_code = StringField('Адрес банка: Индекс', validators=[Length(max=10)])
    bank_city = StringField('Адрес банка: Город', validators=[Length(max=128)])
    bank_street = StringField('Адрес банка: Улица', validators=[Length(max=256)])
    bank_house = StringField('Адрес банка: Дом', validators=[Length(max=32)])

    submit = SubmitField('Сохранить')


class MaterialForm(FlaskForm):
    material_code = StringField('Код материала', validators=[DataRequired(), Length(max=64)])
    material_class_code = StringField('Код класса материала', validators=[DataRequired(), Length(max=64)])
    material_group_code = StringField('Код группы материала', validators=[DataRequired(), Length(max=64)])
    material_name = StringField('Наименование материала', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Сохранить')


class UnitOfMeasurementForm(FlaskForm):
    unit_name = StringField('Наименование единицы (кг, м, шт)', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Сохранить')


class StorageUnitForm(FlaskForm):
    # Выпадающие списки для выбора связей
    # coerce=int говорит полю, что значение, которое придет из формы, нужно преобразовать в число
    supplier = SelectField('Поставщик', coerce=int, validators=[DataRequired()])
    material = SelectField('Материал', coerce=int, validators=[DataRequired()])
    unit = SelectField('Единица измерения', coerce=int, validators=[DataRequired()])
    
    # Обычные текстовые и числовые поля
    order_number = StringField('Номер заказа', validators=[DataRequired(), Length(max=128)])
    balance_account = StringField('Балансовый счет', validators=[DataRequired(), Length(max=64)])
    accompanying_document_code = StringField('Код сопроводительного документа', validators=[Length(max=64)])
    accompanying_document_number = StringField('Номер сопроводительного документа', validators=[Length(max=128)])
    material_account = StringField('Счет материала', validators=[DataRequired(), Length(max=64)])
    quantity_received = FloatField('Количество получено', validators=[DataRequired()])
    unit_price = FloatField('Цена за единицу', validators=[DataRequired()])
    
    submit = SubmitField('Сохранить')