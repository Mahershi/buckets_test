import os
import json


def is_variable(value):
    return isinstance(value, str) and value.startswith("{") and value.endswith("}")


def message_matches(actual: dict, expected_template: dict) -> bool:
    for key, expected_value in expected_template.items():
        if key not in actual:
            return False
        actual_value = actual[key]
        if is_variable(expected_value):
            # It's a placeholder, we skip strict comparison
            continue
        if actual_value != expected_value:
            return False

    return True


def apply_params(obj, params: list[str]):
    if isinstance(obj, str):
        return obj.format(*params)
    elif isinstance(obj, dict):
        return {k: apply_params(v, params) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [apply_params(v, params) for v in obj]
    return obj


def load_template(key, params=[]):
    template = search_key(key, "../../src/constants/templates")
    return apply_params(template, params)


def search_key(key: str, dir: str):
    if not key or not dir:
        raise Exception(f"search_key Key or Dir not provided: key:{key}, dir:{dir}")

    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if key in data:
                            print(f"Found '{key}' in: {file_path}")
                            return data[key]
                except json.JSONDecodeError as e:
                    print(f"Skipping {file_path} due to JSON error: {e}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    print(f"Test key '{key}' not found in any JSON file.")
    raise Exception(f"search_key Key Not found in any json: key:{key}, dir:{dir}")


def json_inheritance_parser(child_dict: dict, dir: str, visited_keys=None) -> dict:
    """
    Recursively resolves inheritance if 'Inherits' key exists.
    Prevents circular dependencies using a visited_keys set.
    """
    def deep_merge(parent: dict, child: dict) -> dict:
        """Merge parent into child recursively (child has priority)."""
        result = parent.copy()
        for k, v in child.items():
            if k == "Inherits":
                continue  # Skip inheritance marker in final result
            if isinstance(v, dict) and isinstance(result.get(k), dict):
                result[k] = deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    if "Inherits" not in child_dict:
        return child_dict

    if visited_keys is None:
        visited_keys = set()

    parent_key = child_dict["Inherits"]

    if parent_key in visited_keys:
        raise Exception(f"Circular inheritance detected: {' -> '.join(visited_keys)} -> {parent_key}")

    visited_keys.add(parent_key)
    print(f"Inheriting from {parent_key}")

    parent_dict = search_key(parent_key, dir)
    parent_dict = json_inheritance_parser(parent_dict, dir, visited_keys)

    merged = deep_merge(parent_dict, child_dict)
    return merged