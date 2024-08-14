from pathlib import Path

DIR_PATH = Path(__file__).parent

queries = []
for file_name in DIR_PATH.glob('*.gql'):

    operation_name = file_name.stem

    with open(file_name, 'r') as gql_file:

        query = gql_file.read().replace('\n', '')
        exec(f'{operation_name} = "{query}"')

        queries.append(operation_name)

__all__ = tuple(queries)
