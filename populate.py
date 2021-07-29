from datetime import date

from django.contrib.auth.models import User

from my_portfolio_web_app.model.financial_instrument import (
    Bond,
    Currency,
    Stock,
)
from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    CouponClipping,
    Inflow,
    Outflow,
    Purchase,
    Sale,
    StockDividend,
)

"""
    To execute do:
    python manage.py flush
    python manage.py shell
    >  exec(open('populate.py', encoding='utf-8').read())
"""


def ars(amount):
    return Measurement(amount, pesos)


def usd(amount):
    return Measurement(amount, dollars)


def create_admin():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')


if __name__ == '__main__':
    create_admin()
    pesos = Currency(code='$', description='Pesos')
    dollars = Currency(code='USD', description='Dólares EEUU')
    mirg = Stock(code="MIRG", description="MIRGOR")
    tb21 = Bond(code='TB21', description='BONOS TES NAC EN PESOS BADLAR Privada + 100 pbs.',
                maturity_date=date(2021, 8, 5), price_each_quantity=100)
    tc20 = Bond(code='TC20', description='BONCER 2020', maturity_date=date(2020, 4, 28), price_each_quantity=100)
    tj20 = Bond(code='TJ20', description='BONOS DEL TESORO 2020', maturity_date=date(2020, 6, 21),
                price_each_quantity=100)
    to21 = Bond(code='TO21', description='BONTE 2021', maturity_date=date(2021, 10, 4), price_each_quantity=100)
    rpc4o = Bond(code='RPC4O', description='IRSA CLASE IV', maturity_date=date(2020, 9, 14))
    irc1o = Bond(code='IRC1O', description='IRSA 2020 U$S 10%', maturity_date=date(2020, 11, 16))
    csdoo = Bond(code='CSDOO', description='CRESUD SACIF Y A 2023 U$S 6.5%', maturity_date=date(2023, 2, 16))
    irc9o = Bond(code='IRC9O', description='IRSA CLASE IX', maturity_date=date(2023, 3, 1))
    bma = Stock(code="BMA", description="BANCO MACRO")
    tgno4 = Stock(code="TGNO4", description="TRANSPORTADORA GAS DEL NORTE")
    abev = Stock(code="ABEV", description="AMBEV")
    ogzd = Stock(code="OGZD", description="GAZPROM")
    arco = Stock(code="ARCO", description="ARCOS DORADOS")
    vist = Stock(code="VIST", description="VISTA OIL")
    ko = Stock(code="KO", description="COCA COLA")
    meli = Stock(code="MELI", description="MERCADO LIBRE")
    auy = Stock(code="AUY", description="YAMANA GOLD")
    baba = Stock(code="BABA", description="ALI BABA")
    gold = Stock(code="GOLD", description="GOLD")
    pfe = Stock(code="PFE", description="PFEIZER")
    intc = Stock(code="INTC", description="INTEL")
    ptsto = Bond(code='PTSTO', description='ON PETROBRAS ARG REGS 7,375%', maturity_date=date(2023, 7, 21))
    spot = Stock(code='SPOT', description='SPOTIFY')
    tsla = Stock(code='TSLA', description='TESLA')
    teco2 = Stock(code='TECO2', description='TELECOM')
    trip = Stock(code='TRIP', description='TRIP ADVISOR')
    pesos.save()
    dollars.save()
    mirg.save()
    tb21.save()
    tc20.save()
    tj20.save()
    to21.save()
    rpc4o.save()
    irc1o.save()
    csdoo.save()
    irc9o.save()
    bma.save()
    tgno4.save()
    abev.save()
    ogzd.save()
    arco.save()
    vist.save()
    ko.save()
    meli.save()
    auy.save()
    baba.save()
    gold.save()
    pfe.save()
    intc.save()
    ptsto.save()
    spot.save()
    tsla.save()
    teco2.save()
    trip.save()

    print("Created instruments")

    martin = InvestmentIndividualAccount.objects.create(description='Martín')
    pablo = InvestmentIndividualAccount.objects.create(description='Pablo')
    andres = InvestmentIndividualAccount.objects.create(description='Andrés')
    portfolio = InvestmentPortfolio.objects.create(description='Gotelli Ferenaz')

    portfolio.individual_accounts.add(martin)
    portfolio.individual_accounts.add(pablo)
    portfolio.individual_accounts.add(andres)

    print("Created accounts")

    t1 = Purchase(date=date(2020, 1, 17), security_quantity=20.7, financial_instrument=mirg,
                  price=ars(957.8792), broker="IOL", commissions=ars(139.15), account=martin)
    t2 = Purchase(date=date(2020, 2, 13), security_quantity=2, financial_instrument=bma, price=ars(266.5), broker="IOL",
                  commissions=ars(3.75), account=martin)
    t3 = Purchase(date=date(2020, 2, 27), security_quantity=41, financial_instrument=bma, price=ars(244.9),
                  broker="IOL", commissions=ars(70.46), account=martin)
    t4 = Purchase(date=date(2020, 3, 3), security_quantity=19164, financial_instrument=tb21, price=ars(0.775),
                  broker="IOL", commissions=ars(75.75), account=martin)
    t5 = Purchase(date=date(2020, 3, 9), security_quantity=6412, financial_instrument=tc20, price=ars(2.275),
                  broker="IOL", commissions=ars(74.4), account=martin)
    t6 = Sale(date=date(2020, 3, 9), security_quantity=19164, financial_instrument=tb21, price=ars(0.792), broker="IOL",
              commissions=ars(77.41), account=martin)
    t7 = Purchase(date=date(2020, 3, 10), security_quantity=3411, financial_instrument=tc20, price=ars(2.277),
                  broker="IOL", commissions=ars(39.61), account=martin)
    t8 = Purchase(date=date(2020, 3, 13), security_quantity=3, financial_instrument=bma, price=ars(182), broker="IOL",
                  commissions=ars(3.83), account=martin)
    t9 = Purchase(date=date(2020, 4, 3), security_quantity=322, financial_instrument=tj20, price=ars(0.62),
                  broker="IOL", commissions=ars(1.02), account=martin)
    t10 = Purchase(date=date(2020, 4, 16), security_quantity=40540, financial_instrument=tj20, price=ars(0.74),
                   broker="IOL", commissions=ars(153), account=martin)
    t11 = Purchase(date=date(2020, 4, 16), security_quantity=26351, financial_instrument=tj20, price=ars(0.74),
                   broker="IOL", commissions=ars(99.45), account=martin)
    t12 = CouponClipping(date=date(2020, 4, 28), security_quantity=31303.45, financial_instrument=pesos,
                         referenced_financial_instrument=tc20, broker="IOL", commissions=ars(3.48), account=martin)
    t13 = Purchase(date=date(2020, 4, 29), security_quantity=43013, financial_instrument=to21, price=ars(0.724725),
                   broker="IOL", commissions=ars(158.98), account=martin)
    t14 = Purchase(date=date(2020, 5, 4), security_quantity=1645, financial_instrument=tgno4, price=ars(24.25),
                   broker="IOL", commissions=ars(279.96), account=martin)
    t15 = Sale(date=date(2020, 5, 5), security_quantity=20.7, financial_instrument=mirg, price=ars(670), broker="IOL",
               commissions=ars(97.34), account=martin)
    t16 = Purchase(date=date(2020, 5, 6), security_quantity=19402, financial_instrument=to21, price=ars(0.67),
                   broker="IOL", commissions=ars(66.3), account=martin)
    t17 = Purchase(date=date(2020, 5, 6), security_quantity=113, financial_instrument=rpc4o, price=ars(87.50),
                   broker="BALANZ", commissions=ars(59.43), account=martin)
    t18 = Purchase(date=date(2020, 5, 11), security_quantity=793, financial_instrument=rpc4o, price=ars(87.936948),
                   broker="BALANZ", commissions=ars(419.10), account=pablo)
    t19 = Sale(date=date(2020, 5, 12), security_quantity=46, financial_instrument=bma, price=ars(246), broker="IOL",
               commissions=ars(79.41), account=martin)
    t20 = Purchase(date=date(2020, 6, 3), security_quantity=12, financial_instrument=abev, price=ars(935), broker="IOL",
                   commissions=ars(78.75), account=martin)
    t21 = Purchase(date=date(2020, 6, 3), security_quantity=22, financial_instrument=ogzd, price=ars(345), broker="IOL",
                   commissions=ars(53.27), account=martin)
    t22 = Purchase(date=date(2020, 6, 4), security_quantity=11, financial_instrument=arco, price=ars(1065),
                   broker="IOL", commissions=ars(82.22), account=martin)
    t23 = CouponClipping(date=date(2020, 6, 12), security_quantity=9.95, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(2.5), account=pablo)
    t24 = CouponClipping(date=date(2020, 6, 12), security_quantity=1.42, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(0.36), account=martin)
    t25 = CouponClipping(date=date(2020, 6, 21), security_quantity=73427.44, financial_instrument=pesos,
                         referenced_financial_instrument=tj20, broker="IOL", commissions=ars(31.07), account=martin)
    t26 = Purchase(date=date(2020, 6, 23), security_quantity=360, financial_instrument=csdoo, price=ars(82),
                   broker="BALANZ", commissions=ars(177.42), account=martin)
    t27 = Purchase(date=date(2020, 6, 24), security_quantity=17, financial_instrument=arco, price=ars(845),
                   broker="IOL", commissions=ars(100.81), account=martin)
    t28 = Purchase(date=date(2020, 7, 1), security_quantity=34, financial_instrument=ogzd, price=ars(290.5),
                   broker="IOL", commissions=ars(69.32), account=martin)
    t29 = Purchase(date=date(2020, 7, 6), security_quantity=22, financial_instrument=abev, price=ars(885), broker="IOL",
                   commissions=ars(136.64), account=martin)
    t30 = Purchase(date=date(2020, 7, 6), security_quantity=544, financial_instrument=csdoo, price=ars(92),
                   broker="BALANZ", commissions=ars(300.79), account=martin)
    t31 = Purchase(date=date(2020, 8, 5), security_quantity=9, financial_instrument=vist, price=ars(2150), broker="IOL",
                   commissions=ars(135.8), account=martin)
    t32 = Purchase(date=date(2020, 8, 5), security_quantity=22, financial_instrument=abev, price=ars(900), broker="IOL",
                   commissions=ars(138.96), account=martin)
    t33 = CouponClipping(date=date(2020, 8, 18), security_quantity=29.18, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(7.92), account=martin)
    t34 = StockDividend(date=date(2020, 8, 21), security_quantity=8.15, financial_instrument=dollars,
                        referenced_financial_instrument=ogzd, broker="IOL", commissions=ars(7.65), account=martin)
    t35 = StockDividend(date=date(2020, 8, 24), security_quantity=262.12, financial_instrument=pesos,
                        referenced_financial_instrument=arco, broker="IOL", commissions=ars(3.17), account=martin)
    t36 = Purchase(date=date(2020, 9, 1), security_quantity=49, financial_instrument=bma, price=ars(241), broker="IOL",
                   commissions=ars(82.88), account=martin)
    t37 = Purchase(date=date(2020, 9, 1), security_quantity=8, financial_instrument=vist, price=ars(1850), broker="IOL",
                   commissions=ars(103.87), account=martin)
    t38 = Purchase(date=date(2020, 9, 14), security_quantity=307, financial_instrument=irc1o, price=usd(1.005),
                   broker="BALANZ", commissions=ars(0.24) + usd(1.86), account=martin)
    t39 = Sale(date=date(2020, 9, 14), security_quantity=169, financial_instrument=csdoo, price=usd(0.92),
               broker="BALANZ", commissions=ars(0.12) + usd(0.93), account=martin)
    t40 = CouponClipping(date=date(2020, 9, 14), security_quantity=803.17, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(2.82), account=pablo)
    t41 = CouponClipping(date=date(2020, 9, 14), security_quantity=114.45, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(0.40), account=martin)
    t42 = Purchase(date=date(2020, 9, 17), security_quantity=889, financial_instrument=csdoo, price=usd(0.9),
                   broker="BALANZ", commissions=ars(0.61) + usd(4.80), account=pablo)
    t43 = Purchase(date=date(2020, 9, 23), security_quantity=147, financial_instrument=csdoo, price=usd(0.88),
                   broker="BALANZ", commissions=ars(0.10) + usd(0.78), account=martin)
    t44 = CouponClipping(date=date(2020, 10, 5), security_quantity=5679.76, financial_instrument=pesos,
                         referenced_financial_instrument=to21, broker="IOL", commissions=ars(28.40), account=martin)
    t45 = Purchase(date=date(2020, 10, 8), security_quantity=27, financial_instrument=bma, price=ars(214), broker="IOL",
                   commissions=ars(40.55), account=martin)
    t46 = Sale(date=date(2020, 10, 28), security_quantity=307, financial_instrument=irc1o, price=usd(1.005),
               broker="BALANZ", account=martin)
    t47 = Purchase(date=date(2020, 10, 28), security_quantity=307, financial_instrument=irc9o, price=usd(1.005),
                   broker="BALANZ", account=martin)
    t48 = Purchase(date=date(2020, 10, 30), security_quantity=13, financial_instrument=ko, price=ars(1480),
                   broker="IOL", commissions=ars(135.02), account=andres)
    t49 = Purchase(date=date(2020, 10, 30), security_quantity=20, financial_instrument=abev, price=ars(1000),
                   broker="IOL", commissions=ars(140.36), account=andres)
    t50 = Purchase(date=date(2020, 10, 30), security_quantity=432, financial_instrument=csdoo, price=ars(115),
                   broker="BALANZ", commissions=ars(298.58), account=andres)
    t51 = Purchase(date=date(2020, 11, 2), security_quantity=8, financial_instrument=meli, price=ars(3100),
                   broker="IOL", commissions=ars(174.05), account=martin)
    t52 = Purchase(date=date(2020, 11, 10), security_quantity=3, financial_instrument=meli, price=ars(3130),
                   broker="IOL", commissions=ars(65.90), account=martin)
    t53 = CouponClipping(date=date(2020, 11, 16), security_quantity=460.64, financial_instrument=pesos,
                         referenced_financial_instrument=irc9o, broker="BALANZ", commissions=ars(0), account=martin)
    t54 = CouponClipping(date=date(2020, 11, 16), security_quantity=5.91, financial_instrument=dollars,
                         referenced_financial_instrument=irc9o, broker="BALANZ", commissions=ars(2.23), account=martin)
    t55 = Purchase(date=date(2020, 12, 1), security_quantity=13, financial_instrument=auy, price=ars(800),
                   broker="IOL", commissions=ars(72.99), account=martin)
    t56 = Purchase(date=date(2020, 12, 1), security_quantity=3, financial_instrument=baba, price=ars(4400),
                   broker="IOL", commissions=ars(92.64), account=martin)
    t57 = Purchase(date=date(2020, 12, 9), security_quantity=4, financial_instrument=baba, price=ars(4200),
                   broker="IOL", commissions=ars(117.90), account=martin)
    t58 = StockDividend(date=date(2020, 12, 17), security_quantity=0.65, financial_instrument=dollars,
                        referenced_financial_instrument=ko, broker="IOL", commissions=ars(0.69), account=andres)
    t59 = Purchase(date=date(2021, 1, 4), security_quantity=8, financial_instrument=baba, price=ars(3645),
                   broker="IOL", commissions=ars(204.65), account=martin)
    t60 = Purchase(date=date(2021, 1, 5), security_quantity=5, financial_instrument=gold, price=ars(3580),
                   broker="IOL", commissions=ars(125.63), account=martin)
    t61 = StockDividend(date=date(2021, 1, 13), security_quantity=10.02, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(10.98), account=martin)
    t62 = StockDividend(date=date(2021, 1, 13), security_quantity=3.58, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(3.92), account=andres)
    t63 = Purchase(date=date(2021, 1, 22), security_quantity=391, financial_instrument=tgno4, price=ars(38.30),
                   broker="IOL", commissions=ars(105.10), account=martin)
    t64 = Purchase(date=date(2021, 2, 1), security_quantity=25, financial_instrument=auy, price=ars(720),
                   broker="IOL", commissions=ars(126.32), account=martin)
    t65 = Purchase(date=date(2021, 2, 8), security_quantity=8, financial_instrument=gold, price=ars(3400),
                   broker="IOL", commissions=ars(190.89), account=andres)
    t66 = Purchase(date=date(2021, 2, 8), security_quantity=6, financial_instrument=gold, price=ars(3400),
                   broker="IOL", commissions=ars(143.17), account=martin)
    t67 = Purchase(date=date(2021, 2, 8), security_quantity=8, financial_instrument=pfe, price=ars(2700),
                   broker="IOL", commissions=ars(151.59), account=martin)
    t68 = StockDividend(date=date(2021, 2, 9), security_quantity=0.76, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(0.85), account=andres)
    t69 = StockDividend(date=date(2021, 2, 9), security_quantity=2.12, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(2.39), account=martin)
    t70 = Purchase(date=date(2021, 2, 9), security_quantity=3, financial_instrument=pfe, price=ars(2700),
                   broker="IOL", commissions=ars(56.85), account=martin)
    t71 = StockDividend(date=date(2021, 2, 10), security_quantity=0.22, financial_instrument=dollars,
                        referenced_financial_instrument=auy, broker="IOL", commissions=ars(0.61), account=martin)
    t72 = Sale(date=date(2021, 2, 17), security_quantity=17, financial_instrument=vist, price=ars(2340), broker="IOL",
               commissions=ars(279.17), account=martin)
    t73 = CouponClipping(date=date(2021, 2, 17), security_quantity=28.80, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(9.46), account=martin)
    t74 = CouponClipping(date=date(2021, 2, 17), security_quantity=29.02, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(9.53), account=pablo)
    t75 = CouponClipping(date=date(2021, 2, 17), security_quantity=14.11, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(4.63), account=andres)
    t76 = Sale(date=date(2021, 2, 18), security_quantity=28, financial_instrument=arco, price=ars(1600), broker="IOL",
               commissions=ars(314.41), account=martin)
    t77 = Sale(date=date(2021, 2, 18), security_quantity=2036, financial_instrument=tgno4, price=ars(44), broker="IOL",
               commissions=ars(628.70), account=martin)
    t78 = Sale(date=date(2021, 2, 18), security_quantity=56, financial_instrument=ogzd, price=ars(450), broker="IOL",
               commissions=ars(176.85), account=martin)
    t79 = Sale(date=date(2021, 2, 18), security_quantity=62415, financial_instrument=to21, price=ars(0.965),
               broker="IOL", commissions=ars(307.17), account=martin)
    t80 = Sale(date=date(2021, 2, 18), security_quantity=76, financial_instrument=bma, price=ars(239.5), broker="IOL",
               commissions=ars(127.74), account=martin)
    t81 = Sale(date=date(2021, 2, 18), security_quantity=11, financial_instrument=meli, price=ars(4535), broker="IOL",
               commissions=ars(350.10), account=martin)
    t82 = CouponClipping(date=date(2021, 2, 22), security_quantity=7.7, financial_instrument=dollars,
                         referenced_financial_instrument=irc9o, broker="BALANZ",
                         commissions=ars(2.39), account=martin)  # DÓLAR CABLE
    t83 = Purchase(date=date(2021, 2, 24), security_quantity=25, financial_instrument=abev, price=ars(1200),
                   broker="IOL", commissions=ars(210.54), account=pablo)
    t84 = Purchase(date=date(2021, 2, 24), security_quantity=10, financial_instrument=meli, price=ars(4160),
                   broker="IOL", commissions=ars(291.95), account=pablo)
    t85 = Purchase(date=date(2021, 2, 24), security_quantity=12, financial_instrument=arco, price=ars(1550),
                   broker="IOL", commissions=ars(130.53), account=pablo)
    t86 = Purchase(date=date(2021, 2, 24), security_quantity=2, financial_instrument=gold, price=ars(2937),
                   broker="IOL", commissions=ars(41.23), account=pablo)
    t87 = Purchase(date=date(2021, 3, 4), security_quantity=1, financial_instrument=meli, price=ars(3875),
                   broker="IOL", commissions=ars(27.20), account=martin)
    t88 = StockDividend(date=date(2021, 3, 18), security_quantity=0.65, financial_instrument=dollars,
                        referenced_financial_instrument=gold, broker="IOL", commissions=ars(0.76), account=martin)
    t89 = StockDividend(date=date(2021, 3, 18), security_quantity=0.47, financial_instrument=dollars,
                        referenced_financial_instrument=gold, broker="IOL", commissions=ars(0.55), account=andres)
    t90 = StockDividend(date=date(2021, 3, 18), security_quantity=0.12, financial_instrument=dollars,
                        referenced_financial_instrument=gold, broker="IOL", commissions=ars(0.14), account=pablo)
    t91 = StockDividend(date=date(2021, 4, 8), security_quantity=0.67, financial_instrument=dollars,
                        referenced_financial_instrument=ko, broker="IOL", commissions=ars(0.80), account=andres)
    t92 = StockDividend(date=date(2021, 4, 21), security_quantity=0.65, financial_instrument=dollars,
                        referenced_financial_instrument=auy, broker="IOL", commissions=ars(0.77), account=martin)
    t93 = Purchase(date=date(2021, 4, 30), security_quantity=16, financial_instrument=intc, price=ars(1828),
                   broker="IOL", commissions=ars(205.26), account=martin)
    t94 = Purchase(date=date(2021, 4, 30), security_quantity=27, financial_instrument=auy, price=ars(725),
                   broker="IOL", commissions=ars(137.38), account=martin)
    t95 = Purchase(date=date(2021, 5, 6), security_quantity=22, financial_instrument=spot, price=ars(1315),
                   broker="IOL", commissions=ars(203.03), account=pablo)
    t96 = Purchase(date=date(2021, 5, 6), security_quantity=12, financial_instrument=meli, price=ars(3875),
                   broker="IOL", commissions=ars(326.34), account=pablo)
    t97 = Purchase(date=date(2021, 5, 6), security_quantity=1000, financial_instrument=ptsto, price=ars(155),
                   broker="BALANZ", commissions=ars(931.55), account=pablo)
    t98 = Sale(date=date(2021, 6, 1), security_quantity=20, financial_instrument=abev, price=ars(1835), broker="IOL",
               commissions=ars(257.56), account=andres)
    t99 = Sale(date=date(2021, 6, 1), security_quantity=25, financial_instrument=abev, price=ars(1835), broker="IOL",
               commissions=ars(321.95), account=pablo)
    t100 = Sale(date=date(2021, 6, 1), security_quantity=20, financial_instrument=abev, price=ars(1835), broker="IOL",
                commissions=ars(257.56), account=martin)
    t101 = Sale(date=date(2021, 6, 2), security_quantity=36, financial_instrument=abev, price=ars(1850), broker="IOL",
                commissions=ars(467.40), account=martin)
    t102 = Purchase(date=date(2021, 6, 2), security_quantity=8, financial_instrument=tsla, price=ars(6710),
                    broker="IOL", commissions=ars(376.72), account=martin)
    t103 = Purchase(date=date(2021, 6, 2), security_quantity=210, financial_instrument=teco2, price=ars(190.25),
                    broker="IOL", commissions=ars(280.38), account=martin)
    t104 = Purchase(date=date(2021, 6, 2), security_quantity=16, financial_instrument=meli, price=ars(3750),
                    broker="IOL", commissions=ars(421.08), account=pablo)
    t105 = Purchase(date=date(2021, 6, 2), security_quantity=3, financial_instrument=trip, price=ars(3525),
                    broker="IOL", commissions=ars(74.22), account=pablo)
    t106 = Purchase(date=date(2021, 6, 2), security_quantity=11, financial_instrument=trip, price=ars(3525),
                    broker="IOL", commissions=ars(272.12), account=andres)

    d1 = Inflow(date=date(2020, 1, 1), security_quantity=8498.30, financial_instrument=pesos, broker="IOL",
                account=martin)  # Inicial
    d2 = Inflow(date=date(2020, 1, 6), security_quantity=20000, financial_instrument=pesos, broker="IOL",
                account=martin)  # Depósito
    d3 = Inflow(date=date(2020, 1, 20), security_quantity=123.51, financial_instrument=pesos, broker="IOL",
                account=martin)  # CAUCIÓN
    d4 = Inflow(date=date(2020, 2, 19), security_quantity=10000, financial_instrument=pesos, broker="IOL",
                account=martin)  # Depósito
    d5 = Inflow(date=date(2020, 2, 27), security_quantity=40.61, financial_instrument=pesos, broker="IOL",
                account=martin)  # CAUCIÓN
    d6 = Inflow(date=date(2020, 3, 1), security_quantity=20.81, financial_instrument=pesos,
                broker="IOL", account=martin)  # Cuenta remunerada
    d7 = Inflow(date=date(2020, 3, 3), security_quantity=15000, financial_instrument=pesos, broker="IOL",
                account=martin)  # Depósito
    d8 = Inflow(date=date(2020, 4, 1), security_quantity=26.81, financial_instrument=pesos,
                broker="IOL", account=martin)  # Cuenta remunerada
    d9 = Inflow(date=date(2020, 4, 15), security_quantity=50000, financial_instrument=pesos, broker="IOL",
                account=martin)  # Depósito
    d10 = Inflow(date=date(2020, 5, 1), security_quantity=82.09, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d11 = Inflow(date=date(2020, 5, 4), security_quantity=40000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d12 = Inflow(date=date(2020, 5, 5), security_quantity=10000, financial_instrument=pesos,
                 broker="BALANZ", account=martin)  # Depósito
    d13 = Inflow(date=date(2020, 5, 7), security_quantity=70000, financial_instrument=pesos,
                 broker="BALANZ", account=pablo)  # Depósito
    d14 = Outflow(date=date(2020, 5, 14), security_quantity=11999.17, financial_instrument=pesos,
                  broker="IOL", account=martin)  # Compra USD
    d15 = Outflow(date=date(2020, 5, 14), security_quantity=12118.73, financial_instrument=pesos,
                  broker="IOL", account=martin)  # Extracción
    d16 = Inflow(date=date(2020, 5, 14), security_quantity=12000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d17 = Inflow(date=date(2020, 6, 1), security_quantity=64.22, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d18 = Inflow(date=date(2020, 6, 3), security_quantity=31000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d19 = Outflow(date=date(2020, 6, 22), security_quantity=58600, financial_instrument=pesos,
                  broker="IOL", account=martin)  # Extracción
    d20 = Inflow(date=date(2020, 6, 22), security_quantity=30000, financial_instrument=pesos,
                 broker="BALANZ", account=martin)  # Depósito
    d21 = Inflow(date=date(2020, 7, 1), security_quantity=50000, financial_instrument=pesos,
                 broker="BALANZ", account=martin)  # Depósito
    d22 = Inflow(date=date(2020, 7, 1), security_quantity=30000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d23 = Inflow(date=date(2020, 7, 1), security_quantity=69.76, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d24 = Inflow(date=date(2020, 8, 1), security_quantity=80.85, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d25 = Inflow(date=date(2020, 8, 3), security_quantity=40000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d26 = Inflow(date=date(2020, 9, 1), security_quantity=25000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d27 = Inflow(date=date(2020, 9, 1), security_quantity=89.86, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d28 = Inflow(date=date(2020, 9, 23), security_quantity=134.01, financial_instrument=dollars,
                 broker="BALANZ", account=martin)  # Depósito
    d29 = Inflow(date=date(2020, 10, 1), security_quantity=27.09, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d30 = Inflow(date=date(2020, 10, 30), security_quantity=40000, financial_instrument=pesos, broker="IOL",
                 account=andres)  # Depósito
    d31 = Inflow(date=date(2020, 10, 30), security_quantity=50000, financial_instrument=pesos,
                 broker="BALANZ", account=andres)  # Depósito
    d32 = Inflow(date=date(2020, 11, 1), security_quantity=76.57, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d33 = Inflow(date=date(2020, 11, 2), security_quantity=25000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d34 = Inflow(date=date(2020, 11, 10), security_quantity=10000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d35 = Inflow(date=date(2020, 12, 1), security_quantity=116.61, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d36 = Inflow(date=date(2020, 12, 1), security_quantity=25000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d37 = Inflow(date=date(2020, 12, 9), security_quantity=15000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d38 = Inflow(date=date(2021, 1, 1), security_quantity=80.27, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d39 = Inflow(date=date(2021, 1, 4), security_quantity=50000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d40 = Inflow(date=date(2021, 1, 20), security_quantity=30000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d41 = Inflow(date=date(2021, 2, 1), security_quantity=304.59, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d42 = Inflow(date=date(2021, 2, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d43 = Inflow(date=date(2021, 2, 2), security_quantity=50000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d44 = Inflow(date=date(2021, 2, 2), security_quantity=30000, financial_instrument=pesos, broker="IOL",
                 account=andres)  # Depósito
    d45 = Outflow(date=date(2021, 2, 22), security_quantity=328222, financial_instrument=pesos,
                  broker="IOL", account=martin)  # Extracción
    d46 = Inflow(date=date(2021, 2, 24), security_quantity=100000, financial_instrument=pesos, broker="IOL",
                 account=pablo)  # Depósito
    d47 = Inflow(date=date(2021, 3, 1), security_quantity=652.38, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d48 = Inflow(date=date(2021, 3, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d49 = Inflow(date=date(2021, 4, 1), security_quantity=20.54, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d50 = Inflow(date=date(2021, 4, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d51 = Inflow(date=date(2021, 4, 30), security_quantity=50000, financial_instrument=pesos, broker="IOL",
                 account=martin)  # Depósito
    d52 = Inflow(date=date(2021, 5, 1), security_quantity=37.44, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d53 = Inflow(date=date(2021, 5, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d54 = Inflow(date=date(2021, 5, 6), security_quantity=185000, financial_instrument=pesos, broker="BALANZ",
                 account=pablo)  # Depósito
    d55 = Inflow(date=date(2021, 5, 6), security_quantity=100000, financial_instrument=pesos, broker="IOL",
                 account=pablo)  # Depósito
    d56 = Inflow(date=date(2021, 6, 1), security_quantity=822.86, financial_instrument=pesos,
                 broker="IOL", account=martin)  # Cuenta remunerada
    d57 = Inflow(date=date(2021, 6, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL", account=martin)  # Cuenta remunerada

    t1.save()
    t2.save()
    t3.save()
    t4.save()
    t5.save()
    t6.save()
    t7.save()
    t8.save()
    t9.save()
    t10.save()
    t11.save()
    t12.save()
    t13.save()
    t14.save()
    t15.save()
    t16.save()
    t17.save()
    t18.save()
    t19.save()
    t20.save()
    t21.save()
    t22.save()
    t23.save()
    t24.save()
    t25.save()
    t26.save()
    t27.save()
    t28.save()
    t29.save()
    t30.save()
    t31.save()
    t32.save()
    t33.save()
    t34.save()
    t35.save()
    t36.save()
    t37.save()
    t38.save()
    t39.save()
    t40.save()
    t41.save()
    t42.save()
    t43.save()
    t44.save()
    t45.save()
    t46.save()
    t47.save()
    t48.save()
    t49.save()
    t50.save()
    t51.save()
    t52.save()
    t53.save()
    t54.save()
    t55.save()
    t56.save()
    t57.save()
    t58.save()
    t59.save()
    t60.save()
    t61.save()
    t62.save()
    t63.save()
    t64.save()
    t65.save()
    t66.save()
    t67.save()
    t68.save()
    t69.save()
    t70.save()
    t71.save()
    t72.save()
    t73.save()
    t74.save()
    t75.save()
    t76.save()
    t77.save()
    t78.save()
    t79.save()
    t80.save()
    t81.save()
    t82.save()
    t83.save()
    t84.save()
    t85.save()
    t86.save()
    t87.save()
    t88.save()
    t89.save()
    t90.save()
    t91.save()
    t92.save()
    t93.save()
    t94.save()
    t95.save()
    t96.save()
    t97.save()
    t98.save()
    t99.save()
    t100.save()
    t101.save()
    t102.save()
    t103.save()
    t104.save()
    t105.save()
    t106.save()

    print("Saved all transactions")

    d1.save()
    d2.save()
    d3.save()
    d4.save()
    d5.save()
    d6.save()
    d7.save()
    d8.save()
    d9.save()
    d10.save()
    d11.save()
    d12.save()
    d13.save()
    d14.save()
    d15.save()
    d16.save()
    d17.save()
    d18.save()
    d19.save()
    d20.save()
    d21.save()
    d22.save()
    d23.save()
    d24.save()
    d25.save()
    d26.save()
    d27.save()
    d28.save()
    d29.save()
    d30.save()
    d31.save()
    d32.save()
    d33.save()
    d34.save()
    d35.save()
    d36.save()
    d37.save()
    d38.save()
    d39.save()
    d40.save()
    d41.save()
    d42.save()
    d43.save()
    d44.save()
    d45.save()
    d46.save()
    d47.save()
    d48.save()
    d49.save()
    d50.save()
    d51.save()
    d52.save()
    d53.save()
    d54.save()
    d55.save()
    d56.save()
    d57.save()

    print("Saved all deposit/extractions")
