from connections import source
from connections import database

def main():
    sourceData = source.connection()
    a = sourceData.getHomePriceData()
    print(a)
    databaseData = database.connection()
    b = databaseData.getTableSingleRow("`sandboxproject2025.firsttest.testtable2`")
    print(b)

if __name__ == "__main__":
    main()