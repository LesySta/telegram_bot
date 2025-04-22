def filter_http_loop(string_list):
    filtered_strings = []
    for s in string_list:
        if s.startswith("http://"):
            filtered_strings.append(s)
    return filtered_strings

strings = ["http://example.com", "ftp://another.site", "http://google.com", "some text", "http://another.url"]
filtered_strings = filter_http_loop(strings)
print(filtered_strings)

empty_list = []
print(filter_http_loop(empty_list))