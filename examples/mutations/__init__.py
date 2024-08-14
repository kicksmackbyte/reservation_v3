from pathlib import Path

DIR_PATH = Path(__file__).parent

mutations = []
for file_name in DIR_PATH.glob('*.gql'):

    operation_name = file_name.stem

    with open(file_name, 'r') as gql_file:

        mutation = gql_file.read().replace('\n', '')
        exec(f'{operation_name} = "{mutation}"')

        mutations.append(operation_name)

__all__ = tuple(mutations)
