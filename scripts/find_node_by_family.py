
def find_family_node(data, family_name):
    if isinstance(data, list):
        for item in data:
            result = find_family_node(item, family_name)
            if result:
                return result
    elif isinstance(data, dict):
        if data.get("label") == "family" and data.get("name") == family_name:
            return data
        if "children" in data:
            return find_family_node(data["children"], family_name)
    return None