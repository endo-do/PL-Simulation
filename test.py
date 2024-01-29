from Table import Table

PL_Teams = ["Liverpool","Man City","Arsenal","Aston Villa","Tottenham","West Ham","Brighton","ManUnited","Chelsea"]

League = Table([[i, 0] for i in PL_Teams])

League.display()

League.remove_column(-1)

League.add_row(0, ["Nottingham"])

League.display()

League.add_column(1, ["active" for i in League.get_content()])

for i in range(3, 6):
    League.replace_cell(i, -1, "inactive")

League.display()

for i in League.get_content().copy():
    if i[-1] == "inactive":
        League.remove_row(League.get_content().index(i))

League.conf_header("row", "add", ["#default"])

League.display()

League.replace_content([[1, 2, 3, 4], [5, 6, 7, 8]])

print(League.content)

League.display()