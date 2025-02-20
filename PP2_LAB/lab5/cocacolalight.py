import re
import json

with open("C:/Users/bolat/OneDrive/Desktop/PP2_LAB/lab5/cocacolazero.txt", "r", encoding="utf-8") as file:
    text = file.read()

receipt = {}


company = re.compile(r"Филиал (.+)")
bin = re.compile(r"БИН (\d+)")
vat= re.compile(r"НДС Серия (\d+)")
cash = re.compile(r"Касса (\d+-\d+)")
shift = re.compile(r"Смена (\d+)")
check= re.compile(r"Чек №(\d+)")
cashier = re.compile(r"Кассир (.+)\n")
items = re.compile(r"(\d+)\.\n(.+?)\n(\d+,\d{3}) x ([\d ]+),00\n([\d ]+),00")
total = re.compile(r"ИТОГО:\n([\d ]+),00")
vat = re.compile(r"в т.ч. НДС 12%:\n([\d ]+),00")
time= re.compile(r"Время: (.+)")
location= re.compile(r"г\. (.+),(.+), (.+)")

receipt["company"] = company.search(text).group(1)
receipt["BIN"] = bin.search(text).group(1)
receipt["VAT_Serial"] = vat.search(text).group(1)
receipt["Cash_Register"] = cash.search(text).group(1)
receipt["Shift"] = shift.search(text).group(1)
receipt["Check_Number"] = check.search(text).group(1)
receipt["Cashier"] = cashier.search(text).group(1)


itemsi = []
for item in items.findall(text):
    itemsi.append({
        "id": int(item[0]),
        "name": item[1].strip(),
        "quantity": float(item[2].replace(',', '.')),
        "unit_price": int(item[3].replace(' ', '')),
        "total_price": int(item[4].replace(' ', ''))
    })
receipt["items"] = itemsi


receipt["payment_method"] = "Банковская карта"
receipt["total"] = int(total.search(text).group(1).replace(' ', ''))
receipt["VAT"] = int(vat.search(text).group(1).replace(' ', ''))


receipt["timestamp"] = time.search(text).group(1)
receipt["location"] = location.search(text).groups()

with open( "C:/Users/bolat/OneDrive/Desktop/PP2_LAB/lab5/parsed_receipt.json", "w", encoding="utf-8") as json_file:
    json.dump(receipt, json_file, ensure_ascii=False, indent=4)

print(f"JSON-файл успешно создан: parsed_receipt.json")