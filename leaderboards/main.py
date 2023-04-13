import pandas as pd
import mysql.connector

# Conectar-se à base de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="myusualpasswordhere",
    database="chess"
)

# Executar uma consulta SQL
query = "SELECT username, elo_blitz FROM player ORDER BY elo_blitz DESC"
df1 = pd.read_sql(query, db)

query = "SELECT username, elo_bullet FROM player ORDER BY elo_bullet DESC"
df2 = pd.read_sql(query, db)

df1.index += 1
df2.index += 1

# Gerar o HTML para cada tabela
html1 = df1.to_html()
html2 = df2.to_html()

# Combinar os HTMLs em uma única string
html = f'<div style="display: inline-block; margin: 0 50px">{html1}</div><div style="display: inline-block; margin: 0 50px">{html2}</div>'

with open('tabela.html', 'w') as f:
    f.write(html)