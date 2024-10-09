

def create_response(data, message, status):
    return {
        "data": data,
        "message": message,
        "status": status
    }

def create_error_response(error, message, status):
    return {
        "error": error,
        "message": message,
        "status": status
    }