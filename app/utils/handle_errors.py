def handle_errors(error):
    msg = str()
    status = False

    if type(error) == IOError:
        error_msg = "stocks object/file was not found or unable to retrieve"
    elif type(error) == IndexError:
        error_msg = "stock data input was unavailable or not found in Investing.com"
    elif type(error) == RuntimeError:
        error_msg = "stock data was not found"
    elif type(error) == ValueError:
        error_msg = "you have not registered anything"
    return status, error_msg
