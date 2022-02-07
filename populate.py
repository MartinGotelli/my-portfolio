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

BALANZ = "BALANZ"

IOL = "IOL"

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
    User.objects.create_superuser('admin', 'admin@example.com', 'SuperUser3,14')


def create_transactions():
    t1 = Purchase.objects.create(date=date(2020, 1, 17), security_quantity=20.7, financial_instrument=mirg,
                                 price=ars(957.8792), broker=IOL, commissions=ars(139.15), account=martin)
    t2 = Purchase.objects.create(date=date(2020, 2, 13), security_quantity=2, financial_instrument=bma,
                                 price=ars(266.5),
                                 broker=IOL, commissions=ars(3.75), account=martin)
    t3 = Purchase.objects.create(date=date(2020, 2, 27), security_quantity=41, financial_instrument=bma,
                                 price=ars(244.9),
                                 broker=IOL, commissions=ars(70.46), account=martin)
    t4 = Purchase.objects.create(date=date(2020, 3, 3), security_quantity=19164, financial_instrument=tb21,
                                 price=ars(0.775),
                                 broker=IOL, commissions=ars(75.75), account=martin)
    t5 = Purchase.objects.create(date=date(2020, 3, 9), security_quantity=6412, financial_instrument=tc20,
                                 price=ars(2.275),
                                 broker=IOL, commissions=ars(74.4), account=martin)
    t6 = Sale.objects.create(date=date(2020, 3, 9), security_quantity=19164, financial_instrument=tb21,
                             price=ars(0.792), broker=IOL, commissions=ars(77.41), account=martin)
    t7 = Purchase.objects.create(date=date(2020, 3, 10), security_quantity=3411, financial_instrument=tc20,
                                 price=ars(2.277), broker=IOL, commissions=ars(39.61), account=martin)
    t8 = Purchase.objects.create(date=date(2020, 3, 13), security_quantity=3, financial_instrument=bma, price=ars(182),
                                 broker=IOL, commissions=ars(3.83), account=martin)
    t9 = Purchase.objects.create(date=date(2020, 4, 3), security_quantity=322, financial_instrument=tj20,
                                 price=ars(0.62), broker=IOL, commissions=ars(1.02), account=martin)
    t10 = Purchase.objects.create(date=date(2020, 4, 16), security_quantity=40540, financial_instrument=tj20,
                                  price=ars(0.74), broker=IOL, commissions=ars(153), account=martin)
    t11 = Purchase.objects.create(date=date(2020, 4, 16), security_quantity=26351, financial_instrument=tj20,
                                  price=ars(0.74), broker=IOL, commissions=ars(99.45), account=martin)
    t12 = CouponClipping.objects.create(date=date(2020, 4, 28), security_quantity=31303.45, financial_instrument=pesos,
                                        referenced_financial_instrument=tc20, broker=IOL, commissions=ars(3.48),
                                        account=martin)
    t13 = Purchase.objects.create(date=date(2020, 4, 29), security_quantity=43013, financial_instrument=to21,
                                  price=ars(0.724725), broker=IOL, commissions=ars(158.98), account=martin)
    t14 = Purchase.objects.create(date=date(2020, 5, 4), security_quantity=1645, financial_instrument=tgno4,
                                  price=ars(24.25), broker=IOL, commissions=ars(279.96), account=martin)
    t15 = Sale.objects.create(date=date(2020, 5, 5), security_quantity=20.7, financial_instrument=mirg, price=ars(670),
                              broker=IOL, commissions=ars(97.34), account=martin)
    t16 = Purchase.objects.create(date=date(2020, 5, 6), security_quantity=19402, financial_instrument=to21,
                                  price=ars(0.67), broker=IOL, commissions=ars(66.3), account=martin)
    t17 = Purchase.objects.create(date=date(2020, 5, 6), security_quantity=113, financial_instrument=rpc4o,
                                  price=ars(87.50), broker=BALANZ, commissions=ars(59.43), account=martin)
    t18 = Purchase.objects.create(date=date(2020, 5, 11), security_quantity=793, financial_instrument=rpc4o,
                                  price=ars(87.936948), broker=BALANZ, commissions=ars(419.10), account=pablo)
    t19 = Sale.objects.create(date=date(2020, 5, 12), security_quantity=46, financial_instrument=bma, price=ars(246),
                              broker=IOL, commissions=ars(79.41), account=martin)
    t20 = Purchase.objects.create(date=date(2020, 6, 3), security_quantity=12, financial_instrument=abev,
                                  price=ars(935), broker=IOL, commissions=ars(78.75), account=martin)
    t21 = Purchase.objects.create(date=date(2020, 6, 3), security_quantity=22, financial_instrument=ogzd,
                                  price=ars(345), broker=IOL, commissions=ars(53.27), account=martin)
    t22 = Purchase.objects.create(date=date(2020, 6, 4), security_quantity=11, financial_instrument=arco,
                                  price=ars(1065), broker=IOL, commissions=ars(82.22), account=martin)
    t23 = CouponClipping.objects.create(date=date(2020, 6, 12), security_quantity=9.95, financial_instrument=dollars,
                                        referenced_financial_instrument=rpc4o, broker=BALANZ, commissions=ars(2.5),
                                        account=pablo)
    t24 = CouponClipping.objects.create(date=date(2020, 6, 12), security_quantity=1.42, financial_instrument=dollars,
                                        referenced_financial_instrument=rpc4o, broker=BALANZ, commissions=ars(0.36),
                                        account=martin)
    t25 = CouponClipping.objects.create(date=date(2020, 6, 21), security_quantity=73427.44, financial_instrument=pesos,
                                        referenced_financial_instrument=tj20, broker=IOL, commissions=ars(31.07),
                                        account=martin)
    t26 = Purchase.objects.create(date=date(2020, 6, 23), security_quantity=360, financial_instrument=csdoo,
                                  price=ars(82), broker=BALANZ, commissions=ars(177.42), account=martin)
    t27 = Purchase.objects.create(date=date(2020, 6, 24), security_quantity=17, financial_instrument=arco,
                                  price=ars(845), broker=IOL, commissions=ars(100.81), account=martin)
    t28 = Purchase.objects.create(date=date(2020, 7, 1), security_quantity=34, financial_instrument=ogzd,
                                  price=ars(290.5), broker=IOL, commissions=ars(69.32), account=martin)
    t29 = Purchase.objects.create(date=date(2020, 7, 6), security_quantity=22, financial_instrument=abev,
                                  price=ars(885), broker=IOL, commissions=ars(136.64), account=martin)
    t30 = Purchase.objects.create(date=date(2020, 7, 6), security_quantity=544, financial_instrument=csdoo,
                                  price=ars(92), broker=BALANZ, commissions=ars(300.79), account=martin)
    t31 = Purchase.objects.create(date=date(2020, 8, 5), security_quantity=9, financial_instrument=vist,
                                  price=ars(2150), broker=IOL, commissions=ars(135.8), account=martin)
    t32 = Purchase.objects.create(date=date(2020, 8, 5), security_quantity=22, financial_instrument=abev,
                                  price=ars(900), broker=IOL, commissions=ars(138.96), account=martin)
    t33 = CouponClipping.objects.create(date=date(2020, 8, 18), security_quantity=29.18, financial_instrument=dollars,
                                        referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(7.92),
                                        account=martin)
    t34 = StockDividend.objects.create(date=date(2020, 8, 21), security_quantity=8.15, financial_instrument=dollars,
                                       referenced_financial_instrument=ogzd, broker=IOL, commissions=ars(7.65),
                                       account=martin)
    t35 = StockDividend.objects.create(date=date(2020, 8, 24), security_quantity=262.12, financial_instrument=pesos,
                                       referenced_financial_instrument=arco, broker=IOL, commissions=ars(3.17),
                                       account=martin)
    t36 = Purchase.objects.create(date=date(2020, 9, 1), security_quantity=49, financial_instrument=bma, price=ars(241),
                                  broker=IOL, commissions=ars(82.88), account=martin)
    t37 = Purchase.objects.create(date=date(2020, 9, 1), security_quantity=8, financial_instrument=vist,
                                  price=ars(1850), broker=IOL, commissions=ars(103.87), account=martin)
    t38 = Purchase.objects.create(date=date(2020, 9, 14), security_quantity=307, financial_instrument=irc1o,
                                  price=usd(1.005), broker=BALANZ, commissions=ars(0.24) + usd(1.86), account=martin)
    t39 = Sale.objects.create(date=date(2020, 9, 14), security_quantity=169, financial_instrument=csdoo,
                              price=usd(0.92), broker=BALANZ, commissions=ars(0.12) + usd(0.93), account=martin)
    t40 = CouponClipping.objects.create(date=date(2020, 9, 14), security_quantity=803.17, financial_instrument=dollars,
                                        referenced_financial_instrument=rpc4o, broker=BALANZ, commissions=ars(2.82),
                                        account=pablo)
    t41 = CouponClipping.objects.create(date=date(2020, 9, 14), security_quantity=114.45, financial_instrument=dollars,
                                        referenced_financial_instrument=rpc4o, broker=BALANZ, commissions=ars(0.40),
                                        account=martin)
    t42 = Purchase.objects.create(date=date(2020, 9, 17), security_quantity=889, financial_instrument=csdoo,
                                  price=usd(0.9), broker=BALANZ, commissions=ars(0.61) + usd(4.80), account=pablo)
    t43 = Purchase.objects.create(date=date(2020, 9, 23), security_quantity=147, financial_instrument=csdoo,
                                  price=usd(0.88), broker=BALANZ, commissions=ars(0.10) + usd(0.78), account=martin)
    t44 = CouponClipping.objects.create(date=date(2020, 10, 5), security_quantity=5679.76, financial_instrument=pesos,
                                        referenced_financial_instrument=to21, broker=IOL, commissions=ars(28.40),
                                        account=martin)
    t45 = Purchase.objects.create(date=date(2020, 10, 8), security_quantity=27, financial_instrument=bma,
                                  price=ars(214), broker=IOL, commissions=ars(40.55), account=martin)
    t46 = Sale.objects.create(date=date(2020, 10, 28), security_quantity=307, financial_instrument=irc1o,
                              price=usd(1.005),
                              broker=BALANZ, account=martin)
    t47 = Purchase.objects.create(date=date(2020, 10, 28), security_quantity=307, financial_instrument=irc9o,
                                  price=usd(1.005),
                                  broker=BALANZ, account=martin)
    t48 = Purchase.objects.create(date=date(2020, 10, 30), security_quantity=13, financial_instrument=ko,
                                  price=ars(1480),
                                  broker=IOL, commissions=ars(135.02), account=andres)
    t49 = Purchase.objects.create(date=date(2020, 10, 30), security_quantity=20, financial_instrument=abev,
                                  price=ars(1000),
                                  broker=IOL, commissions=ars(140.36), account=andres)
    t50 = Purchase.objects.create(date=date(2020, 10, 30), security_quantity=432, financial_instrument=csdoo,
                                  price=ars(115),
                                  broker=BALANZ, commissions=ars(298.58), account=andres)
    t51 = Purchase.objects.create(date=date(2020, 11, 2), security_quantity=8, financial_instrument=meli,
                                  price=ars(3100),
                                  broker=IOL, commissions=ars(174.05), account=martin)
    t52 = Purchase.objects.create(date=date(2020, 11, 10), security_quantity=3, financial_instrument=meli,
                                  price=ars(3130),
                                  broker=IOL, commissions=ars(65.90), account=martin)
    t53 = CouponClipping.objects.create(date=date(2020, 11, 16), security_quantity=460.64, financial_instrument=pesos,
                                        referenced_financial_instrument=irc9o, broker=BALANZ, commissions=ars(0),
                                        account=martin)
    t54 = CouponClipping.objects.create(date=date(2020, 11, 16), security_quantity=5.91, financial_instrument=dollars,
                                        referenced_financial_instrument=irc9o, broker=BALANZ, commissions=ars(2.23),
                                        account=martin)
    t55 = Purchase.objects.create(date=date(2020, 12, 1), security_quantity=13, financial_instrument=auy,
                                  price=ars(800),
                                  broker=IOL, commissions=ars(72.99), account=martin)
    t56 = Purchase.objects.create(date=date(2020, 12, 1), security_quantity=3, financial_instrument=baba,
                                  price=ars(4400),
                                  broker=IOL, commissions=ars(92.64), account=martin)
    t57 = Purchase.objects.create(date=date(2020, 12, 9), security_quantity=4, financial_instrument=baba,
                                  price=ars(4200),
                                  broker=IOL, commissions=ars(117.90), account=martin)
    t58 = StockDividend.objects.create(date=date(2020, 12, 17), security_quantity=0.65, financial_instrument=dollars,
                                       referenced_financial_instrument=ko, broker=IOL, commissions=ars(0.69),
                                       account=andres)
    t59 = Purchase.objects.create(date=date(2021, 1, 4), security_quantity=8, financial_instrument=baba,
                                  price=ars(3645),
                                  broker=IOL, commissions=ars(204.65), account=martin)
    t60 = Purchase.objects.create(date=date(2021, 1, 5), security_quantity=5, financial_instrument=gold,
                                  price=ars(3580),
                                  broker=IOL, commissions=ars(125.63), account=martin)
    t61 = StockDividend.objects.create(date=date(2021, 1, 13), security_quantity=10.02, financial_instrument=dollars,
                                       referenced_financial_instrument=abev, broker=IOL, commissions=ars(10.98),
                                       account=martin)
    t62 = StockDividend.objects.create(date=date(2021, 1, 13), security_quantity=3.58, financial_instrument=dollars,
                                       referenced_financial_instrument=abev, broker=IOL, commissions=ars(3.92),
                                       account=andres)
    t63 = Purchase.objects.create(date=date(2021, 1, 22), security_quantity=391, financial_instrument=tgno4,
                                  price=ars(38.30),
                                  broker=IOL, commissions=ars(105.10), account=martin)
    t64 = Purchase.objects.create(date=date(2021, 2, 1), security_quantity=25, financial_instrument=auy, price=ars(720),
                                  broker=IOL, commissions=ars(126.32), account=martin)
    t65 = Purchase.objects.create(date=date(2021, 2, 8), security_quantity=8, financial_instrument=gold,
                                  price=ars(3400),
                                  broker=IOL, commissions=ars(190.89), account=andres)
    t66 = Purchase.objects.create(date=date(2021, 2, 8), security_quantity=6, financial_instrument=gold,
                                  price=ars(3400),
                                  broker=IOL, commissions=ars(143.17), account=martin)
    t67 = Purchase.objects.create(date=date(2021, 2, 8), security_quantity=8, financial_instrument=pfe, price=ars(2700),
                                  broker=IOL, commissions=ars(151.59), account=martin)
    t68 = StockDividend.objects.create(date=date(2021, 2, 9), security_quantity=0.76, financial_instrument=dollars,
                                       referenced_financial_instrument=abev, broker=IOL, commissions=ars(0.85),
                                       account=andres)
    t69 = StockDividend.objects.create(date=date(2021, 2, 9), security_quantity=2.12, financial_instrument=dollars,
                                       referenced_financial_instrument=abev, broker=IOL, commissions=ars(2.39),
                                       account=martin)
    t70 = Purchase.objects.create(date=date(2021, 2, 9), security_quantity=3, financial_instrument=pfe, price=ars(2700),
                                  broker=IOL, commissions=ars(56.85), account=martin)
    t71 = StockDividend.objects.create(date=date(2021, 2, 10), security_quantity=0.22, financial_instrument=dollars,
                                       referenced_financial_instrument=auy, broker=IOL, commissions=ars(0.61),
                                       account=martin)
    t72 = Sale.objects.create(date=date(2021, 2, 17), security_quantity=17, financial_instrument=vist, price=ars(2340),
                              broker=IOL, commissions=ars(279.17), account=martin)
    t73 = CouponClipping.objects.create(date=date(2021, 2, 17), security_quantity=28.80, financial_instrument=dollars,
                                        referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(9.46),
                                        account=martin)
    t74 = CouponClipping.objects.create(date=date(2021, 2, 17), security_quantity=29.02, financial_instrument=dollars,
                                        referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(9.53),
                                        account=pablo)
    t75 = CouponClipping.objects.create(date=date(2021, 2, 17), security_quantity=14.11, financial_instrument=dollars,
                                        referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(4.63),
                                        account=andres)
    t76 = Sale.objects.create(date=date(2021, 2, 18), security_quantity=28, financial_instrument=arco, price=ars(1600),
                              broker=IOL, commissions=ars(314.41), account=martin)
    t77 = Sale.objects.create(date=date(2021, 2, 18), security_quantity=2036, financial_instrument=tgno4, price=ars(44),
                              broker=IOL, commissions=ars(628.70), account=martin)
    t78 = Sale.objects.create(date=date(2021, 2, 18), security_quantity=56, financial_instrument=ogzd, price=ars(450),
                              broker=IOL, commissions=ars(176.85), account=martin)
    t79 = Sale.objects.create(date=date(2021, 2, 18), security_quantity=62415, financial_instrument=to21,
                              price=ars(0.965), broker=IOL, commissions=ars(307.17), account=martin)
    t80 = Sale.objects.create(date=date(2021, 2, 18), security_quantity=76, financial_instrument=bma, price=ars(239.5),
                              broker=IOL, commissions=ars(127.74), account=martin)
    t81 = Sale.objects.create(date=date(2021, 2, 18), security_quantity=11, financial_instrument=meli, price=ars(4535),
                              broker=IOL, commissions=ars(350.10), account=martin)
    t82 = CouponClipping.objects.create(date=date(2021, 2, 22), security_quantity=7.7, financial_instrument=dollars,
                                        referenced_financial_instrument=irc9o, broker=BALANZ, commissions=ars(2.39),
                                        account=martin)  # DÓLAR CABLE
    t83 = Purchase.objects.create(date=date(2021, 2, 24), security_quantity=25, financial_instrument=abev,
                                  price=ars(1200),
                                  broker=IOL, commissions=ars(210.54), account=pablo)
    t84 = Purchase.objects.create(date=date(2021, 2, 24), security_quantity=10, financial_instrument=meli,
                                  price=ars(4160),
                                  broker=IOL, commissions=ars(291.95), account=pablo)
    t85 = Purchase.objects.create(date=date(2021, 2, 24), security_quantity=12, financial_instrument=arco,
                                  price=ars(1550),
                                  broker=IOL, commissions=ars(130.53), account=pablo)
    t86 = Purchase.objects.create(date=date(2021, 2, 24), security_quantity=2, financial_instrument=gold,
                                  price=ars(2937),
                                  broker=IOL, commissions=ars(41.23), account=pablo)
    t87 = Purchase.objects.create(date=date(2021, 3, 4), security_quantity=1, financial_instrument=meli,
                                  price=ars(3875),
                                  broker=IOL, commissions=ars(27.20), account=martin)
    t88 = StockDividend.objects.create(date=date(2021, 3, 18), security_quantity=0.65, financial_instrument=dollars,
                                       referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.76),
                                       account=martin)
    t89 = StockDividend.objects.create(date=date(2021, 3, 18), security_quantity=0.47, financial_instrument=dollars,
                                       referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.55),
                                       account=andres)
    t90 = StockDividend.objects.create(date=date(2021, 3, 18), security_quantity=0.12, financial_instrument=dollars,
                                       referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.14),
                                       account=pablo)
    t91 = StockDividend.objects.create(date=date(2021, 4, 8), security_quantity=0.67, financial_instrument=dollars,
                                       referenced_financial_instrument=ko, broker=IOL, commissions=ars(0.80),
                                       account=andres)
    t92 = StockDividend.objects.create(date=date(2021, 4, 21), security_quantity=0.65, financial_instrument=dollars,
                                       referenced_financial_instrument=auy, broker=IOL, commissions=ars(0.77),
                                       account=martin)
    t93 = Purchase.objects.create(date=date(2021, 4, 30), security_quantity=16, financial_instrument=intc,
                                  price=ars(1828), broker=IOL, commissions=ars(205.26), account=martin)
    t94 = Purchase.objects.create(date=date(2021, 4, 30), security_quantity=27, financial_instrument=auy,
                                  price=ars(725), broker=IOL, commissions=ars(137.38), account=martin)
    t95 = Purchase.objects.create(date=date(2021, 5, 6), security_quantity=22, financial_instrument=spot,
                                  price=ars(1315), broker=IOL, commissions=ars(203.03), account=pablo)
    t96 = Purchase.objects.create(date=date(2021, 5, 6), security_quantity=12, financial_instrument=meli,
                                  price=ars(3875), broker=IOL, commissions=ars(326.34), account=pablo)
    t97 = Purchase.objects.create(date=date(2021, 5, 6), security_quantity=1000, financial_instrument=ptsto,
                                  price=ars(155), broker=BALANZ, commissions=ars(931.55), account=pablo)
    t98 = Sale.objects.create(date=date(2021, 6, 1), security_quantity=20, financial_instrument=abev, price=ars(1835),
                              broker=IOL, commissions=ars(257.56), account=andres)
    t99 = Sale.objects.create(date=date(2021, 6, 1), security_quantity=25, financial_instrument=abev, price=ars(1835),
                              broker=IOL, commissions=ars(321.95), account=pablo)
    t100 = Sale.objects.create(date=date(2021, 6, 1), security_quantity=20, financial_instrument=abev, price=ars(1835),
                               broker=IOL, commissions=ars(257.56), account=martin)
    t101 = Sale.objects.create(date=date(2021, 6, 2), security_quantity=36, financial_instrument=abev, price=ars(1850),
                               broker=IOL, commissions=ars(467.40), account=martin)
    t102 = Purchase.objects.create(date=date(2021, 6, 2), security_quantity=8, financial_instrument=tsla,
                                   price=ars(6710), broker=IOL, commissions=ars(376.72), account=martin)
    t103 = Purchase.objects.create(date=date(2021, 6, 2), security_quantity=210, financial_instrument=teco2,
                                   price=ars(190.25), broker=IOL, commissions=ars(280.38), account=martin)
    t104 = Purchase.objects.create(date=date(2021, 6, 2), security_quantity=16, financial_instrument=meli,
                                   price=ars(3750), broker=IOL, commissions=ars(421.08), account=pablo)
    t105 = Purchase.objects.create(date=date(2021, 6, 2), security_quantity=3, financial_instrument=trip,
                                   price=ars(3525), broker=IOL, commissions=ars(74.22), account=pablo)
    t106 = Purchase.objects.create(date=date(2021, 6, 2), security_quantity=11, financial_instrument=trip,
                                   price=ars(3525), broker=IOL, commissions=ars(272.12), account=andres)
    t107 = StockDividend.objects.create(date=date(2021, 6, 2), security_quantity=0.68, financial_instrument=dollars,
                                        referenced_financial_instrument=intc, broker=IOL, commissions=ars(0.82),
                                        account=martin)
    t108 = Purchase.objects.create(date=date(2021, 6, 4), security_quantity=581, financial_instrument=cp21o,
                                   price=usd(1), broker=BALANZ, commissions=ars(0), account=martin)
    t109 = StockDividend.objects.create(date=date(2021, 6, 7), security_quantity=1.32, financial_instrument=dollars,
                                        referenced_financial_instrument=pfe, broker=IOL, commissions=ars(1.60),
                                        account=martin)
    t110 = StockDividend.objects.create(date=date(2021, 6, 23), security_quantity=0.65, financial_instrument=dollars,
                                        referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.79),
                                        account=martin)
    t111 = StockDividend.objects.create(date=date(2021, 6, 23), security_quantity=0.47, financial_instrument=dollars,
                                        referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.57),
                                        account=andres)
    t112 = StockDividend.objects.create(date=date(2021, 6, 23), security_quantity=0.12, financial_instrument=dollars,
                                        referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.14),
                                        account=pablo)
    t113 = StockDividend.objects.create(date=date(2021, 6, 23), security_quantity=1.55, financial_instrument=dollars,
                                        referenced_financial_instrument=gold, broker=IOL, commissions=ars(1.88),
                                        account=martin)
    t114 = StockDividend.objects.create(date=date(2021, 6, 23), security_quantity=1.12, financial_instrument=dollars,
                                        referenced_financial_instrument=gold, broker=IOL, commissions=ars(1.36),
                                        account=andres)
    t115 = StockDividend.objects.create(date=date(2021, 6, 23), security_quantity=0.28, financial_instrument=dollars,
                                        referenced_financial_instrument=gold, broker=IOL, commissions=ars(0.34),
                                        account=pablo)
    t116 = StockDividend.objects.create(date=date(2021, 7, 7), security_quantity=0.67, financial_instrument=dollars,
                                        referenced_financial_instrument=ko, broker=IOL, commissions=ars(0.82),
                                        account=andres)
    t117 = StockDividend.objects.create(date=date(2021, 7, 15), security_quantity=1.12, financial_instrument=dollars,
                                        referenced_financial_instrument=auy, broker=IOL, commissions=ars(1.37),
                                        account=martin)
    t118 = CouponClipping.objects.create(date=date(2021, 7, 26), security_quantity=36.74, financial_instrument=dollars,
                                         referenced_financial_instrument=ptsto, broker=BALANZ, commissions=ars(12.44),
                                         account=martin)  # DÓLAR CABLE
    t119 = StockDividend.objects.create(date=date(2021, 7, 30), security_quantity=1.96, financial_instrument=dollars,
                                        referenced_financial_instrument=arco, broker=IOL, commissions=ars(0.61),
                                        account=pablo)
    t120 = Purchase.objects.create(date=date(2021, 8, 18), security_quantity=14, financial_instrument=abev,
                                   price=ars(1600), broker=IOL, commissions=ars(157.20), account=martin)
    t121 = Purchase.objects.create(date=date(2021, 8, 18), security_quantity=33, financial_instrument=gd30,
                                   price=ars(0), broker=IOL, commissions=ars(0.61), account=martin)
    t122 = Purchase.objects.create(date=date(2021, 8, 18), security_quantity=16, financial_instrument=gd35,
                                   price=ars(0), broker=IOL, commissions=ars(0.61), account=martin)
    t123 = CouponClipping.objects.create(date=date(2021, 8, 18), security_quantity=28.32, financial_instrument=dollars,
                                         referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(1.17),
                                         account=martin)
    t124 = CouponClipping.objects.create(date=date(2021, 8, 18), security_quantity=13.87, financial_instrument=dollars,
                                         referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(4.98),
                                         account=andres)
    t125 = CouponClipping.objects.create(date=date(2021, 8, 18), security_quantity=28.55, financial_instrument=dollars,
                                         referenced_financial_instrument=csdoo, broker=BALANZ, commissions=ars(10.25),
                                         account=pablo)
    t126 = CouponClipping.objects.create(date=date(2021, 8, 19), security_quantity=7.70, financial_instrument=dollars,
                                         referenced_financial_instrument=irc9o, broker=BALANZ, commissions=ars(2.63),
                                         account=martin)  # DÓLAR CABLE
    t127 = Purchase.objects.create(date=date(2021, 8, 25), security_quantity=11, financial_instrument=baba,
                                   price=ars(3360), broker=IOL, commissions=ars(258.99), account=martin)
    t128 = Purchase.objects.create(date=date(2021, 8, 25), security_quantity=12, financial_instrument=baba,
                                   price=ars(3275), broker=IOL, commissions=ars(275.81), account=martin)
    t129 = Purchase.objects.create(date=date(2021, 8, 26), security_quantity=165, financial_instrument=csdoo,
                                   price=ars(167.5), broker=BALANZ, commissions=ars(166.11), account=pablo)

    print("Saved all transactions")

    d1 = Inflow.objects.create(date=date(2020, 1, 1), security_quantity=8498.30, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Inicial
    d2 = Inflow.objects.create(date=date(2020, 1, 6), security_quantity=20000, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Depósito
    d3 = Inflow.objects.create(date=date(2020, 1, 20), security_quantity=123.51, financial_instrument=pesos, broker=IOL,
                               account=martin)  # CAUCIÓN
    d4 = Inflow.objects.create(date=date(2020, 2, 19), security_quantity=10000, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Depósito
    d5 = Inflow.objects.create(date=date(2020, 2, 27), security_quantity=40.61, financial_instrument=pesos, broker=IOL,
                               account=martin)  # CAUCIÓN
    d6 = Inflow.objects.create(date=date(2020, 3, 1), security_quantity=20.81, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Cuenta remunerada
    d7 = Inflow.objects.create(date=date(2020, 3, 3), security_quantity=15000, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Depósito
    d8 = Inflow.objects.create(date=date(2020, 4, 1), security_quantity=26.81, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Cuenta remunerada
    d9 = Inflow.objects.create(date=date(2020, 4, 15), security_quantity=50000, financial_instrument=pesos, broker=IOL,
                               account=martin)  # Depósito
    d10 = Inflow.objects.create(date=date(2020, 5, 1), security_quantity=82.09, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d11 = Inflow.objects.create(date=date(2020, 5, 4), security_quantity=40000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d12 = Inflow.objects.create(date=date(2020, 5, 5), security_quantity=10000, financial_instrument=pesos,
                                broker=BALANZ, account=martin)  # Depósito
    d13 = Inflow.objects.create(date=date(2020, 5, 7), security_quantity=70000, financial_instrument=pesos,
                                broker=BALANZ, account=pablo)  # Depósito
    d14 = Outflow.objects.create(date=date(2020, 5, 14), security_quantity=11999.17, financial_instrument=pesos,
                                 broker=IOL, account=martin)  # Compra USD
    d15 = Outflow.objects.create(date=date(2020, 5, 14), security_quantity=12118.73, financial_instrument=pesos,
                                 broker=IOL, account=martin)  # Extracción
    d16 = Inflow.objects.create(date=date(2020, 5, 14), security_quantity=12000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d17 = Inflow.objects.create(date=date(2020, 6, 1), security_quantity=64.22, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d18 = Inflow.objects.create(date=date(2020, 6, 3), security_quantity=31000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d19 = Outflow.objects.create(date=date(2020, 6, 22), security_quantity=58600, financial_instrument=pesos,
                                 broker=IOL, account=martin)  # Extracción
    d20 = Inflow.objects.create(date=date(2020, 6, 22), security_quantity=30000, financial_instrument=pesos,
                                broker=BALANZ, account=martin)  # Depósito
    d21 = Inflow.objects.create(date=date(2020, 7, 1), security_quantity=50000, financial_instrument=pesos,
                                broker=BALANZ, account=martin)  # Depósito
    d22 = Inflow.objects.create(date=date(2020, 7, 1), security_quantity=30000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d23 = Inflow.objects.create(date=date(2020, 7, 1), security_quantity=69.76, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d24 = Inflow.objects.create(date=date(2020, 8, 1), security_quantity=80.85, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d25 = Inflow.objects.create(date=date(2020, 8, 3), security_quantity=40000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d26 = Inflow.objects.create(date=date(2020, 9, 1), security_quantity=25000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d27 = Inflow.objects.create(date=date(2020, 9, 1), security_quantity=89.86, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d28 = Inflow.objects.create(date=date(2020, 9, 23), security_quantity=134.01, financial_instrument=dollars,
                                broker=BALANZ, account=martin)  # Depósito
    d29 = Inflow.objects.create(date=date(2020, 10, 1), security_quantity=27.09, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d30 = Inflow.objects.create(date=date(2020, 10, 30), security_quantity=40000, financial_instrument=pesos,
                                broker=IOL, account=andres)  # Depósito
    d31 = Inflow.objects.create(date=date(2020, 10, 30), security_quantity=50000, financial_instrument=pesos,
                                broker=BALANZ, account=andres)  # Depósito
    d32 = Inflow.objects.create(date=date(2020, 11, 1), security_quantity=76.57, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d33 = Inflow.objects.create(date=date(2020, 11, 2), security_quantity=25000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d34 = Inflow.objects.create(date=date(2020, 11, 10), security_quantity=10000, financial_instrument=pesos,
                                broker=IOL, account=martin)  # Depósito
    d35 = Inflow.objects.create(date=date(2020, 12, 1), security_quantity=116.61, financial_instrument=pesos,
                                broker=IOL, account=martin)  # Cuenta remunerada
    d36 = Inflow.objects.create(date=date(2020, 12, 1), security_quantity=25000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d37 = Inflow.objects.create(date=date(2020, 12, 9), security_quantity=15000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d38 = Inflow.objects.create(date=date(2021, 1, 1), security_quantity=80.27, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d39 = Inflow.objects.create(date=date(2021, 1, 4), security_quantity=50000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d40 = Inflow.objects.create(date=date(2021, 1, 20), security_quantity=30000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d41 = Inflow.objects.create(date=date(2021, 2, 1), security_quantity=304.59, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d42 = Inflow.objects.create(date=date(2021, 2, 1), security_quantity=0.01, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d43 = Inflow.objects.create(date=date(2021, 2, 2), security_quantity=50000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d44 = Inflow.objects.create(date=date(2021, 2, 2), security_quantity=30000, financial_instrument=pesos, broker=IOL,
                                account=andres)  # Depósito
    d45 = Outflow.objects.create(date=date(2021, 2, 22), security_quantity=328222, financial_instrument=pesos,
                                 broker=IOL, account=martin)  # Extracción
    d46 = Inflow.objects.create(date=date(2021, 2, 24), security_quantity=100000, financial_instrument=pesos,
                                broker=IOL, account=pablo)  # Depósito
    d47 = Inflow.objects.create(date=date(2021, 3, 1), security_quantity=652.38, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d48 = Inflow.objects.create(date=date(2021, 3, 1), security_quantity=0.01, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d49 = Inflow.objects.create(date=date(2021, 4, 1), security_quantity=20.54, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d50 = Inflow.objects.create(date=date(2021, 4, 1), security_quantity=0.01, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d51 = Inflow.objects.create(date=date(2021, 4, 30), security_quantity=50000, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Depósito
    d52 = Inflow.objects.create(date=date(2021, 5, 1), security_quantity=37.44, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d53 = Inflow.objects.create(date=date(2021, 5, 1), security_quantity=0.01, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d54 = Inflow.objects.create(date=date(2021, 5, 6), security_quantity=185000, financial_instrument=pesos,
                                broker=BALANZ, account=pablo)  # Depósito
    d55 = Inflow.objects.create(date=date(2021, 5, 6), security_quantity=100000, financial_instrument=pesos, broker=IOL,
                                account=pablo)  # Depósito
    d56 = Inflow.objects.create(date=date(2021, 6, 1), security_quantity=822.86, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d57 = Inflow.objects.create(date=date(2021, 6, 1), security_quantity=0.01, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d58 = Inflow.objects.create(date=date(2021, 6, 3), security_quantity=849.40, financial_instrument=dollars,
                                broker=BALANZ, account=martin)  # Depósito
    d59 = Inflow.objects.create(date=date(2021, 7, 1), security_quantity=266.79, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d60 = Inflow.objects.create(date=date(2021, 7, 1), security_quantity=0.01, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d61 = Inflow.objects.create(date=date(2021, 8, 1), security_quantity=147.73, financial_instrument=pesos, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d62 = Inflow.objects.create(date=date(2021, 8, 1), security_quantity=0.02, financial_instrument=dollars, broker=IOL,
                                account=martin)  # Cuenta remunerada
    d63 = Inflow.objects.create(date=date(2021, 8, 17), security_quantity=100000, financial_instrument=pesos,
                                broker=IOL, account=martin)  # Depósito

    print("Saved all deposit/extractions")


if __name__ == '__main__':
    create_admin()
    pesos = Currency.objects.create(code='$', description='Pesos')
    dollars = Currency.objects.create(code='USD', description='Dólares EEUU')
    dollars_link = Currency.objects.create(code='USD C', description='Dólares EEUU - Cable')
    mirg = Stock.objects.create(code="MIRG", description="MIRGOR")
    tb21 = Bond.objects.create(code='TB21', description='BONOS TES NAC EN PESOS BADLAR Privada + 100 pbs.',
                               maturity_date=date(2021, 8, 5), price_each_quantity=100)
    tc20 = Bond.objects.create(code='TC20', description='BONCER 2020', maturity_date=date(2020, 4, 28),
                               price_each_quantity=100)
    tj20 = Bond.objects.create(code='TJ20', description='BONOS DEL TESORO 2020', maturity_date=date(2020, 6, 21),
                               price_each_quantity=100)
    to21 = Bond.objects.create(code='TO21', description='BONTE 2021', maturity_date=date(2021, 10, 4),
                               price_each_quantity=100)
    rpc4o = Bond.objects.create(code='RPC4O', description='IRSA CLASE IV', maturity_date=date(2020, 9, 14))
    irc1o = Bond.objects.create(code='IRC1O', description='IRSA 2020 U$S 10%', maturity_date=date(2020, 11, 16))
    csdoo = Bond.objects.create(code='CSDOO', description='CRESUD SACIF Y A 2023 U$S 6.5%',
                                maturity_date=date(2023, 2, 16))
    irc9o = Bond.objects.create(code='IRC9O', description='IRSA CLASE IX', maturity_date=date(2023, 3, 1))
    bma = Stock.objects.create(code="BMA", description="BANCO MACRO")
    tgno4 = Stock.objects.create(code="TGNO4", description="TRANSPORTADORA GAS DEL NORTE")
    abev = Stock.objects.create(code="ABEV", description="AMBEV")
    ogzd = Stock.objects.create(code="OGZD", description="GAZPROM")
    arco = Stock.objects.create(code="ARCO", description="ARCOS DORADOS")
    vist = Stock.objects.create(code="VIST", description="VISTA OIL")
    ko = Stock.objects.create(code="KO", description="COCA COLA")
    meli = Stock.objects.create(code="MELI", description="MERCADO LIBRE")
    auy = Stock.objects.create(code="AUY", description="YAMANA GOLD")
    baba = Stock.objects.create(code="BABA", description="ALI BABA")
    gold = Stock.objects.create(code="GOLD", description="GOLD")
    pfe = Stock.objects.create(code="PFE", description="PFEIZER")
    intc = Stock.objects.create(code="INTC", description="INTEL")
    ptsto = Bond.objects.create(code='PTSTO', description='ON PETROBRAS ARG REGS 7,375%',
                                maturity_date=date(2023, 7, 21))
    spot = Stock.objects.create(code='SPOT', description='SPOTIFY')
    tsla = Stock.objects.create(code='TSLA', description='TESLA')
    teco2 = Stock.objects.create(code='TECO2', description='TELECOM')
    trip = Stock.objects.create(code='TRIP', description='TRIP ADVISOR')
    cp21o = Bond.objects.create(code='CP21O', description='ON CIA GRAL.COMBUS. CL21 V.10/06/23 U$S',
                                maturity_date=date(2023, 6, 10))
    gd30 = Bond.objects.create(code='GD30', description='Bonos Rep. Arg. U$S Step Up V.09/07/30',
                               maturity_date=date(2030, 7, 9), price_each_quantity=100)
    gd35 = Bond.objects.create(code='GD35', description='Bonos Rep. Arg. U$S Step Up V.09/07/35',
                               maturity_date=date(2035, 7, 9), price_each_quantity=100)

    print("Created instruments")

    martin = InvestmentIndividualAccount.objects.create(description='Martín')
    pablo = InvestmentIndividualAccount.objects.create(description='Pablo')
    andres = InvestmentIndividualAccount.objects.create(description='Andrés')
    portfolio = InvestmentPortfolio.objects.create(description='Gotelli Ferenaz')

    portfolio.individual_accounts.add(martin)
    portfolio.individual_accounts.add(pablo)
    portfolio.individual_accounts.add(andres)

    print("Created accounts")

    # create_transactions()
