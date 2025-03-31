#!/bin/python3
import csv
from datetime import datetime
import argparse

def get_event(nominal):
    quantity = float(nominal.replace(",","."))
    if quantity >= 0:
        return "Buy"
    return "Sell"

def get_date(valuta):
    return datetime.strptime(valuta, "%d.%m.%Y").strftime("%Y-%m-%d")

def get_price(kurs):
    return kurs.replace(",",".")

def get_quantity(nominal):
    quantity = float(nominal.replace(",",".").replace("-",""))
    return quantity

def fix_header(file):
    with open(file, "r", encoding="ISO-8859-1") as file_reader:
        lines = file_reader.readlines()
    
    if lines:
        header_parts = lines[0].strip().split(";")
        
        if len(header_parts) >= 11 and header_parts[10] == "":
            header_parts[10] = "Currency"
            lines[0] = ";".join(header_parts) + "\n"
    
    with open(file, "w", encoding="ISO-8859-1") as file_writer:
        file_writer.writelines(lines)
    
def read_file(file):
    with open(file, mode="r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file, delimiter=";")  # Reads rows as dictionaries
        data = list(reader)  # Store all rows in memory
    return data

def convert_file(input_data, output_file):

    with open(output_file, "w") as file:
        # Rewrite the header line
        file.write("Event,Date,Symbol,Price,Quantity,Currency,FeeTax,Exchange,FeeCurrency,DoNotAdjustCash,Note\n")

        for row in data:
            event = get_event(row['Nominal'])
            date = get_date(row['Valuta'])
            stock_id = row['ISIN']
            price = get_price(row['Kurs'])
            quantity = get_quantity(row['Nominal'])
            currency = row['Currency']
            note = get_event(row['Nominal']) + " " + row['Bezeichnung']

            file.write(f"{event},{date},{stock_id},{price},{quantity},{currency},,,,{note}\n")


            
parser = argparse.ArgumentParser(description="Process CSV files for stock events.")
parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
parser.add_argument("-o", "--output", required=True, help="Output CSV file path")

# Parse the command-line arguments
args = parser.parse_args()

fix_header(args.input)
data = read_file(args.input)
convert_file(data, args.output)


print(f"Converting: {args.input} --> {args.output}")
print("Done!")
