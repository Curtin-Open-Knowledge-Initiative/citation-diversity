import pyparsing as pp

from typing import Union, List, Dict, NamedTuple, AnyStr
from pathlib import Path

from precipy.analytics_function import AnalyticsFunction


# from .report_data_processing.sql import load_sql_to_string


def process_sql_to_queries(af: AnalyticsFunction,
                           parameters: dict,
                           rerun: bool,
                           sql_template_dir: Union[Path, str],
                           sql_processed_dir: Union[Path, str]):
    if not rerun:
        return
    sql_templates = sorted(Path(sql_template_dir).glob('*.sql_templates'))
    jinja_templates = sorted(Path(sql_template_dir).glob('*.jinja2'))

    for template in sql_templates:
        query = load_sql_to_string(template.name,
                                   parameters=parameters,
                                   directory=sql_template_dir)
        filepath = Path(sql_processed_dir) / template
        with open(filepath) as f:
            f.write(query)

        # af.add_existing_file(filepath)


class Node(NamedTuple):
    name: str
    info: str = ''
    n_out: int = 0
    n_in: int = 0


class Edge(NamedTuple):
    from_node: str
    to_node: str


class Dag(object):
    def __init__(self,
                 nodes: dict = {},
                 edges: List[Edge] = []):
        self.nodes = nodes
        self.edges = edges

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


def build_sql_dag(rerun: bool,
                  sql_processed_dir: Union[Path, str]):
    dag = Dag()
    processed_sql = sorted(Path(sql_processed_dir).glob('*.sql'))

    heading_marker = pp.Literal('##')
    summary_head = heading_marker + pp.Literal('Summary') + pp.White()
    description_head = heading_marker + pp.Literal('Description') + pp.White()
    contacts_head = heading_marker + pp.Literal('Contacts') + pp.White()
    requires_head = heading_marker + pp.Literal('Requires') + pp.White()
    creates_head = heading_marker + pp.Literal('Creates') + pp.White()

    info_body = pp.ZeroOrMore(pp.Word(pp.alphas + '.@://{}_'))
    summary = summary_head.suppress() + pp.Combine(info_body, adjacent=False, join_string=" ").set_results_name(
        'summary')
    description = description_head + info_body.set_results_name('description')
    contacts = contacts_head + info_body.set_results_name('contacts')

    node_type = (pp.Literal('table') ^ pp.Literal('file')).set_results_name('type', list_all_matches=True)
    node_name = pp.Word(pp.alphas + '.@://{}_').set_results_name('name', list_all_matches=True)
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
                {f'{node_type}_{name}': Node(name) for ndoe_type, name in parsed.info.requires}
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
        test = dag.mermaid()
        print(dag.mermaid())


if __name__ == '__main__':
    build_sql_dag(True, Path('../../report_data_processing/sql_templates'))
