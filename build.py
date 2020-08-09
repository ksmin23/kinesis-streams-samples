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
#use_plugin("python.unittest")
#use_plugin("python.flake8")
#use_plugin("python.coverage")
#use_plugin("python.distutils")
use_plugin('python.install_dependencies')
use_plugin("exec")


name = "kinesis-streams-samples"
default_task = "publish"


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
  logger.info("Executing pylint on project sources.")

  src_dir = project.get_property('dir_source_main_python')
  py_files = [e for e in discover_files_matching(src_dir, '*.py')]
  cmd = as_list('pylint', '--rcfile=.pylintrc', py_files)
  out_fname = project.expand_path("$dir_reports/{}".format('pylint'))
  err_fname = '{}.err'.format(out_fname)
  exit_code = execute_command(cmd, out_fname)
  report = read_file(out_fname)
  error = read_file(err_fname)

  if exit_code != 0 and len(error):
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
  except Exception as ex:
    traceback.print_exc()
    raise BuildFailedException('fail to parse pylint score.')

  cut_off = 8.5
  if project.get_property('break_build') and score < cut_off:
    msg = 'Fail to pass (score={:.2f}, cut_off={:.2f})'.format(score, cut_off)
    raise BuildFailedException(msg)
  else:
    logger.info('Pass (score={:.2f}, cut_off={:.2f})'.format(score, cut_off))


@task(description='kinesis data streams consumer')
def kinesis_consumer(project):
  src_name = 'consumer'
  dist_name = 'kinesis-streams-{}'.format(src_name)
  dist_dir = '{}/dist/{}'.format(project.get_property('dir_target'), dist_name)
  project.set_property('dir_source_main_python', 'src/main/python/{}'.format(src_name))
  project.set_property('dir_dist', dist_dir)
