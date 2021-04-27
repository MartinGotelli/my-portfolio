from datetime import date

from django.contrib.auth.models import User

from my_portfolio_web_app.model.financial_instrument import (
    Stock,
    Currency,
    Bond,
)
from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    Purchase,
    Sale,
    CouponClipping,
    StockDividend,
    Outflow,
    Inflow,
)

"""
    To execute do:
    python manage.py flush
    python manage.py shell
    >  exec(open('populate.py').read())
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
    t1 = Purchase(date=date(2020, 1, 17), security_quantity=20.7, financial_instrument=mirg,
                  price=ars(957.8792), broker="IOL", commissions=ars(139.15))
    t2 = Purchase(date=date(2020, 2, 13), security_quantity=2, financial_instrument=bma, price=ars(266.5), broker="IOL",
                  commissions=ars(3.75))
    t3 = Purchase(date=date(2020, 2, 27), security_quantity=41, financial_instrument=bma, price=ars(244.9),
                  broker="IOL", commissions=ars(70.46))
    t4 = Purchase(date=date(2020, 3, 3), security_quantity=19164, financial_instrument=tb21, price=ars(0.775),
                  broker="IOL", commissions=ars(75.75))
    t5 = Purchase(date=date(2020, 3, 9), security_quantity=6412, financial_instrument=tc20, price=ars(2.275),
                  broker="IOL", commissions=ars(74.4))
    t6 = Sale(date=date(2020, 3, 9), security_quantity=19164, financial_instrument=tb21, price=ars(0.792), broker="IOL",
              commissions=ars(77.41))
    t7 = Purchase(date=date(2020, 3, 10), security_quantity=3411, financial_instrument=tc20, price=ars(2.277),
                  broker="IOL", commissions=ars(39.61))
    t8 = Purchase(date=date(2020, 3, 13), security_quantity=3, financial_instrument=bma, price=ars(182), broker="IOL",
                  commissions=ars(3.83))
    t9 = Purchase(date=date(2020, 4, 3), security_quantity=322, financial_instrument=tj20, price=ars(0.62),
                  broker="IOL", commissions=ars(1.02))
    t10 = Purchase(date=date(2020, 4, 16), security_quantity=40540, financial_instrument=tj20, price=ars(0.74),
                   broker="IOL", commissions=ars(153))
    t11 = Purchase(date=date(2020, 4, 16), security_quantity=26351, financial_instrument=tj20, price=ars(0.74),
                   broker="IOL", commissions=ars(99.45))
    t12 = CouponClipping(date=date(2020, 4, 28), security_quantity=31303.45, financial_instrument=pesos,
                         referenced_financial_instrument=tc20, broker="IOL", commissions=ars(3.48))
    t13 = Purchase(date=date(2020, 4, 29), security_quantity=43013, financial_instrument=to21, price=ars(0.724725),
                   broker="IOL", commissions=ars(158.98))
    t14 = Purchase(date=date(2020, 5, 4), security_quantity=1645, financial_instrument=tgno4, price=ars(24.25),
                   broker="IOL", commissions=ars(279.96))
    t15 = Sale(date=date(2020, 5, 5), security_quantity=20.7, financial_instrument=mirg, price=ars(670), broker="IOL",
               commissions=ars(97.34))
    t16 = Purchase(date=date(2020, 5, 6), security_quantity=19402, financial_instrument=to21, price=ars(0.67),
                   broker="IOL", commissions=ars(66.3))
    t17 = Purchase(date=date(2020, 5, 6), security_quantity=113, financial_instrument=rpc4o, price=ars(87.50),
                   broker="BALANZ", commissions=ars(59.43))
    t18 = Purchase(date=date(2020, 5, 11), security_quantity=793, financial_instrument=rpc4o, price=ars(87.936948),
                   broker="BALANZ", commissions=ars(419.10))
    t19 = Sale(date=date(2020, 5, 12), security_quantity=46, financial_instrument=bma, price=ars(246), broker="IOL",
               commissions=ars(79.41))
    t20 = Purchase(date=date(2020, 6, 3), security_quantity=12, financial_instrument=abev, price=ars(935), broker="IOL",
                   commissions=ars(78.75))
    t21 = Purchase(date=date(2020, 6, 3), security_quantity=22, financial_instrument=ogzd, price=ars(345), broker="IOL",
                   commissions=ars(53.27))
    t22 = Purchase(date=date(2020, 6, 4), security_quantity=11, financial_instrument=arco, price=ars(1065),
                   broker="IOL", commissions=ars(82.22))
    t23 = CouponClipping(date=date(2020, 6, 12), security_quantity=9.95, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(2.5))
    t24 = CouponClipping(date=date(2020, 6, 12), security_quantity=1.42, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(0.36))
    t25 = CouponClipping(date=date(2020, 6, 22), security_quantity=73427.44, financial_instrument=pesos,
                         referenced_financial_instrument=tj20, broker="IOL", commissions=ars(31.07))
    t26 = Purchase(date=date(2020, 6, 23), security_quantity=360, financial_instrument=csdoo, price=ars(82),
                   broker="BALANZ", commissions=ars(177.42))
    t27 = Purchase(date=date(2020, 6, 24), security_quantity=17, financial_instrument=arco, price=ars(845),
                   broker="IOL", commissions=ars(100.81))
    t28 = Purchase(date=date(2020, 7, 1), security_quantity=34, financial_instrument=ogzd, price=ars(290.5),
                   broker="IOL", commissions=ars(69.32))
    t29 = Purchase(date=date(2020, 7, 6), security_quantity=22, financial_instrument=abev, price=ars(885), broker="IOL",
                   commissions=ars(136.64))
    t30 = Purchase(date=date(2020, 7, 6), security_quantity=544, financial_instrument=csdoo, price=ars(92),
                   broker="BALANZ", commissions=ars(300.79))
    t31 = Purchase(date=date(2020, 8, 5), security_quantity=9, financial_instrument=vist, price=ars(2150), broker="IOL",
                   commissions=ars(135.8))
    t32 = Purchase(date=date(2020, 8, 5), security_quantity=22, financial_instrument=abev, price=ars(900), broker="IOL",
                   commissions=ars(138.96))
    t33 = CouponClipping(date=date(2020, 8, 18), security_quantity=29.18, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(7.92))
    t34 = StockDividend(date=date(2020, 8, 21), security_quantity=8.15, financial_instrument=dollars,
                        referenced_financial_instrument=ogzd, broker="IOL", commissions=ars(7.65))
    t35 = StockDividend(date=date(2020, 8, 24), security_quantity=262.12, financial_instrument=pesos,
                        referenced_financial_instrument=arco, broker="IOL", commissions=ars(3.17))
    t36 = Purchase(date=date(2020, 9, 1), security_quantity=49, financial_instrument=bma, price=ars(241), broker="IOL",
                   commissions=ars(82.88))
    t37 = Purchase(date=date(2020, 9, 1), security_quantity=8, financial_instrument=vist, price=ars(1850), broker="IOL",
                   commissions=ars(103.87))
    t38 = Purchase(date=date(2020, 9, 14), security_quantity=307, financial_instrument=irc1o, price=usd(1.005),
                   broker="BALANZ", commissions=ars(0.24) + usd(1.86))
    t39 = Sale(date=date(2020, 9, 14), security_quantity=169, financial_instrument=csdoo, price=usd(0.92),
               broker="BALANZ", commissions=ars(0.12) + usd(0.93))
    t40 = CouponClipping(date=date(2020, 9, 14), security_quantity=803.17, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(2.82))
    t41 = CouponClipping(date=date(2020, 9, 14), security_quantity=114.45, financial_instrument=dollars,
                         referenced_financial_instrument=rpc4o, broker="BALANZ", commissions=ars(0.40))
    t42 = Purchase(date=date(2020, 9, 17), security_quantity=889, financial_instrument=csdoo, price=usd(0.9),
                   broker="BALANZ", commissions=ars(0.61) + usd(4.80))
    t43 = Purchase(date=date(2020, 9, 23), security_quantity=147, financial_instrument=csdoo, price=usd(0.88),
                   broker="BALANZ", commissions=ars(0.10) + usd(0.78))
    t44 = CouponClipping(date=date(2020, 10, 5), security_quantity=5679.76, financial_instrument=pesos,
                         referenced_financial_instrument=to21, broker="IOL", commissions=ars(28.40))
    t45 = Purchase(date=date(2020, 10, 8), security_quantity=27, financial_instrument=bma, price=ars(214), broker="IOL",
                   commissions=ars(40.55))
    t46 = Outflow(date=date(2020, 10, 28), security_quantity=307, financial_instrument=irc1o, broker="BALANZ")
    t47 = Inflow(date=date(2020, 10, 28), security_quantity=307, financial_instrument=irc9o, broker="BALANZ")
    t48 = Purchase(date=date(2020, 10, 30), security_quantity=13, financial_instrument=ko, price=ars(1480),
                   broker="IOL", commissions=ars(135.02))
    t49 = Purchase(date=date(2020, 10, 30), security_quantity=20, financial_instrument=abev, price=ars(1000),
                   broker="IOL", commissions=ars(140.36))
    t50 = Purchase(date=date(2020, 10, 30), security_quantity=432, financial_instrument=csdoo, price=ars(115),
                   broker="BALANZ", commissions=ars(298.58))
    t51 = Purchase(date=date(2020, 11, 2), security_quantity=8, financial_instrument=meli, price=ars(3100),
                   broker="IOL", commissions=ars(174.05))
    t52 = Purchase(date=date(2020, 11, 10), security_quantity=3, financial_instrument=meli, price=ars(3130),
                   broker="IOL", commissions=ars(65.90))
    t53 = CouponClipping(date=date(2020, 11, 16), security_quantity=460.64, financial_instrument=pesos,
                         referenced_financial_instrument=irc9o, broker="BALANZ", commissions=ars(0))
    t54 = CouponClipping(date=date(2020, 11, 16), security_quantity=5.91, financial_instrument=dollars,
                         referenced_financial_instrument=irc9o, broker="BALANZ", commissions=ars(2.23))
    t55 = Purchase(date=date(2020, 12, 1), security_quantity=13, financial_instrument=auy, price=ars(800),
                   broker="IOL", commissions=ars(72.99))
    t56 = Purchase(date=date(2020, 12, 1), security_quantity=3, financial_instrument=baba, price=ars(4400),
                   broker="IOL", commissions=ars(92.64))
    t57 = Purchase(date=date(2020, 12, 9), security_quantity=4, financial_instrument=baba, price=ars(4200),
                   broker="IOL", commissions=ars(117.90))
    t58 = StockDividend(date=date(2020, 12, 17), security_quantity=0.65, financial_instrument=dollars,
                        referenced_financial_instrument=ko, broker="IOL", commissions=ars(0.69))
    t59 = Purchase(date=date(2021, 1, 4), security_quantity=8, financial_instrument=baba, price=ars(3645),
                   broker="IOL", commissions=ars(204.65))
    t60 = Purchase(date=date(2021, 1, 5), security_quantity=5, financial_instrument=gold, price=ars(3580),
                   broker="IOL", commissions=ars(125.63))
    t61 = StockDividend(date=date(2021, 1, 13), security_quantity=10.02, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(10.98))
    t62 = StockDividend(date=date(2021, 1, 13), security_quantity=3.58, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(3.92))
    t63 = Purchase(date=date(2021, 1, 22), security_quantity=391, financial_instrument=tgno4, price=ars(38.30),
                   broker="IOL", commissions=ars(105.10))
    t64 = Purchase(date=date(2021, 2, 1), security_quantity=25, financial_instrument=auy, price=ars(720),
                   broker="IOL", commissions=ars(126.32))
    t65 = Purchase(date=date(2021, 2, 8), security_quantity=8, financial_instrument=gold, price=ars(3400),
                   broker="IOL", commissions=ars(190.89))
    t66 = Purchase(date=date(2021, 2, 8), security_quantity=6, financial_instrument=gold, price=ars(3400),
                   broker="IOL", commissions=ars(143.17))
    t67 = Purchase(date=date(2021, 2, 8), security_quantity=8, financial_instrument=pfe, price=ars(2700),
                   broker="IOL", commissions=ars(151.59))
    t68 = StockDividend(date=date(2021, 2, 9), security_quantity=0.76, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(0.85))
    t69 = StockDividend(date=date(2021, 2, 9), security_quantity=2.12, financial_instrument=dollars,
                        referenced_financial_instrument=abev, broker="IOL", commissions=ars(2.39))
    t70 = Purchase(date=date(2021, 2, 9), security_quantity=3, financial_instrument=pfe, price=ars(2700),
                   broker="IOL", commissions=ars(56.85))
    t71 = StockDividend(date=date(2021, 2, 10), security_quantity=0.22, financial_instrument=dollars,
                        referenced_financial_instrument=auy, broker="IOL", commissions=ars(0.61))
    t72 = Sale(date=date(2021, 2, 17), security_quantity=17, financial_instrument=vist, price=ars(2340), broker="IOL",
               commissions=ars(279.17))
    t73 = CouponClipping(date=date(2021, 2, 17), security_quantity=28.80, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(9.46))
    t74 = CouponClipping(date=date(2021, 2, 17), security_quantity=29.03, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(9.53))
    t75 = CouponClipping(date=date(2021, 2, 17), security_quantity=14.11, financial_instrument=dollars,
                         referenced_financial_instrument=csdoo, broker="BALANZ", commissions=ars(4.63))
    t76 = Sale(date=date(2021, 2, 18), security_quantity=28, financial_instrument=arco, price=ars(1600), broker="IOL",
               commissions=ars(314.41))
    t77 = Sale(date=date(2021, 2, 18), security_quantity=2036, financial_instrument=tgno4, price=ars(44), broker="IOL",
               commissions=ars(628.70))
    t78 = Sale(date=date(2021, 2, 18), security_quantity=56, financial_instrument=ogzd, price=ars(450), broker="IOL",
               commissions=ars(176.85))
    t79 = Sale(date=date(2021, 2, 18), security_quantity=62415, financial_instrument=to21, price=ars(0.965),
               broker="IOL", commissions=ars(307.17))
    t80 = Sale(date=date(2021, 2, 18), security_quantity=76, financial_instrument=bma, price=ars(239.5), broker="IOL",
               commissions=ars(127.74))
    t81 = Sale(date=date(2021, 2, 18), security_quantity=11, financial_instrument=meli, price=ars(4535), broker="IOL",
               commissions=ars(350.10))
    t82 = CouponClipping(date=date(2021, 2, 22), security_quantity=7.7, financial_instrument=dollars,
                         referenced_financial_instrument=irc9o, broker="BALANZ",
                         commissions=ars(2.39))  # DÓLAR CABLE
    t83 = Purchase(date=date(2021, 2, 24), security_quantity=25, financial_instrument=abev, price=ars(1200),
                   broker="IOL", commissions=ars(210.54))
    t84 = Purchase(date=date(2021, 2, 24), security_quantity=10, financial_instrument=meli, price=ars(4160),
                   broker="IOL", commissions=ars(291.95))

    t85 = Purchase(date=date(2021, 2, 24), security_quantity=12, financial_instrument=arco, price=ars(1550),
                   broker="IOL", commissions=ars(130.53))
    t86 = Purchase(date=date(2021, 2, 24), security_quantity=2, financial_instrument=gold, price=ars(2937),
                   broker="IOL", commissions=ars(41.23))
    t87 = Purchase(date=date(2021, 3, 4), security_quantity=1, financial_instrument=meli, price=ars(3875),
                   broker="IOL", commissions=ars(27.20))
    t88 = StockDividend(date=date(2021, 3, 18), security_quantity=0.65, financial_instrument=dollars,
                        referenced_financial_instrument=gold, broker="IOL", commissions=ars(0.76))
    t89 = StockDividend(date=date(2021, 3, 18), security_quantity=0.47, financial_instrument=dollars,
                        referenced_financial_instrument=gold, broker="IOL", commissions=ars(0.55))
    t90 = StockDividend(date=date(2021, 3, 18), security_quantity=0.12, financial_instrument=dollars,
                        referenced_financial_instrument=gold, broker="IOL", commissions=ars(0.14))
    t91 = StockDividend(date=date(2021, 4, 8), security_quantity=0.67, financial_instrument=dollars,
                        referenced_financial_instrument=ko, broker="IOL", commissions=ars(0.80))
    t92 = StockDividend(date=date(2021, 4, 21), security_quantity=0.65, financial_instrument=dollars,
                        referenced_financial_instrument=auy, broker="IOL", commissions=ars(0.77))

    d1 = Inflow(date=date(2020, 1, 1), security_quantity=8498.30, financial_instrument=pesos, broker="IOL")  # Inicial
    d2 = Inflow(date=date(2020, 1, 6), security_quantity=20000, financial_instrument=pesos, broker="IOL")  # Depósito
    d3 = Inflow(date=date(2020, 1, 20), security_quantity=123.51, financial_instrument=pesos, broker="IOL")  # CAUCIÓN
    d4 = Inflow(date=date(2020, 2, 19), security_quantity=10000, financial_instrument=pesos, broker="IOL")  # Depósito
    d5 = Inflow(date=date(2020, 2, 27), security_quantity=40.61, financial_instrument=pesos, broker="IOL")  # CAUCIÓN
    d6 = Inflow(date=date(2020, 3, 1), security_quantity=20.81, financial_instrument=pesos,
                broker="IOL")  # Cuenta remunerada
    d7 = Inflow(date=date(2020, 3, 3), security_quantity=15000, financial_instrument=pesos, broker="IOL")  # Depósito
    d8 = Inflow(date=date(2020, 4, 1), security_quantity=26.81, financial_instrument=pesos,
                broker="IOL")  # Cuenta remunerada
    d9 = Inflow(date=date(2020, 4, 15), security_quantity=50000, financial_instrument=pesos, broker="IOL")  # Depósito
    d10 = Inflow(date=date(2020, 5, 1), security_quantity=82.09, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d11 = Inflow(date=date(2020, 5, 4), security_quantity=40000, financial_instrument=pesos, broker="IOL")  # Depósito
    d12 = Inflow(date=date(2020, 5, 5), security_quantity=10000, financial_instrument=pesos,
                 broker="BALANZ")  # Depósito
    d13 = Inflow(date=date(2020, 5, 7), security_quantity=70000, financial_instrument=pesos,
                 broker="BALANZ")  # Depósito
    d14 = Outflow(date=date(2020, 5, 14), security_quantity=11999.17, financial_instrument=pesos,
                  broker="IOL")  # Compra USD
    d15 = Outflow(date=date(2020, 5, 14), security_quantity=12118.73, financial_instrument=pesos,
                  broker="IOL")  # Extracción
    d16 = Inflow(date=date(2020, 5, 14), security_quantity=12000, financial_instrument=pesos, broker="IOL")  # Depósito
    d17 = Inflow(date=date(2020, 6, 1), security_quantity=64.22, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d18 = Inflow(date=date(2020, 6, 3), security_quantity=31000, financial_instrument=pesos, broker="IOL")  # Depósito
    d19 = Outflow(date=date(2020, 6, 22), security_quantity=58600, financial_instrument=pesos,
                  broker="IOL")  # Extracción
    d20 = Inflow(date=date(2020, 6, 22), security_quantity=30000, financial_instrument=pesos,
                 broker="BALANZ")  # Depósito
    d21 = Inflow(date=date(2020, 7, 1), security_quantity=50000, financial_instrument=pesos,
                 broker="BALANZ")  # Depósito
    d22 = Inflow(date=date(2020, 7, 1), security_quantity=30000, financial_instrument=pesos, broker="IOL")  # Depósito
    d23 = Inflow(date=date(2020, 7, 1), security_quantity=69.76, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d24 = Inflow(date=date(2020, 8, 1), security_quantity=80.85, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d25 = Inflow(date=date(2020, 8, 3), security_quantity=40000, financial_instrument=pesos, broker="IOL")  # Depósito
    d26 = Inflow(date=date(2020, 9, 1), security_quantity=25000, financial_instrument=pesos, broker="IOL")  # Depósito
    d27 = Inflow(date=date(2020, 9, 1), security_quantity=89.86, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d28 = Inflow(date=date(2020, 9, 23), security_quantity=134.01, financial_instrument=dollars,
                 broker="BALANZ")  # Depósito
    d29 = Inflow(date=date(2020, 10, 1), security_quantity=27.09, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d30 = Inflow(date=date(2020, 10, 30), security_quantity=40000, financial_instrument=pesos, broker="IOL")  # Depósito
    d31 = Inflow(date=date(2020, 10, 30), security_quantity=50000, financial_instrument=pesos,
                 broker="BALANZ")  # Depósito
    d32 = Inflow(date=date(2020, 11, 1), security_quantity=76.57, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d33 = Inflow(date=date(2020, 11, 2), security_quantity=25000, financial_instrument=pesos, broker="IOL")  # Depósito
    d34 = Inflow(date=date(2020, 11, 10), security_quantity=10000, financial_instrument=pesos, broker="IOL")  # Depósito
    d35 = Inflow(date=date(2020, 12, 1), security_quantity=116.61, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d36 = Inflow(date=date(2020, 12, 1), security_quantity=25000, financial_instrument=pesos, broker="IOL")  # Depósito
    d37 = Inflow(date=date(2020, 12, 9), security_quantity=15000, financial_instrument=pesos, broker="IOL")  # Depósito
    d38 = Inflow(date=date(2021, 1, 1), security_quantity=80.27, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d39 = Inflow(date=date(2021, 1, 4), security_quantity=50000, financial_instrument=pesos, broker="IOL")  # Depósito
    d40 = Inflow(date=date(2021, 1, 20), security_quantity=30000, financial_instrument=pesos, broker="IOL")  # Depósito
    d41 = Inflow(date=date(2021, 2, 1), security_quantity=304.59, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d42 = Inflow(date=date(2021, 2, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL")  # Cuenta remunerada
    d43 = Inflow(date=date(2021, 2, 2), security_quantity=50000, financial_instrument=pesos, broker="IOL")  # Depósito
    d44 = Inflow(date=date(2021, 2, 2), security_quantity=30000, financial_instrument=pesos, broker="IOL")  # Depósito
    d45 = Outflow(date=date(2021, 2, 22), security_quantity=328222, financial_instrument=pesos,
                  broker="IOL")  # Extracción
    d46 = Inflow(date=date(2021, 2, 24), security_quantity=100000, financial_instrument=pesos, broker="IOL")  # Depósito
    d47 = Inflow(date=date(2021, 3, 1), security_quantity=652.38, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d48 = Inflow(date=date(2021, 3, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL")  # Cuenta remunerada
    d49 = Inflow(date=date(2021, 4, 1), security_quantity=20.54, financial_instrument=pesos,
                 broker="IOL")  # Cuenta remunerada
    d50 = Inflow(date=date(2021, 4, 1), security_quantity=0.01, financial_instrument=dollars,
                 broker="IOL")  # Cuenta remunerada

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

    print("Saved all transactions")

    d12.save()
    d13.save()
    d20.save()
    d21.save()
    d28.save()
    d6.save()
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
    d14.save()
    d15.save()
    d16.save()
    d17.save()
    d18.save()
    d19.save()
    d22.save()
    d23.save()
    d24.save()
    d25.save()
    d26.save()
    d27.save()
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

    print("Saved all deposit/extractions")

    martin = InvestmentIndividualAccount.objects.create(description='Martín')
    pablo = InvestmentIndividualAccount.objects.create(description='Pablo')
    andres = InvestmentIndividualAccount.objects.create(description='Andrés')
    portfolio = InvestmentPortfolio.objects.create(description='Gotelli Ferenaz')

    portfolio.individual_accounts.add(martin)
    portfolio.individual_accounts.add(pablo)
    portfolio.individual_accounts.add(andres)

    print("Created accounts")

    martin.add_transaction(t1)
    martin.add_transaction(t2)
    martin.add_transaction(t3)
    martin.add_transaction(t4)
    martin.add_transaction(t5)
    martin.add_transaction(t6)
    martin.add_transaction(t7)
    martin.add_transaction(t8)
    martin.add_transaction(t9)
    martin.add_transaction(t10)
    martin.add_transaction(t11)
    martin.add_transaction(t12)
    martin.add_transaction(t13)
    martin.add_transaction(t14)
    martin.add_transaction(t15)
    martin.add_transaction(t16)
    martin.add_transaction(t17)
    pablo.add_transaction(t18)
    martin.add_transaction(t19)
    martin.add_transaction(t20)
    martin.add_transaction(t21)
    martin.add_transaction(t22)
    pablo.add_transaction(t23)
    martin.add_transaction(t24)
    martin.add_transaction(t25)
    martin.add_transaction(t26)
    martin.add_transaction(t27)
    martin.add_transaction(t28)
    martin.add_transaction(t29)
    martin.add_transaction(t30)
    martin.add_transaction(t31)
    martin.add_transaction(t32)
    martin.add_transaction(t33)
    martin.add_transaction(t34)
    martin.add_transaction(t35)
    martin.add_transaction(t36)
    martin.add_transaction(t37)
    martin.add_transaction(t38)
    martin.add_transaction(t39)
    pablo.add_transaction(t40)
    martin.add_transaction(t41)
    pablo.add_transaction(t42)
    martin.add_transaction(t43)
    martin.add_transaction(t44)
    martin.add_transaction(t45)
    martin.add_transaction(t46)
    martin.add_transaction(t47)
    andres.add_transaction(t48)
    andres.add_transaction(t49)
    andres.add_transaction(t50)
    martin.add_transaction(t51)
    martin.add_transaction(t52)
    martin.add_transaction(t53)
    martin.add_transaction(t54)
    martin.add_transaction(t55)
    martin.add_transaction(t56)
    martin.add_transaction(t57)
    andres.add_transaction(t58)
    martin.add_transaction(t59)
    martin.add_transaction(t60)
    martin.add_transaction(t61)
    andres.add_transaction(t62)
    martin.add_transaction(t63)
    martin.add_transaction(t64)
    andres.add_transaction(t65)
    martin.add_transaction(t66)
    martin.add_transaction(t67)
    andres.add_transaction(t68)
    martin.add_transaction(t69)
    martin.add_transaction(t70)
    martin.add_transaction(t71)
    martin.add_transaction(t72)
    martin.add_transaction(t73)
    pablo.add_transaction(t74)
    andres.add_transaction(t75)
    martin.add_transaction(t76)
    martin.add_transaction(t77)
    martin.add_transaction(t78)
    martin.add_transaction(t79)
    martin.add_transaction(t80)
    martin.add_transaction(t81)
    martin.add_transaction(t82)
    pablo.add_transaction(t83)
    pablo.add_transaction(t84)
    pablo.add_transaction(t85)
    pablo.add_transaction(t86)
    martin.add_transaction(t87)
    martin.add_transaction(t88)
    andres.add_transaction(t89)
    pablo.add_transaction(t90)
    andres.add_transaction(t91)
    martin.add_transaction(t92)

    print("Assigned all transactions")

    martin.add_transaction(d1)
    martin.add_transaction(d2)
    martin.add_transaction(d3)
    martin.add_transaction(d4)
    martin.add_transaction(d5)
    martin.add_transaction(d6)
    martin.add_transaction(d7)
    martin.add_transaction(d8)
    martin.add_transaction(d9)
    martin.add_transaction(d10)
    martin.add_transaction(d11)
    martin.add_transaction(d12)
    pablo.add_transaction(d13)
    martin.add_transaction(d14)
    martin.add_transaction(d15)
    martin.add_transaction(d16)
    martin.add_transaction(d17)
    martin.add_transaction(d18)
    martin.add_transaction(d19)
    martin.add_transaction(d20)
    martin.add_transaction(d21)
    martin.add_transaction(d22)
    martin.add_transaction(d23)
    martin.add_transaction(d24)
    martin.add_transaction(d25)
    martin.add_transaction(d26)
    martin.add_transaction(d27)
    martin.add_transaction(d28)
    martin.add_transaction(d29)
    andres.add_transaction(d30)
    andres.add_transaction(d31)
    martin.add_transaction(d32)
    martin.add_transaction(d33)
    martin.add_transaction(d34)
    martin.add_transaction(d35)
    martin.add_transaction(d36)
    martin.add_transaction(d37)
    martin.add_transaction(d38)
    martin.add_transaction(d39)
    martin.add_transaction(d40)
    martin.add_transaction(d41)
    martin.add_transaction(d42)
    martin.add_transaction(d43)
    andres.add_transaction(d44)
    martin.add_transaction(d45)
    pablo.add_transaction(d46)
    martin.add_transaction(d47)
    martin.add_transaction(d48)
    martin.add_transaction(d49)
    martin.add_transaction(d50)

    print("Assigned all deposit/extractions")
