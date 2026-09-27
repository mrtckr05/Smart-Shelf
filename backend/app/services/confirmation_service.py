from collections import Counter

from app.models import Observation


CONFIRMATION_SAMPLES = 5


def get_consensus(
    counts_list: list[dict[str, int]]
) -> dict[str, int]:

    product_quantities: dict[str, list[int]] = {}

    for counts in counts_list:

        for class_name, quantity in counts.items():

            product_quantities.setdefault(
                class_name,
                []
            ).append(quantity)

    consensus = {}

    for class_name, quantities in product_quantities.items():

        vote = Counter(
            quantities
        ).most_common(1)[0][0]

        consensus[class_name] = vote

    return consensus