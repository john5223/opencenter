#!/usr/bin/env python

from flask import Blueprint, Response, jsonify, url_for, request

import db.api as api
import generic
import utility

object_type = 'adventures'
bp = Blueprint(object_type, __name__)


@bp.route('/', methods=['GET', 'POST'])
def list():
    return generic.list(object_type)


@bp.route('/<object_id>', methods=['GET', 'PUT', 'DELETE'])
def by_id(object_id):
    return generic.object_by_id(object_type, object_id)

@bp.route('/<adventure_id>/execute', methods=['POST'])
def execute_adventure(adventure_id):
    data = request.json
    data['adventure'] = adventure_id

    nodes = utility.expand_nodelist(data['nodes'])
    data['nodes'] = nodes

    # find the node with the adventurator plugin
    query = "'adventurator' in facts.roush_agent_output_modules"

    adventure_nodes = api.nodes_query(query)

    if len(adventure_nodes) > 0:
        adventure_node = adventure_nodes.pop(0)['id']

        task = api.task_create({'action': 'adventurate',
                                'node_id': adventure_node,
                                'payload': data})
        utility.notify('task-for-%s' % adventure_node)

        href = request.base_url + str(task['id'])
        msg = {'status': 201,
               'message': 'Task Created',
               'task': task,
               'ref': href}
    else:
        msg = {'status': 404,
               'message': 'Cannot find adventure orchestrator'}

    resp = jsonify(msg)
    resp.status_code = msg['status']

    return resp
