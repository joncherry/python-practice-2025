from ports import source
from adapters import nasdaq

def main():
    a = start(nasdaq.NasdaqData)
    print(a)

def start(sourceData: source.SourceData):
    a = sourceData.getZillowData()
    return a
    

if __name__ == "__main__":
    main()