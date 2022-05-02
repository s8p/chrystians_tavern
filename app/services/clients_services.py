from app.exceptions.client_exc import WrongKeys


def checking_keys(data: dict):
    box_flag = data.get("box_flag")

    if not box_flag:
        data["box_flag"] = box_flag
    else:
        data["box_flag"] = box_flag.capitalize()

    data["total_points"] = 0

    data_keys = set(data.keys())

    default_keys = ["cpf", "name", "email", "box_flag", "total_points"]
    default_keys = set(default_keys)

    if data_keys != default_keys:
        raise WrongKeys

    return data
