"""Teacher integration example; in-memory single-process exercise, no concurrency."""


def find_book(catalog, book_id):
    """Return a detached book dict, or None. Do not expose the mutable original."""
    book = catalog.get(book_id)
    return dict(book) if book is not None else None


def borrow(catalog, loans, reader, book_id):
    """Valid nonempty reader/book IDs and a consistent catalog are preconditions."""
    book = catalog.get(book_id)
    if book is None:
        return 'not_found'
    if book['available'] <= 0:
        return 'unavailable'
    book['available'] -= 1
    key = (reader, book_id)
    loans[key] = loans.get(key, 0) + 1
    return 'ok'


def return_book(catalog, loans, reader, book_id):
    book = catalog.get(book_id)
    if book is None:
        return 'not_found'
    key = (reader, book_id)
    if loans.get(key, 0) == 0:
        return 'no_loan'
    book['available'] += 1
    if loans[key] == 1:
        del loans[key]
    else:
        loans[key] -= 1
    return 'ok'
