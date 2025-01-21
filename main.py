import sql_handler as sh

def main():
    e, c = sh.test_fuction()
    e(1)
    print(e.tables[0].get_column("ID"))

if __name__ == "__main__":
    main()