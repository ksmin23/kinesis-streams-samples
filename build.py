# -*- coding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

from pybuilder.core import use_plugin, init, task

use_plugin("python.core")
#use_plugin("python.unittest")
#use_plugin("python.flake8")
#use_plugin("python.coverage")
#use_plugin("python.distutils")


name = "kinesis-streams-samples"
default_task = "publish"


@init
def set_properties(project):
  project.set_property('dir_dist_scripts', None)


@task(description='kinesis data streams consumer')
def kinesis_consumer(project):
  src_name = 'consumer'
  dist_name = 'kinesis-streams-{}'.format(src_name)
  dist_dir = '{}/dist/{}'.format(project.get_property('dir_target'), dist_name)
  project.set_property('dir_source_main_python', 'src/main/python/{}'.format(src_name))
  project.set_property('dir_dist', dist_dir)
