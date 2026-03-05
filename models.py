from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Негізгі атау
    name = db.Column(db.String(255), nullable=False, unique=True)

    # Закуп
    purchase_price = db.Column(db.Integer, nullable=False, default=0)

    # Қолда бар (склад)
    stock_qty = db.Column(db.Integer, nullable=False, default=0)

    # Резерв (ескі логика - қазір қолданылмайды, бірақ БД-да қалсын)
    reserved_qty = db.Column(db.Integer, nullable=False, default=0)

    # ЖОЛДА (қолмен қосылатын onway позициялар саны)
    onway_qty = db.Column(db.Integer, nullable=False, default=0)

    @property
    def available_qty(self) -> int:
        """Қолжетімді = қолда - резерв - жолда"""
        try:
            return int(self.stock_qty or 0) - int(self.reserved_qty or 0) - int(self.onway_qty or 0)
        except Exception:
            return 0


class ProductAlias(db.Model):
    __tablename__ = "product_aliases"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    alias = db.Column(db.String(255), nullable=False, unique=True)


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    # IN / SALE / ONWAY / RETURN
    kind = db.Column(db.String(20), nullable=False)

    # + немесе -
    qty_change = db.Column(db.Integer, nullable=False)

    note = db.Column(db.String(255), nullable=True)

    # SALE үшін қосымша:
    sale_sum = db.Column(db.Integer, nullable=False, default=0)         # түсім
    delivery_cost = db.Column(db.Integer, nullable=False, default=0)    # доставка (продавец)
    commission_pct = db.Column(db.Integer, nullable=False, default=12)  # комиссия %

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def calc_profit(self, purchase_price: int) -> int:
        qty_sold = int(-self.qty_change) if self.kind == "SALE" else 0
        revenue = int(self.sale_sum or 0)
        delivery = int(self.delivery_cost or 0)
        pct = int(self.commission_pct or 12)

        commission = int(round(revenue * pct / 100.0))
        cogs = int(purchase_price or 0) * qty_sold
        return int(revenue - commission - delivery - cogs)


class ImportBatch(db.Model):
    __tablename__ = "import_batches"

    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String(255), nullable=False)
    file_hash = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class OnwayItem(db.Model):
    """
    ЖОЛДА позициялары: әр жазба = 1 дана (қолмен қосылады), sale_price сақтаймыз.
    """
    __tablename__ = "onway_items"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    # 1 дана позицияның сатылған бағасы
    sale_price = db.Column(db.Integer, nullable=False, default=0)

    # active = жолда тұр, false = жабылды (сатылды/алып тасталды)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class IncomingItem(db.Model):
    """
    КЕЛЕ ЖАТЫР: заказ берілген, бірақ складқа келмеген.
    qty көп болуы мүмкін, purchase_price осы заказдағы закуп.
    """
    __tablename__ = "incoming_items"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    qty = db.Column(db.Integer, nullable=False, default=1)
    purchase_price = db.Column(db.Integer, nullable=False, default=0)

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
