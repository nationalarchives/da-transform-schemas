#!/usr/bin/env bash
# Removes Python package build files.
set -e

function clean() {
  printf 'Removing local build files\n'
  local pkg_name='tre_event_lib'
  rm -rfv "${pkg_name}/tests/__pycache__/"
  rm -rfv "${pkg_name}/__pycache__/"
  rm -rfv "${pkg_name}.egg-info/"
  rm -rfv build/
  rm -rfv dist/
}

clean
