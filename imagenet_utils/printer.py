def print_results(results):
    output = ""
    for result in results:
        output += f"{result.wnid}: {result.words}\n"
    return output