from typing import List

from source.smwc.entry import Difficulty


def form_filter_params(
    name: str = None,
    authors: List[str] = None,
    tags: List[str] = None,
    demo: bool = None,
    featured: bool = None,
    difficulty: Difficulty = None,
    description: str = None,
) -> list:
    params = []

    if name is not None:
        params.append(f"f%5Bname%5D={name}")

    if authors is not None:
        params.append(form_filter_list_param("author", authors))

    if tags is not None:
        params.append(form_filter_list_param("tags", tags))

    if demo is not None:
        params.append(form_filter_bool_param("demo", demo))

    if featured is not None:
        params.append(form_filter_bool_param("featured", featured))

    if difficulty is not None:
        params.append(f"f%5Bdifficulty%5D%5B%5D={difficulty.value[1]}")

    if description is not None:
        params.append(f"f%5Bdescription%5D={description}")

    filter_params = "&".join(params).replace(" ", "+")
    if filter_params:
        filter_params = "&" + filter_params

    return filter_params


def form_filter_bool_param(name: str, value: bool) -> str:
    return f"f%5B{name}%5D={1 if value else 0}"


def form_filter_list_param(name: str, values: list) -> str:
    param = f"f%5B{name}%5D={values[0]}"

    if len(values) > 1:
        for value in values[1:]:
            param += f"%2C+{value}"

    return param
