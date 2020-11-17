from model import investment_account, financial_instrument, transaction, measurement
from persistence import investment_account_persistence_manager
import datetime

pesos = financial_instrument.Currency('$', 'Pesos')
dollars = financial_instrument.Currency('U$D', 'Dólares EEUU')


def ars(amount):
    return measurement.Measurement(amount, pesos)


def usd(amount):
    return measurement.Measurement(amount, dollars)


def transactions():
    tb21 = financial_instrument.Bond('TB21', 'BONOS TES NAC EN PESOS BADLAR Privada + 100 pbs.',
                                     datetime.date(2021, 8, 5))
    tc20 = financial_instrument.Bond('TC20', 'BONCER 2020', datetime.date(2020, 4, 28))
    tj20 = financial_instrument.Bond('TJ20', 'BONOS DEL TESORO 2020', datetime.date(2020, 6, 21))
    to21 = financial_instrument.Bond('T021', 'BONTE 2021', datetime.date(2021, 10, 4))
    rpc4o = financial_instrument.Bond('RPC4O', 'IRSA CLASE IV', datetime.date(2020, 9, 14))
    irc1o = financial_instrument.Bond('IRC1O', 'IRSA 2020 U$S 10%', datetime.date(2020, 11, 16))
    csdoo = financial_instrument.Bond('CSDOO', 'CRESUD SACIF Y A 2023 U$S 6.5%', datetime.date(2023, 2, 16))
    irc9o = financial_instrument.Bond('IRC9O', 'IRSA CLASE IX', datetime.date(2023, 3, 1))
    mirg = financial_instrument.Stock("MIRG", "MIRGOR")
    bma = financial_instrument.Stock("BMA", "BANCO MACRO")
    tgno4 = financial_instrument.Stock("TGNO4", "TRANSPORTADORA GAS DEL NORTE")
    abev = financial_instrument.Stock("ABEV", "AMBEV")
    ogzd = financial_instrument.Stock("OGZD", "GAZPROM")
    arco = financial_instrument.Stock("ARCO", "ARCOS DORADOS")
    vist = financial_instrument.Stock("VIST", "VISTA OIL")
    ko = financial_instrument.Stock("KO", "COCA COLA")
    meli = financial_instrument.Stock("MELI", "MERCADO LIBRE")

    martin = investment_account.InvestmentIndividualAccount("Martín")
    pablo = investment_account.InvestmentIndividualAccount("Pablo")
    andres = investment_account.InvestmentIndividualAccount("Andrés")

    portfolio = investment_account.InvestmentPortfolio("Gotelli Ferenaz", [martin, pablo, andres])

    t1 = transaction.Purchase(datetime.date(2020, 1, 17), 20.7, mirg, ars(957.8792), "IOL", ars(139.15))
    t2 = transaction.Purchase(datetime.date(2020, 2, 13), 2, bma, ars(266.5), "IOL", ars(3.75))
    t3 = transaction.Purchase(datetime.date(2020, 2, 27), 41, bma, ars(244.9), "IOL", ars(70.46))
    t4 = transaction.Purchase(datetime.date(2020, 3, 3), 19164, tb21, ars(0.775), "IOL", ars(75.75))
    t5 = transaction.Purchase(datetime.date(2020, 3, 9), 6412, tc20, ars(2.28), "IOL", ars(74.4))
    t6 = transaction.Sale(datetime.date(2020, 3, 9), 19164, tb21, ars(0.792), "IOL", ars(77.41))
    t7 = transaction.Purchase(datetime.date(2020, 3, 10), 3411, tc20, ars(2.275), "IOL", ars(39.61))
    t8 = transaction.Purchase(datetime.date(2020, 3, 13), 3, bma, ars(182), "IOL", ars(3.83))
    t9 = transaction.Purchase(datetime.date(2020, 4, 3), 322, tj20, ars(0.62), "IOL", ars(1.02))
    t10 = transaction.Purchase(datetime.date(2020, 4, 16), 40540, tj20, ars(0.74), "IOL", ars(153))
    t11 = transaction.Purchase(datetime.date(2020, 4, 16), 26351, tj20, ars(0.74), "IOL", ars(99.45))
    t12 = transaction.CouponClipping(datetime.date(2020, 4, 28), 31303.45, pesos, tc20, "IOL", ars(3.48))
    t13 = transaction.Purchase(datetime.date(2020, 4, 29), 43013, to21, ars(0.724725), "IOL", ars(158.98))
    t14 = transaction.Purchase(datetime.date(2020, 5, 4), 1645, tgno4, ars(24.25), "IOL", ars(279.96))
    t15 = transaction.Sale(datetime.date(2020, 5, 5), 20.7, mirg, ars(670), "IOL", ars(97.34))
    t16 = transaction.Purchase(datetime.date(2020, 5, 6), 19402, to21, ars(0.67), "IOL", ars(66.3))
    t17 = transaction.Purchase(datetime.date(2020, 5, 6), 113, rpc4o, ars(87.50), "BALANZ", ars(59.43))
    t18 = transaction.Purchase(datetime.date(2020, 5, 11), 793, rpc4o, ars(87.936948), "BALANZ", ars(419.10))
    t19 = transaction.Sale(datetime.date(2020, 5, 12), 46, bma, ars(246), "IOL", ars(79.41))
    t20 = transaction.Purchase(datetime.date(2020, 6, 3), 12, abev, ars(935), "IOL", ars(78.75))
    t21 = transaction.Purchase(datetime.date(2020, 6, 3), 22, ogzd, ars(345), "IOL", ars(53.27))
    t22 = transaction.Purchase(datetime.date(2020, 6, 4), 11, arco, ars(1065), "IOL", ars(82.22))
    t23 = transaction.CouponClipping(datetime.date(2020, 6, 12), 1.42, dollars, rpc4o, "BALANZ", ars(0.36))
    t24 = transaction.CouponClipping(datetime.date(2020, 6, 12), 9.95, dollars, rpc4o, "BALANZ", ars(2.5))
    t25 = transaction.CouponClipping(datetime.date(2020, 6, 22), 73427.44, pesos, tj20, "IOL", ars(31.07))
    t26 = transaction.Purchase(datetime.date(2020, 6, 23), 360, csdoo, ars(82), "BALANZ", ars(177.42))
    t27 = transaction.Purchase(datetime.date(2020, 6, 24), 17, arco, ars(845), "IOL", ars(100.81))
    t28 = transaction.Purchase(datetime.date(2020, 7, 1), 34, ogzd, ars(290.5), "IOL", ars(69.32))
    t29 = transaction.Purchase(datetime.date(2020, 7, 6), 22, abev, ars(885), "IOL", ars(136.64))
    t30 = transaction.Purchase(datetime.date(2020, 7, 6), 544, csdoo, ars(92), "BALANZ", ars(300.79))
    t31 = transaction.Purchase(datetime.date(2020, 8, 5), 9, vist, ars(2150), "IOL", ars(135.8))
    t32 = transaction.Purchase(datetime.date(2020, 8, 5), 22, abev, ars(900), "IOL", ars(138.96))
    t33 = transaction.CouponClipping(datetime.date(2020, 8, 18), 29.18, dollars, csdoo, "BALANZ", ars(7.92))
    t34 = transaction.StockDividend(datetime.date(2020, 8, 21), 8.15, dollars, ogzd, "IOL", ars(7.65))
    t35 = transaction.StockDividend(datetime.date(2020, 8, 24), 262.12, pesos, arco, "IOL", ars(3.17))
    t36 = transaction.Purchase(datetime.date(2020, 9, 1), 49, bma, ars(241), "IOL", ars(82.88))
    t37 = transaction.Purchase(datetime.date(2020, 9, 1), 8, vist, ars(1850), "IOL", ars(103.87))
    t38 = transaction.Purchase(datetime.date(2020, 9, 14), 307, irc1o, usd(1.005), "BALANZ", ars(0.24) + usd(1.86))
    t39 = transaction.Sale(datetime.date(2020, 9, 14), 169, csdoo, usd(0.92), "BALANZ", ars(0.12) + usd(0.93))
    t40 = transaction.CouponClipping(datetime.date(2020, 9, 14), 114.45, dollars, rpc4o, "BALANZ", ars(0.40))
    t41 = transaction.CouponClipping(datetime.date(2020, 9, 14), 803.17, dollars, rpc4o, "BALANZ", ars(2.82))
    t42 = transaction.Purchase(datetime.date(2020, 9, 17), 889, csdoo, usd(0.9), "BALANZ", ars(0.61) + usd(4.80))
    t43 = transaction.Purchase(datetime.date(2020, 9, 23), 147, csdoo, usd(0.88), "BALANZ", ars(0.10) + usd(0.78))
    t44 = transaction.CouponClipping(datetime.date(2020, 10, 5), 5679.76, pesos, to21, "IOL", ars(28.40))
    t45 = transaction.Purchase(datetime.date(2020, 10, 8), 27, bma, ars(214), "IOL", ars(40.55))
    t46 = transaction.Outflow(datetime.date(2020, 10, 28), 307, irc1o, "BALANZ")
    t47 = transaction.Inflow(datetime.date(2020, 10, 28), 307, irc9o, "BALANZ")
    t48 = transaction.Purchase(datetime.date(2020, 10, 30), 13, ko, ars(1480), "IOL", ars(135.02))
    t49 = transaction.Purchase(datetime.date(2020, 10, 30), 20, abev, ars(1000), "IOL", ars(140.36))
    t50 = transaction.Purchase(datetime.date(2020, 10, 30), 432, csdoo, ars(115), "BALANZ", ars(298.58))
    t51 = transaction.Purchase(datetime.date(2020, 11, 2), 8, meli, ars(3100), "IOL", ars(174.05))
    t52 = transaction.Purchase(datetime.date(2020, 11, 10), 3, meli, ars(3130), "IOL", ars(65.90))
    t53 = transaction.CouponClipping(datetime.date(2020, 11, 16), 7.45, dollars, irc9o, "BALANZ", ars(2.23))
    t54 = transaction.CouponClipping(datetime.date(2020, 11, 16), 487.16, pesos, irc9o, "BALANZ", ars(0))

    d1 = transaction.Inflow(datetime.date(2020, 5, 5), 10000, pesos, "BALANZ")
    d2 = transaction.Inflow(datetime.date(2020, 5, 7), 70000, pesos, "BALANZ")
    d3 = transaction.Inflow(datetime.date(2020, 6, 22), 30000, pesos, "BALANZ")
    d4 = transaction.Inflow(datetime.date(2020, 7, 1), 50000, pesos, "BALANZ")
    d5 = transaction.Inflow(datetime.date(2020, 9, 23), 134.01, dollars, "BALANZ")
    d6 = transaction.Inflow(datetime.date(2020, 10, 30), 50000, pesos, "BALANZ")

    d7 = transaction.Inflow(datetime.date(2020, 1, 1), 8523.52, pesos, "IOL")  # Inicial
    d8 = transaction.Inflow(datetime.date(2020, 1, 6), 20000, pesos, "IOL")  # Depósito
    d9 = transaction.Inflow(datetime.date(2020, 1, 20), 123.51, pesos, "IOL")  # CAUCIÓN
    d10 = transaction.Inflow(datetime.date(2020, 2, 19), 10000, pesos, "IOL")  # Depósito
    d11 = transaction.Inflow(datetime.date(2020, 2, 27), 40.61, pesos, "IOL")  # CAUCIÓN
    d12 = transaction.Inflow(datetime.date(2020, 3, 1), 20.81, pesos, "IOL")  # Cuenta remunerada
    d13 = transaction.Inflow(datetime.date(2020, 3, 3), 15000, pesos, "IOL")  # Depósito
    d14 = transaction.Inflow(datetime.date(2020, 4, 1), 26.81, pesos, "IOL")  # Cuenta remunerada
    d15 = transaction.Inflow(datetime.date(2020, 4, 15), 50000, pesos, "IOL")  # Depósito
    d16 = transaction.Inflow(datetime.date(2020, 5, 1), 82.09, pesos, "IOL")  # Cuenta remunerada
    d17 = transaction.Inflow(datetime.date(2020, 5, 4), 40000, pesos, "IOL")  # Depósito
    d18 = transaction.Outflow(datetime.date(2020, 5, 14), 11999.17, pesos, "IOL")  # Compra USD
    d19 = transaction.Outflow(datetime.date(2020, 5, 14), 12118.73, pesos, "IOL")  # Extracción
    d20 = transaction.Inflow(datetime.date(2020, 5, 14), 12000, pesos, "IOL")  # Depósito
    d21 = transaction.Inflow(datetime.date(2020, 6, 1), 64.22, pesos, "IOL")  # Cuenta remunerada
    d22 = transaction.Inflow(datetime.date(2020, 6, 3), 31000, pesos, "IOL")  # Depósito
    d23 = transaction.Outflow(datetime.date(2020, 6, 22), 58600, pesos, "IOL")  # Extracción
    d24 = transaction.Inflow(datetime.date(2020, 7, 1), 30000, pesos, "IOL")  # Depósito
    d25 = transaction.Inflow(datetime.date(2020, 7, 1), 69.76, pesos, "IOL")  # Cuenta remunerada
    d26 = transaction.Inflow(datetime.date(2020, 8, 1), 80.85, pesos, "IOL")  # Cuenta remunerada
    d27 = transaction.Inflow(datetime.date(2020, 8, 3), 40000, pesos, "IOL")  # Depósito
    d28 = transaction.Inflow(datetime.date(2020, 9, 1), 25000, pesos, "IOL")  # Depósito
    d29 = transaction.Inflow(datetime.date(2020, 9, 1), 89.86, pesos, "IOL")  # Cuenta remunerada
    d30 = transaction.Inflow(datetime.date(2020, 10, 1), 27.09, pesos, "IOL")  # Cuenta remunerada
    d31 = transaction.Inflow(datetime.date(2020, 10, 30), 40000, pesos, "IOL")  # Depósito
    d32 = transaction.Inflow(datetime.date(2020, 11, 1), 76.57, pesos, "IOL")  # Cuenta remunerada
    d33 = transaction.Inflow(datetime.date(2020, 11, 2), 25000, pesos, "IOL")  # Depósito
    d34 = transaction.Inflow(datetime.date(2020, 11, 10), 10000, pesos, "IOL")  # Depósito

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
    martin.add_transaction(t23)
    pablo.add_transaction(t24)
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
    martin.add_transaction(t40)
    pablo.add_transaction(t41)
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

    martin.add_transaction(d1)
    pablo.add_transaction(d2)
    martin.add_transaction(d3)
    martin.add_transaction(d4)
    martin.add_transaction(d5)
    andres.add_transaction(d6)
    martin.add_transaction(d7)
    martin.add_transaction(d8)
    martin.add_transaction(d9)
    martin.add_transaction(d10)
    martin.add_transaction(d11)
    martin.add_transaction(d12)
    martin.add_transaction(d13)
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
    martin.add_transaction(d30)
    andres.add_transaction(d31)
    martin.add_transaction(d32)
    martin.add_transaction(d33)
    martin.add_transaction(d34)

    investment_account_persistence_manager.InvestmentAccountPersistenceManager().persist([portfolio])


if __name__ == '__main__':
    csdoo = financial_instrument.Bond('CSDOO', 'CRESUD SACIF Y A 2023 U$S 6.5%', datetime.date(2023, 2, 16))
    today = datetime.date.today()
    transactions()
    portfolio = investment_account_persistence_manager.InvestmentAccountPersistenceManager().retrieve()[0]
    #print(portfolio.balance_of_on(csdoo, today))
    #print(portfolio.individual_accounts[0].balances_on(today, "IOL"))
    print("Posición en IOL")
    print(portfolio.balances_on(today, "IOL"))
    print("")
    print("Posición en Balanz")
    print(portfolio.balances_on(today, "BALANZ"))
    #print(portfolio.individual_accounts[1].balances_on(today, "IOL"))

    #print(portfolio.individual_accounts[2].balances_on(today, "IOL"))
    print("")
    #print(portfolio.individual_accounts[2].balances_on(today))
    # print(portfolio.individual_accounts[0].transactions[0])
    # print(portfolio.individual_accounts[0].transactions[0].movements())
    # print(portfolio.individual_accounts[0].transactions[0].movements_in("BALANZ"))
