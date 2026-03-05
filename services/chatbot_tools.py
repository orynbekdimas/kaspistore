from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, time as dtime, date
from typing import Optional

from sqlalchemy import func

# импорттарды өз проектіңе сай қоямыз:
from models import db, Product, StockMovement, OnwayItem, IncomingItem


@dataclass
class TopProfitResult:
    name: str
    profit: int
    start: str
    end: str


def _calc_profit_for_sale(m: StockMovement, p: Product) -> int:
    qty = int(-m.qty_change)  # SALE кезінде qty_change теріс
    revenue = int(m.sale_sum or 0)
    delivery = int(m.delivery_cost or 0)
    pct = int(m.commission_pct or 12)

    commission = int(round(revenue * pct / 100.0))
    cogs = qty * int(p.purchase_price or 0)
    profit = revenue - commission - delivery - cogs
    return int(profit)


def top_profit_product_last_week(now: Optional[date] = None) -> Optional[TopProfitResult]:
    today = now or datetime.utcnow().date()
    start_d = today - timedelta(days=7)
    end_d = today

    start_dt = datetime.combine(start_d, dtime.min)
    end_dt = datetime.combine(end_d, dtime.max)

    rows = (
        db.session.query(StockMovement, Product)
        .join(Product, Product.id == StockMovement.product_id)
        .filter(StockMovement.kind == "SALE")
        .filter(StockMovement.created_at >= start_dt)
        .filter(StockMovement.created_at <= end_dt)
        .all()
    )

    if not rows:
        return None

    by_pid: dict[int, int] = {}
    for m, p in rows:
        by_pid[p.id] = by_pid.get(p.id, 0) + _calc_profit_for_sale(m, p)

    best_pid = max(by_pid, key=by_pid.get)
    best_profit = int(by_pid[best_pid])

    best_product = Product.query.get(best_pid)
    name = best_product.name if best_product else str(best_pid)

    return TopProfitResult(
        name=name,
        profit=best_profit,
        start=start_d.isoformat(),
        end=end_d.isoformat(),
    )


def summary_numbers() -> dict:
    # склад суммасы (available * purchase)
    products = Product.query.all()
    stock_total = 0
    for p in products:
        stock_qty = int(p.stock_qty or 0)
        onway_qty = int(getattr(p, "onway_qty", 0) or 0)
        available = max(0, stock_qty - onway_qty)
        stock_total += available * int(p.purchase_price or 0)

    incoming_total = int(
        db.session.query(func.coalesce(func.sum(IncomingItem.qty * IncomingItem.purchase_price), 0))
        .filter(IncomingItem.is_active == True)  # noqa
        .scalar() or 0
    )

    onway_total = int(
        db.session.query(func.coalesce(func.sum(OnwayItem.sale_price), 0))
        .filter(OnwayItem.is_active == True)  # noqa
        .scalar() or 0
    )

    return {
        "stockTotal": stock_total,
        "incomingTotal": incoming_total,
        "onwayTotal": onway_total,
        "turnoverTotal": int(stock_total) + int(incoming_total) + int(onway_total),
    }