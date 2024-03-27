from operations_with_files import search_file, transfer_file, filter_file
from utils import display_prompt

option_to_functionality_map = {
    "Search file": search_file,
    "Transfer file": transfer_file,
    "Filter file": filter_file
}


def display_prompt_messages():
    prompt_msg_list = [
        "Search file",
        "Transfer file",
        "Filter file",
        "Stop"
    ]

    while True:
        selected_option = display_prompt(prompt_msg_list)
        if selected_option == "Stop":
            break

        option_to_functionality_map[selected_option]()


if __name__ == "__main__":
    display_prompt_messages()
