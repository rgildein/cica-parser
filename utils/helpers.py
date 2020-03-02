def progress_bar_alive():
    """generator progress bar alive status"""
    options, i = ["|", "/", "─", "\\"], 0
    while True:
        yield options[i]
        i = (i+1)%4
