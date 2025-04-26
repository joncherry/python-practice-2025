from connections import externalsource
from connections import database

def main():
    sourceData = externalsource.connection()
    a = sourceData.getHomePriceData()
    print(a)
    databaseData = database.connection()
    b = databaseData.getTableSingleRow("`sandboxproject2025.firsttest.testtable2`")
    print(b)

if __name__ == "__main__":
    main()