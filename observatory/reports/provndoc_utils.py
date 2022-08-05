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


class DAG(NamedTuple):
    nodes = {}
    edges: List[Node] = []


def build_sql_dag(rerun: bool,
                  sql_processed_dir: Union[Path, str]):
    dag = DAG()
    processed_sql = sorted(Path(sql_processed_dir).glob('*.sql'))

    heading_marker = pp.Literal('##')
    summary_head = heading_marker + pp.Literal('Summary') + pp.White()
    description_head = heading_marker + pp.Literal('Description') + pp.White()
    contacts_head = heading_marker + pp.Literal('Contacts') + pp.White()
    requires_head = heading_marker + pp.Literal('Requires') + pp.White()
    creates_head = heading_marker + pp.Literal('Creates') + pp.White()

    info_body = pp.ZeroOrMore(pp.Word(pp.alphas + '.@://{}_'))
    summary = summary_head.suppress() + info_body.set_results_name('summary')
    description = description_head + info_body.set_results_name('description')
    contacts = contacts_head + info_body.set_results_name('contacts')

    node_type = (pp.Literal('table') ^ pp.Literal('file')).set_results_name('type')
    node_name = pp.Word(pp.alphas + '.@://{}_').set_results_name('name')
    reference = node_type + node_name
    requires = requires_head + reference[...].set_results_name('requires', list_all_matches=True)
    creates = creates_head + reference[...].set_results_name('creates', list_all_matches=True)

    info_section = summary ^ description ^ contacts ^ requires ^ creates

    info = pp.Literal('/*').suppress() + pp.Group(info_section[...]).set_results_name('info') + pp.Literal('*/').suppress()

    for sql in processed_sql:
        try:
            parsed = info.parse_file(sql)
            print(parsed)
        except pp.exceptions.ParseException as e:
            print(e)
            print(f'Failed on {sql}')
            continue


if __name__ == '__main__':
    build_sql_dag(True, Path('../../report_data_processing/sql_templates'))
