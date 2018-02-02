#!/usr/bin/python3

import os

def get_order_lines(filename):
    # "client_id": [list, of, orders_lines]
    orders = {}

    with open(filename, 'r') as input_file:
        for line in input_file:
            cols = line.strip().split(" ")
            order = {
                "product_number": cols[1],
                "quantity": int(cols[2]),
                "price": float(cols[3]),
            }

            taxes = ""
            if len(cols) >= 5:
                taxes = cols[4]
            order["taxes"] = taxes

            client_number = cols[0]

            client_orders = orders.get(client_number, [])
            client_orders.append(order)

            orders[client_number] = client_orders

    return orders


def create_bill(client_number, order_lines):
    grand_total = 0
    grand_total_with_rebate = 0
    number_of_products = 0

    for order_line in order_lines:
        product_price = order_line["price"]
        product_quantity = order_line["quantity"]

        order_line_total = product_price * product_quantity

        if "F" in order_line["taxes"]:
            order_line_total = order_line_total * 1.05
        if "P" in order_line["taxes"]:
            order_line_total = order_line_total * 1.0997

        order_line["total"] = order_line_total

        grand_total += order_line_total
        number_of_products += product_quantity

    rebate_multiplier = 1
    if number_of_products >= 100:
        rebate_multiplier = 0.85

    grand_total_with_rebate = grand_total * rebate_multiplier

    rebate = grand_total - grand_total_with_rebate


    bill = {
        "client_number": client_number,
        "grand_total": grand_total,
        "number_of_products": number_of_products,
        "order_lines": order_lines,
        "rebate": rebate,
        "grand_total_with_rebate": grand_total_with_rebate,
    }

    return bill


def print_bill_to_str(bill):
    bill_str = ""
    bill_str += "Client numéro {client_number}".format(
        client_number=bill["client_number"],
    )
    bill_str += "\n\n"
    bill_str += "\t\tNo de produit\tQte\tPrix\tTotal (tx)\n"

    order_lines = bill["order_lines"]


    for order_line_count in range(len(order_lines)):
        order_line = order_lines[order_line_count]

        bill_str += "Produit #{order_line_count}\t".format(
            order_line_count=order_line_count,
        )
        bill_str += "{product_number}\t".format(
            product_number=order_line["product_number"],
        )
        bill_str += "{quantity}\t".format(
            quantity=order_line["quantity"],
        )
        bill_str += "{price}\t".format(
            price="{0:.2f}".format(order_line["price"]),
        )
        bill_str += "{total}\t".format(
            total="{0:.2f}".format(order_line["total"]),
        )
        bill_str += "\n"

    bill_str += "\nTotal avant rabais: {total_avant_rabais}\n".format(
        total_avant_rabais="{0:.2f}".format(bill["grand_total"]),
    )
    bill_str += "Rabais: {rabais}\n".format(
        rabais="{0:.2f}".format(bill["rebate"]),
    )
    bill_str += "Total: {total}\n".format(
        total="{0:.2f}".format(bill["grand_total_with_rebate"]),
    )

    return bill_str


def create_bills(order_lines):
    bills = []
    for order_line in order_lines.items():
        bill = create_bill(order_line[0], order_line[1])
        bills.append(bill)
    return bills


def print_bills(bills):
    for bill in bills:
        bill_str = print_bill_to_str(bill)
        with open(bill["client_number"]+".txt", "w") as f:
            f.write(bill_str)

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(current_dir, "input.txt")

    order_lines = get_order_lines(input_file)
    bills = create_bills(order_lines)

    print_bills(bills)


if __name__ == "__main__":
    main()
