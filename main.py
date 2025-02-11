import os
import mysql.connector
from colorama import Fore, init


init(autoreset=True)


ascii_art = """
.▄▄ · ▄• ▄▌▄• ▄▌ ▄▄▄·
▐█ ▀. █▪██▌█▪██▌▐█ ▄█
▄▀▀▀█▄█▌▐█▌█▌▐█▌ ██▀·
▐█▄▪▐█▐█▄█▌▐█▄█▌▐█▪·•
 ▀▀▀▀  ▀▀▀  ▀▀▀ .▀   
"""


def get_input(prompt):
    current_directory = os.getcwd().replace(os.path.expanduser("~"), "~")  
    user_name = os.getlogin()  
    prompt_str = f"""
┌──({user_name}@MysqlDump)─[{current_directory}]
 └─$ {Fore.MAGENTA}{prompt}{Fore.RESET}"""
    return input(prompt_str)


print(Fore.MAGENTA + ascii_art)


host = get_input("Entrez l'adresse ip de la base de données : ")
database = get_input("Entrez le nom de la base de données : ")
user = get_input("Entrez le nom d'utilisateur : ")
password = get_input("Entrez le mot de passe : ")


mysql_connection_string = {
    'host': host,
    'database': database,
    'user': user,
    'password': password
}


output_folder = "tables_sql"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


try:
    connection = mysql.connector.connect(**mysql_connection_string)
    print(Fore.MAGENTA + "\nConnexion réussie à la base de données MySQL!")
except mysql.connector.Error as error:
    print(Fore.MAGENTA + f"\nÉchec de la connexion à la base de données MySQL: {error}")
    exit(1)

cursor = connection.cursor()


cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
table_names = [table[0] for table in tables]

for table_name in table_names:
    sql_file_path = os.path.join(output_folder, f"{table_name}.sql")
    with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            values = ', '.join([f"'{str(value)}'" for value in row])
            insert_statement = f"INSERT INTO {table_name} VALUES ({values});\n"
            sql_file.write(insert_statement)

    print(Fore.MAGENTA + f"\nDonnées de la table '{table_name}' exportées dans le fichier '{sql_file_path}'")


cursor.close()
connection.close()
