from web import scrape
from model import query

def main():
    #scrape(["https://docs.datadoghq.com/intelligent_test_runner/"])
    response = query("Tell me all about intelligent datadog for tests")
    print(response)

if __name__ == "__main__":
    main()