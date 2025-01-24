def burns_citation(title: str, date: str, identifier: str) -> str:
    """
    Citation for item at Burns

    :param title:
    :param date:
    :param identifier:
    :return:
    """
    return f'{title}, {date}, John J. Burns Library, Boston College, http://hdl.handle.net/2345.2/{identifier}.'


def law_citation(title: str, date: str, room: str, identifier: str) -> str:
    """
    Citation for item at Law Library

    :param title:
    :param date:
    :param room:
    :param identifier:
    :return:
    """
    return f'{title}, {date}, {room}, Daniel R. Coquillette Rare Book Room, Boston College Law Library, http://hdl.handle.net/2345.2/{identifier}.'
