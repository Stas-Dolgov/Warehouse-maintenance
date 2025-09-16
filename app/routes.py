from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.models import db, Supplier, Material, UnitOfMeasurement, StorageUnit
from app.forms import SupplierForm, MaterialForm, UnitOfMeasurementForm, StorageUnitForm
from app import models
from sqlalchemy import func
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/suppliers')
def suppliers():
    all_suppliers = Supplier.query.all()  # Получаем всех поставщиков из БД
    return render_template('suppliers.html', suppliers=all_suppliers, title='Все поставщики')


@main.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        new_supplier = Supplier(
            supplier_code=form.supplier_code.data,
            supplier_name=form.supplier_name.data,
            tin=form.tin.data,
            legal_postal_code=form.legal_postal_code.data,
            legal_city=form.legal_city.data,
            legal_street=form.legal_street.data,
            legal_house=form.legal_house.data,
            bank_account_number=form.bank_account_number.data,
            bank_postal_code=form.bank_postal_code.data,
            bank_city=form.bank_city.data,
            bank_street=form.bank_street.data,
            bank_house=form.bank_house.data
        )
        db.session.add(new_supplier)
        db.session.commit()
        
        flash('Поставщик успешно добавлен!')
        return redirect(url_for('main.suppliers'))
        
    return render_template('add_supplier.html', title='Добавить поставщика', form=form)


@main.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm()

    # Если форма отправлена
    if form.validate_on_submit():
        supplier.supplier_code = form.supplier_code.data
        supplier.supplier_name = form.supplier_name.data
        supplier.tin = form.tin.data
        supplier.legal_postal_code = form.legal_postal_code.data
        supplier.legal_city = form.legal_city.data
        supplier.legal_street = form.legal_street.data
        supplier.legal_house = form.legal_house.data
        supplier.bank_account_number = form.bank_account_number.data
        supplier.bank_postal_code = form.bank_postal_code.data
        supplier.bank_city = form.bank_city.data
        supplier.bank_street = form.bank_street.data
        supplier.bank_house = form.bank_house.data
        
        db.session.commit()
        flash('Данные поставщика обновлены!', 'success')
        return redirect(url_for('main.suppliers'))

    # Если это GET-запрос
    elif request.method == 'GET':
        form.supplier_code.data = supplier.supplier_code
        form.supplier_name.data = supplier.supplier_name
        form.tin.data = supplier.tin
        form.legal_postal_code.data = supplier.legal_postal_code
        form.legal_city.data = supplier.legal_city
        form.legal_street.data = supplier.legal_street
        form.legal_house.data = supplier.legal_house
        form.bank_account_number.data = supplier.bank_account_number
        form.bank_postal_code.data = supplier.bank_postal_code
        form.bank_city.data = supplier.bank_city
        form.bank_street.data = supplier.bank_street
        form.bank_house.data = supplier.bank_house
    
    return render_template('add_supplier.html', title='Редактировать поставщика', form=form)


@main.route('/materials')
def materials():
    all_materials = Material.query.all()
    return render_template('materials.html', materials=all_materials, title='Все материалы', models=models)


@main.route('/material/<int:material_id>/suppliers')
def suppliers_for_material(material_id):
    material = Material.query.get_or_404(material_id)
    
    # --- САМЫЙ ГЛАВНЫЙ ЗАПРОС ---
    # Мы хотим найти всех уникальных Поставщиков (Supplier),
    # которые связаны с таблицей Складских единиц (StorageUnit),
    # где id материала равен тому, что мы получили.
    suppliers = Supplier.query \
        .join(StorageUnit) \
        .filter(StorageUnit.material_id == material_id) \
        .distinct() \
        .all()
        
    # Передаем найденный материал и список поставщиков в новый шаблон
    return render_template('suppliers_for_material.html',
                           material=material,
                           suppliers=suppliers,
                           title=f"Поставщики материала: {material.material_name}")


@main.route('/add_material', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        new_material = Material(
            material_code=form.material_code.data,
            material_class_code=form.material_class_code.data,
            material_group_code=form.material_group_code.data,
            material_name=form.material_name.data
        )
        db.session.add(new_material)
        db.session.commit()
        flash('Материал успешно добавлен!', 'success')
        return redirect(url_for('main.materials'))
    
    return render_template('add_material.html', title='Добавить материал', form=form)


@main.route('/units')
def units():
    all_units = UnitOfMeasurement.query.all()
    return render_template('units.html', units=all_units, title='Единицы измерения')


@main.route('/add_unit', methods=['GET', 'POST'])
def add_unit():
    form = UnitOfMeasurementForm()
    if form.validate_on_submit():
        new_unit = UnitOfMeasurement(unit_name=form.unit_name.data)
        db.session.add(new_unit)
        db.session.commit()
        flash('Единица измерения добавлена!', 'success')
        return redirect(url_for('main.units'))
    return render_template('add_unit.html', title='Добавить единицу измерения', form=form)


@main.route('/storage_units')
def storage_units():
    # №2 предоставить возможность добавления единицы хранения с указанием всех реквизитов
    all_units = StorageUnit.query.order_by(StorageUnit.date.desc()).all()
    return render_template('storage_units.html', units=all_units, title='Складские единицы')


@main.route('/add_storage_unit', methods=['GET', 'POST'])
def add_storage_unit():
    form = StorageUnitForm()
    
    # Мы получаем список всех поставщиков/материалов/единиц из БД
    # и передаем их в форму в виде (id, name).
    # ID будет значением <option>, а имя - текстом, который видит пользователь.
    form.supplier.choices = [(s.id, s.supplier_name) for s in Supplier.query.order_by('supplier_name').all()]
    form.material.choices = [(m.id, m.material_name) for m in Material.query.order_by('material_name').all()]
    form.unit.choices = [(u.id, u.unit_name) for u in UnitOfMeasurement.query.order_by('unit_name').all()]

    if form.validate_on_submit():
        new_storage_unit = StorageUnit(
            supplier_id=form.supplier.data,
            material_id=form.material.data,
            unit_id=form.unit.data,
            order_number=form.order_number.data,
            balance_account=form.balance_account.data,
            accompanying_document_code=form.accompanying_document_code.data,
            accompanying_document_number=form.accompanying_document_number.data,
            material_account=form.material_account.data,
            quantity_received=form.quantity_received.data,
            unit_price=form.unit_price.data
        )
        db.session.add(new_storage_unit)
        db.session.commit()
        flash('Новая складская единица успешно добавлена!', 'success')
        return redirect(url_for('main.storage_units'))
    
    return render_template('add_storage_unit.html', title='Добавить складскую единицу', form=form)


@main.route('/reports/bank_suppliers')
def bank_report():
    # 1. Взять четыре колонки с адресом банка и посчитать количество ID поставщиков (func.count).
    # 2. Сгруппировать все записи по этим четырем колонкам адреса (group_by).
    #    В результате все поставщики с одинаковым адресом банка попадут в одну "корзину".
    # 3. Отфильтровать те записи, где адрес не указан, чтобы не было пустой строки в отчете.
    # 4. Выполнить запрос и получить все "корзины".
    report_data = db.session.query(
        Supplier.bank_postal_code,
        Supplier.bank_city,
        Supplier.bank_street,
        Supplier.bank_house,
        func.count(Supplier.id).label('supplier_count')
    ).group_by(
        Supplier.bank_postal_code,
        Supplier.bank_city,
        Supplier.bank_street,
        Supplier.bank_house
    ).filter(
        Supplier.bank_city.isnot(None),
        Supplier.bank_city != ''
    ).all()

    return render_template('bank_report.html',
                           report_data=report_data,
                           title="Отчет: Количество поставщиков по адресам банков")