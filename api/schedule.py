#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from flask import jsonify, request, abort
import traceback

from api import api
from logic.schedule import (
    logic_get_schedules,
    logic_add_schedule,
    logic_delete_schedule
)


@api.route('/schedules', methods=['GET'])
def api_get_schedules():
    year = month = None
    try:
        year = request.args.get('year').strip()
        month = request.args.get('month').strip()
        if not re.match(u'\d{4}$', year) or not re.match(u'\d{1,2}$', month):
            raise ValueError('year or month is wrong')
        if re.match(u'\d$', month):
            month = '0%s' % month
    except:
        print traceback.print_exc()
        abort(400)

    schedules = logic_get_schedules(year, month)
    return jsonify(stat=1, schedules=schedules), 200


@api.route('/schedules/add', methods=['POST'])
def api_add_schedule():
    title = s_type = start_date = end_date = None
    try:
        title = request.form.get('title').strip()
        s_type = request.form.get('type').strip()
        start_date = request.form.get('startdate').strip()
        end_date = request.form.get('enddate').strip()

        if not re.match(u'\d{4}-\d{2}-\d{2}$', start_date) or not re.match(u'\d{4}-\d{2}-\d{2}$', end_date):
            raise ValueError('start_date or end_date is wrong')

    except:
        print traceback.print_exc()
        abort(400)

    status = logic_add_schedule(title, s_type, start_date, end_date)
    if status:
        return jsonify(stat=1, msg="SUCCESS"), 200
    return jsonify(stat=0), 403


@api.route('/schedules/remove', methods=['DELETE'])
def api_delete_schedule():
    s_id = None
    try:
        s_id = request.form.get('id').strip()
    except:
        print traceback.print_exc()
        abort(400)

    status = logic_delete_schedule(s_id)
    if status:
        return jsonify(stat=1, msg="SUCCESS"), 200
    return jsonify(stat=0), 403
