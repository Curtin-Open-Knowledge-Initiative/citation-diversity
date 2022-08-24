import pyparsing as pp
import json
import pickle

from typing import Union, List, Dict, NamedTuple, AnyStr
from pathlib import Path

from precipy.analytics_function import AnalyticsFunction

from report_data_processing.sql import load_sql_to_string


def process_sql_to_queries(af: AnalyticsFunction,
                           parameters: dict,
                           rerun: bool,
                           sql_template_dir: Union[Path, str],
                           sql_processed_dir: Union[Path, str]):
    if not rerun:
        return
    sql_templates = sorted(Path(sql_template_dir).glob('*.sql'))
    jinja_templates = sorted(Path(sql_template_dir).glob('*.jinja2'))

    for template in sql_templates:
        try:
            query = load_sql_to_string(template.name,
                                       parameters=parameters,
                                       directory=sql_template_dir)
            filepath = Path(sql_processed_dir) / template.name
            with open(filepath, 'w') as f:
                f.write(query)
        except KeyError:  # Case for templates that need to be processed for each year
            for year in parameters.get('years'):
                parameters.update(dict(
                    year=year
                ))
                query = load_sql_to_string(template.name,
                                           parameters=parameters,
                                           directory=sql_template_dir)
                filepath = Path(sql_processed_dir) / f'{template.stem}_{year}{template.suffix}'
                with open(filepath, 'w') as f:
                    f.write(query)
            parameters.pop('year')

        # af.add_existing_file(filepath)


class Node(NamedTuple):
    name: str
    info: str = ''
    n_out: int = 0
    n_in: int = 0

    def __repr__(self):
        return self.name


class Edge(NamedTuple):
    from_node: str
    to_node: str


class Dag(object):
    def __init__(self,
                 nodes: dict = {},
                 edges: List[Edge] = []):
        self.nodes = nodes
        self.edges = edges

    def to_dict(self):
        return dict(
            nodes=[f'{node}' for node in self.nodes],
            edges=[[f'{edge.from_node}', f'{edge.to_node}'] for edge in self.edges]
        )

    def to_pickle(self,
                  filepath: Union[Path, str]):

        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        return True

    def to_json(self,
                filepath: Union[Path, str, None] = None):
        if filepath:
            with open(filepath, 'w') as f:
                dump = self.to_dict()
                json.dump(dump, f)
        else:
            return json.dumps(self.to_dict())

    def from_json(self,
                  filepath: Union[Path, str],
                  assert_empty: bool = True):
        with open(filepath) as f:
            j = json.load(f)

        if assert_empty:
            assert len(self.nodes) == 0
            assert len(self.edges) == 0

        self.nodes.update(j.get('nodes'))
        self.edges.extend(j.get('edges'))

    def edges_by_from_node(self,
                           from_node: Union[str, Node]):

        if type(from_node) == Node:
            from_node = from_node.name

        return [edge for edge in self.edges if edge[0] == from_node]

    def mermaid(self,
                github_string=True):
        mermaid_string = """
%%{ init: { "theme":"forest", "themeVariables": { "fontFamily" : "helvetica" }}}%%
graph LR
    classDef table   fill:#DDF,stroke:#000;
    classDef file    fill:#DFD,stroke:#000;
    classDef exec    fill:#FDD,stroke:#000;
    classDef default fill:#FFF,stroke:#000;
        
"""
        lines = []
        for a, b in self.edges:
            mermaid_string = mermaid_string + (f'  {self._mermaid_format_node(a)} --> {self._mermaid_format_node(b)}\n')

        if github_string:
            return f"""
```mermaid
{mermaid_string}
```
"""
        else:
            return mermaid_string

    def _mermaid_format_node(self, nd):
        puncmap = dict(
            table=('[(', ')]'),
            file=('{{', '}}'),
            exec=('(', ')')
        )
        node_type, body = nd.split('_')[0], '_'.join(nd.split('_')[1:])
        return f'{body}{puncmap.get(node_type)[0]}{body}{puncmap.get(node_type)[1]}:::{node_type}'

    def topologicalSortUtil(self, node, visited, stack):

        visited[node] = True

        # Recur for all the vertices adjacent to this vertex
        for to_node in [e.to_node for e in self.edges if e.from_node == node]:
            if visited[to_node] == False:
                self.topologicalSortUtil(to_node, visited, stack)

        # Push current vertex to stack which stores result
        stack.insert(0, node)

    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = {node: False for node in self.nodes}
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for node in self.nodes:
            if visited[node] == False:
                self.topologicalSortUtil(node, visited, stack)
        return stack


def build_sql_dag(sql_processed_dir: Union[Path, str]) -> Dag:
    dag = Dag()
    processed_sql = sorted(Path(sql_processed_dir).glob('*.sql'))

    heading_marker = pp.Literal('##')
    summary_head = heading_marker + pp.Literal('Summary') + pp.White()
    description_head = heading_marker + pp.Literal('Description') + pp.White()
    contacts_head = heading_marker + pp.Literal('Contacts') + pp.White()
    requires_head = heading_marker + pp.Literal('Requires') + pp.White()
    creates_head = heading_marker + pp.Literal('Creates') + pp.White()

    info_body = pp.ZeroOrMore(pp.Word(pp.alphas + pp.nums + '.@://{}_-;,()'))
    summary = summary_head.suppress() + pp.Combine(info_body, adjacent=False, join_string=" ").set_results_name(
        'summary')
    description = description_head + info_body.set_results_name('description')
    contacts = contacts_head + info_body.set_results_name('contacts')

    node_type = (pp.Literal('table') ^ pp.Literal('file')).set_results_name('type', list_all_matches=True)
    node_name = pp.Word(pp.alphas + pp.nums + '.@://{}_-').set_results_name('name', list_all_matches=True)
    reference = node_type + node_name
    references = pp.Group(reference).set_results_name('references', list_all_matches=True)
    requires = requires_head + pp.Group(references[...]).set_results_name('requires')
    creates = creates_head + pp.Group(references[...]).set_results_name('creates')

    info_section = summary ^ description ^ contacts ^ requires ^ creates

    info = pp.Literal('/*').suppress() + pp.Group(info_section[...]).set_results_name('info') + pp.Literal(
        '*/').suppress()

    for sql in processed_sql:

        sql_node_name = f'file_{sql}'
        if sql in dag.nodes.keys():
            raise ValueError('Reading the same sql file twice')

        try:
            parsed = info.parse_file(sql)
            sql_node = Node(name=sql_node_name,
                            info=parsed.info.summary)
            dag.nodes.update({sql_node_name: sql_node})

            dag.nodes.update(
                {f'{node_type}_{name}': Node(name) for node_type, name in parsed.info.creates}
            )
            dag.nodes.update(
                {f'{node_type}_{name}': Node(name) for node_type, name in parsed.info.requires}
            )

            dag.edges.extend(
                [Edge(f'{node_type}_{name}', sql_node_name) for node_type, name in parsed.info.requires]
            )
            dag.edges.extend(
                [Edge(sql_node_name, f'{node_type}_{name}') for node_type, name in parsed.info.creates]
            )

        except pp.exceptions.ParseException as e:
            print(e)
            print(f'Failed on {sql}')
            continue

    return dag


def dag_from_json(filepath):
    dag = Dag()
    dag.from_json(filepath)


def dag_from_pickle(filepath):
    with open(filepath, 'rb') as f:
        dag = pickle.load(f)
    return dag


if __name__ == '__main__':
    dag = build_sql_dag(Path('../../report_data_processing/sql_processed'))
    print(dag.mermaid())
    print(dag.topologicalSort())
