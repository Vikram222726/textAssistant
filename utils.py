def display_prompt(prompt_msg_list):
    while True:
        for msg_id in range(len(prompt_msg_list)):
            print(f"{msg_id+1}. {prompt_msg_list[msg_id]}")
        prompt_msg_id = input("Please enter the serial num of the option you want to select\n")
        if prompt_msg_id.isdigit():
            selected_prompt_msg_idx = int(prompt_msg_id) - 1
            if selected_prompt_msg_idx > len(prompt_msg_list):
                print("Invalid serial num selected, please retry")
                continue
            return prompt_msg_list[selected_prompt_msg_idx]
        else:
            print("Invalid option selected, please retry!")


def select_multiple_prompt_options(prompt_msg_list):
    while True:
        for msg_id in range(len(prompt_msg_list)):
            print(f"{msg_id+1}. {prompt_msg_list[msg_id]}")
        prompt_msg_str = input("Please enter space separated serial nums of the options you want to select\n")

        prompt_serial_num_list = prompt_msg_str.split(" ")
        prompt_msg_to_be_transferred_list = []

        for msg_serial_num in prompt_serial_num_list:
            if msg_serial_num.isdigit():
                if int(msg_serial_num) > len(prompt_msg_list):
                    print("Invalid serial number provided, please retry!")
                    continue

                prompt_msg_to_be_transferred_list.append(prompt_msg_list[int(msg_serial_num) - 1])

        if len(prompt_msg_to_be_transferred_list) == 0:
            print("No files selected, please retry!")
            continue

        return prompt_msg_to_be_transferred_list
