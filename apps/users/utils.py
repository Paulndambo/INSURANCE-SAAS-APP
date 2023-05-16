import os
def get_fake_emails() -> str:

    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.abspath(
        os.path.join(current_directory, os.pardir))
    file_path = os.path.join(parent_directory, "users",
                             "fake_email_domains_library.conf")
    with open(file_path) as fake_emails_list:
        return {line.rstrip() for line in fake_emails_list.readlines()}


def is_fake_email(email: str) -> bool:
    fake_list_content = get_fake_emails()
    return email.partition('@')[2] in fake_list_content
