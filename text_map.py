def map_text_to_option(text, possible_options_list):
    try:
        possible_option_count = 1
        for possible_options in possible_options_list:
            for possible_text_field in possible_options:
                if possible_text_field.isdigit():
                    if possible_text_field == text:
                        return possible_option_count
                else:
                    if possible_text_field in text:
                        return possible_option_count
            possible_option_count += 1
    except Exception as e:
        print("Got error in map text to option with error", e)
    return -1
