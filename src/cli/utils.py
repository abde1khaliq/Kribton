def to_class_name(module_name: str) -> str:
    return module_name.replace("_", " ").title().replace(" ", "")