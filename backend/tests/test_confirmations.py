from app.services.confirmation_service import get_consensus


def test_get_consensus():

    counts_list = [
        {
            "pen": 5,
            "cup": 2
        },
        {
            "pen": 5,
            "cup": 2
        },
        {
            "pen": 4,
            "cup": 2
        },
        {
            "pen": 5,
            "cup": 3
        },
        {
            "pen": 4,
            "cup": 2
        }
    ]

    result = get_consensus(counts_list)

    assert result == {
        "pen": 5,
        "cup": 2
    }

def test_get_consensus_ignores_missing_product():

    counts_list = [
        {
            "pen": 5,
            "cup": 2
        },
        {
            "pen": 5
        },
        {
            "pen": 5,
            "cup": 2
        },
        {
            "pen": 4
        },
        {
            "pen": 5,
            "cup": 2
        }
    ]

    result = get_consensus(counts_list)

    assert result == {
        "pen": 5,
        "cup": 2
    }