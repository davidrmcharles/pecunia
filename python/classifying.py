'''
Transaction classification

* :func:`classify_interactively`
'''

# Standard imports:
import sys

# Project imports:
import formatting
import transactions


def classify_interactively(allTransactions, filteredTransactions):
    for index, transaction in enumerate(filteredTransactions):
        sys.stdout.write('''\
Classifying transaction %d of %d:

    ----------------------------------------------------------------------
''' % (index + 1, len(filteredTransactions)))
        sys.stdout.write('%s\n' % formatting.formatTransactionForDetail(transaction))
        sys.stdout.write('''\
    ----------------------------------------------------------------------

Each whitespace-delimited token is either a COMMAND or TAG to add to
this transaction.  Each token is processed in the order it appears.

To 'split' a transaction, append a colon and a dollar amount that
represents the amount associated with the tag.  For example:

    grocery cash:20.00

In the above example, $20.00 of the total amount is tagged as cash,
and the remaining balance of the transaction is tagged as grocery.

Here are the commands:

    !quit:  Quit without saving
    !save:  Save classification work to disk

You may also simply press ENTER to skip to the next transaction.

''')

        _handle_user_input(
            raw_input('>>> '),
            allTransactions,
            transaction)


def _handle_user_input(rawInput, allTransactions, transaction):
    tokens = rawInput.strip().split()
    for token in tokens:
        if token.lower() in ('!quit', '!exit'):
            raise SystemExit(0)
        elif token.lower() in ('!store', '!save'):
            transactions.store(allTransactions)
            sys.stdout.write(
                'Stored %d transcations to file "%s".\n' % (
                    len(allTransactions), transactions.database_path()))
        else:
            transaction.tags.update(_parseTag(token))


def _parse_tag(token):
    if ':' in token:
        tagName, tagAmount = token.split(':')
        return {tagName: float(tagAmount)}
    else:
        return {token: None}
