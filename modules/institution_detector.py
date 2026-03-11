from config.institution_keywords import all_institutions


def detect_institution(client_name):

    if not isinstance(client_name, str):
        return None

    client_lower = client_name.lower()

    for institution in all_institutions:
        if institution.lower() in client_lower:
            return institution

    return None

if __name__ == "__main__":
    test_client = "BlackRock Global Funds"
    result = detect_institution(test_client)

    print(result)