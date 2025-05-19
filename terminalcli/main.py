import sys
import requests


class BadStatusCodeException(Exception):
    """got a non 200 status code in response"""

def main():
    if len(sys.argv) < 2:
        print(
            """\
commands available are:
    authorize
    clear_authorization {session_id}
    revoke_authorization {session_id}
    home_and_hay_report {session_id}
    amazon_report {session_id}
    motorola_report {session_id}

            """
        )
        return
    match sys.argv[1]:
        case "authorize":
            authorize()
        case "clear_authorization":
            clear_auth()
        case "revoke_authorization":
            revoke_auth()
        case "home_and_hay_report":
            get_home_and_hay_report()
        case "amazon_report":
            get_amazon_report()
        case "motorola_report":
            get_motorola_report()

    print("finished")


local_session_cache = {}


def authorize():
    url = "http://localhost:8080/authorize"
    print(make_request(url))


def clear_auth():
    if len(sys.argv) < 3:
        print("missing session_id arg")
        return
    session_id = sys.argv[2]
    url = "http://localhost:8080/clear"
    print(make_request(url, session_id=session_id))


def revoke_auth():
    if len(sys.argv) < 3:
        print("missing session_id arg")
        return
    session_id = sys.argv[2]
    url = "http://localhost:8080/revoke"
    print(make_request(url, session_id=session_id))


def get_home_and_hay_report():
    if len(sys.argv) < 3:
        print("missing session_id arg")
        return
    session_id = sys.argv[2]
    url = "http://localhost:8080/home_and_hay_data"
    print(make_request(url, session_id=session_id))


def get_amazon_report():
    if len(sys.argv) < 3:
        print("missing session_id arg")
        return
    session_id = sys.argv[2]
    url = "http://localhost:8080/amazon_data"
    print(make_request(url, session_id=session_id))


def get_motorola_report():
    if len(sys.argv) < 3:
        print("missing session_id arg")
        return
    session_id = sys.argv[2]
    url = "http://localhost:8080/motorola_data"
    print(make_request(url, session_id=session_id))


def make_request(url: str, session_id=None):
    response = requests.get(url, headers={"SESSION-ID":session_id}, timeout=300)
    if response.status_code != 200:
        raise BadStatusCodeException(f"status code was {response.status_code}")
    return response.text


if __name__ == "__main__":
    main()
