#!/usr/bin/env bash
# Build the module into a Python package (whl file). The version assigned to
# the API will be assigned from:
#
# 1: Version argument passed to the script (takes precendence)
# 2: The latest git tag from the current branch commit
# 3: The latest git tag (if present and no other version found)
#
# If no version is found the script will fail.
#
# Arguments:
# 1: Optional build version to override git tag version
set -e

function build() {
  local pkg_name='tre_event_lib'

  printf 'Attempting to get latest git tag from branch commit\n'
  local latest_tag_branch_commit
  if latest_tag_branch_commit="$(git describe --exact-match --abbrev=0)"; then
    printf 'latest_tag_branch_commit=%s' "${latest_tag_branch_commit}"
  fi
  
  printf 'Attempting to get latest git tag from anywhere\n'
  local latest_tag_anywhere
  if latest_tag_anywhere="$(
    git describe --tags "$(git rev-list --tags --max-count=1)"
  )"; then
    printf 'latest_tag_anywhere=%s' "${latest_tag_anywhere}"
  fi
  
  local BUILD_VERSION="${1:-${latest_tag_branch_commit:-${latest_tag_anywhere}}}"

  # Ensure BUILD_VERSION is set (i.e. ":?")
  printf 'BUILD_VERSION=%s\n' "${BUILD_VERSION:?}"

  # Remove local build files to ensure clean environment
  ./clean.sh

  # Create build specific content (e.g. version from git tag)
  printf '{\n  "version": "%s"\n}\n' "${BUILD_VERSION}" > "${pkg_name}/about.json"

  # Check tests pass
  printf 'Running Python tests\n'
  export BUILD_VERSION
  python3 -m unittest discover "${pkg_name}/tests" -p 'test_*.py'

  # Build package .whl file in ./dist/
  printf 'Building\n'
  python3 setup.py bdist_wheel

  printf -- '--- ./dist -------------------------------------------------\n'
  find ./dist -name '*.whl'
  printf -- '------------------------------------------------------------\n'
  unzip -l "$(find ./dist -name '*.whl')"
}

build "$@"
