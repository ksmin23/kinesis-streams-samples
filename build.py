#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import re
import traceback

from pybuilder.core import use_plugin, init, task, after, depends
from pybuilder.errors import BuildFailedException
from pybuilder.utils import assert_can_execute, read_file, execute_command, as_list, \
  discover_files_matching

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("exec")

name = "kinesis-streams-samples" #pylint: disable=C0103
default_task = "package" #pylint: disable=C0103


@init
def set_properties(project):
  project.set_property('dir_dist_scripts', None)
  project.build_depends_on('pylint', '~=2.5.0')
  project.set_property_if_unset('break_build', True)


@after('prepare')
def check_if_pylint_exists(logger):
  logger.debug('Checking if pylint is installed')
  assert_can_execute(('pylint', ), 'pylint', 'checkstyle', None)
  logger.debug('pylint exists')


@depends('prepare')
@task(description='check code style using pylint')
def checkstyle(project, logger):
  #pylint: disable=R0914
  logger.info("Executing pylint on project sources.")

  src_dir = project.get_property('dir_source_main_python')
  py_files = [e for e in discover_files_matching(src_dir, '*.py')] #pylint: disable=R1721
  cmd = as_list('pylint', '--rcfile=.pylintrc', py_files)
  out_fname = project.expand_path("$dir_reports/{}".format('pylint'))
  err_fname = '{}.err'.format(out_fname)
  exit_code = execute_command(cmd, out_fname)
  report = read_file(out_fname)
  error = read_file(err_fname)

  if exit_code != 0 and error:
    msg = 'Errors occurred while running pylint, check {}'.format(err_fname)
    logger.error(msg)
    raise BuildFailedException(msg)
  logger.warn(''.join(report))

  try:
    # get pylint score from the message
    # e.g. "Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)"
    pattern = r'(\d{0,2}\.\d{2})/10'
    pat = re.compile(pattern)
    res = re.search(pat, report[-2])
    score = float(res.group(1))
  except Exception as _:
    traceback.print_exc()
    raise BuildFailedException('fail to parse pylint score.')

  cutoff = 8.5
  if project.get_property('break_build') and score < cutoff:
    msg = 'Fail to pass (score={:.2f}, cutoff={:.2f})'.format(score, cutoff)
    raise BuildFailedException(msg)
  logger.info('Pass (score={:.2f}, cutoff={:.2f})'.format(score, cutoff))


@task(description='kinesis data streams consumer')
def kinesis_consumer(project):
  src_name = 'consumer'
  dist_name = 'kinesis-streams-{}'.format(src_name)
  dir_dist = '{}/dist/{}'.format(project.get_property('dir_target'), dist_name)
  project.set_property('dir_source_main_python', 'src/main/python/{}'.format(src_name))
  project.set_property('dir_dist', dir_dist)


@task(description='kinesis data streams producers')
def kinesis_producers(project):
  src_name = 'producers'
  dist_name = 'kinesis-streams-{}'.format(src_name)
  dir_dist = '{}/dist/{}'.format(project.get_property('dir_target'), dist_name)
  project.set_property('dir_source_main_python', 'src/main/python/{}'.format(src_name))
  project.set_property('dir_dist', dir_dist)


@task(description='kinesis data streams producer: stocks')
def kinesis_stocks_producer(project):
  src_name = 'producers'
  dist_name = 'kinesis-streams-stocks'
  dir_dist = '{}/dist/{}'.format(project.get_property('dir_target'), dist_name)
  project.set_property('dir_source_main_python', 'src/main/python/{}'.format(src_name))
  project.set_property('dir_dist', dir_dist)
  #pylint: disable=W1401
  cmd = '''find {dir_dist}/ -type f -name '*.py' ! -name '{src_file}' -exec rm -f {{}} \;'''.format(
    dir_dist=dir_dist, src_file='stocks.py')
  project.set_property('package_command', cmd)
