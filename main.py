from pycoingecko import CoinGeckoAPI
from csv import writer
import pandas as pd
import os

cg = CoinGeckoAPI()

totalBal = 0
loadFromFile = True
count = 0

def collectCrypto():
    cryptos = []
    crypto_names = []
    print("Input the cryptocurrency then how much you have.")
    print('Type "STOP" to halt the crypto-balance loop')
    while True:
        crypto = input("Crypto: ")
        if crypto == "STOP":
            break
        bal = float(input("Balance: "))
        if cryptos != []:
            for i in cryptos:
                if i[0] == crypto:
                    print("Adding",bal,crypto,"to your original",i[1],crypto)
                    i[1] = i[1] + bal
                else: # an error around here, can't figure out where
                    global count
                    count += 1
                    if count == len(cryptos):
                        cryptos.append([crypto, bal])
                        crypto_names.append(crypto)
                        count = 0
                        break
        else:
            cryptos.append([crypto, bal])
            crypto_names.append(crypto)
    return cryptos, crypto_names

def collectPrices(crypto_names, cryptos, loadFromFile):
    global totalBal
    getPrices = cg.get_price(ids=crypto_names, vs_currencies='gbp')
    priceOfHeldCrypto = []
    priceOfCrypto = []
    percDiff = []
    for i in cryptos:
        price = getPrices[i[0]]["gbp"]
        total = i[1] * price
        priceOfHeldCrypto.append(total)
        priceOfCrypto.append(price)
        if loadFromFile == True:
            percDiff.append(((total/i[2])-1)*100)
        else:
            percDiff.append(0)
        print("Total", i[0], "=", i[1], "@", price, "=", total)
        totalBal = totalBal + total
    return totalBal, priceOfHeldCrypto, priceOfCrypto, percDiff

def csvSaver(cryptos, priceOfHeldCrypto, totalBal, priceOfCrypto, percDiff, csvFileName):
    coins = []
    qty = []
    for i in cryptos:
        coins.append(i[0])
        qty.append(i[1])
    dict = {"Cryptos": coins, "Quantity": qty, "Price at time": priceOfCrypto, "Value of held crypto": priceOfHeldCrypto, "Percentage difference": percDiff}
    df = pd.DataFrame(dict)
    df.to_csv(csvFileName)
    contents = ["","Balance:",totalBal]
    append_list_as_row(csvFileName, contents)
    print("Exported to", csvFileName)

def csvChecker(csvFileName):
    if csvFileName[-4:] != ".csv":
        csvFileName = csvFileName + ".csv"
    return csvFileName

def append_list_as_row(file_name, list_of_elements):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elements)

def main(csvFileName, crypto_names, cryptos, loadFromFile):
    totalBal, priceOfHeldCrypto, priceOfCrypto, percDiff = collectPrices(crypto_names, cryptos, loadFromFile)
    print("Your total balance is", totalBal)
    csvSaver(cryptos, priceOfHeldCrypto, totalBal, priceOfCrypto, percDiff, csvFileName)

def newUser():
    question = input("Do you want to retrieve previous cryptocurrency data? (y/n) ")
    global loadFromFile
    if question == "y":
        files = os.listdir()
        print("Here is a list of all the files in this directory:")
        for f in files:
            print(f)
        csvFileName = input("Please enter the file name for your csv file containing the relevant cryptocurrency data.\n")
        csvFileName = csvChecker(csvFileName)
        data = pd.read_csv(csvFileName)
        data = data.iloc[:-1]
        df = pd.DataFrame(data, columns= ['Cryptos', 'Quantity','Value of held crypto'])
        cryptos = df.to_numpy()
        global crypto_names
        crypto_names = []
        for i in cryptos:
            crypto_names.append(i[0])
    elif question == "n":
        csvFileName = input ("Please enter the name that you want this file to be called.\n")
        csvFileName = csvChecker(csvFileName)
        cryptos, crypto_names = collectCrypto()
        loadFromFile = False
    return csvFileName, crypto_names, cryptos, loadFromFile

if __name__ == "__main__":
    csvFileName, crypto_names, cryptos, loadFromFile = newUser()
    main(csvFileName, crypto_names, cryptos, loadFromFile)

