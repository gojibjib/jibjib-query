from flask import jsonify

def response(status, message, count, data):
    """Returns a JSON encoded API response"""
    
    # return jsonify(status=status,
    #                message=message,
    #                count=count,
    #                data=data)

    return {
        "status": status,
        "message": message,
        "count": count,
        "data": data
    }, status