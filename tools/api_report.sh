#!/usr/bin/env bash
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

set -eu

TMPDIR=`mktemp -d /tmp/${0##*/}.XXXXXX` || exit 1
trap "rm -rf $TMPDIR" EXIT

PROJECT="neutron-lib"
PACKAGE="neutron_lib"
PYIR_PATH="tools/pyir.py"
TAG_RELEASE=''


usage() {
  echo "Usage: $0 [OPTION]..."
  echo "Generate a python API report between current and the said release tag."
  echo ""
  echo "  -t, --tag=[<tag>] Release tag to generate API report difference with."
  echo "                    Defaults to the latest git tag."
  echo "  -h, --help        Print this usage message"
  echo
  exit 0
}


install_project() {
    git clone -b ${TAG_RELEASE} https://github.com/openstack/${PROJECT}.git ${TMPDIR}/${PROJECT} || (echo "Failed to install ${TAG_RELEASE}" && exit 2)
}


parse_args() {
    while [ "$1" != "" ]; do
        PARAM=`echo $1 | awk -F= '{print $1}'`
        VALUE=`echo $1 | awk -F= '{print $2}'`
        case ${PARAM} in
            -h | --help)
                usage
                exit
                ;;
            -t | --tag)
                TAG_RELEASE=${VALUE}
                break
                ;;
            *)
                echo "ERROR: unknown parameter \"${PARAM}\""
                usage
                exit 1
                ;;
        esac
        shift
    done
}


if [ $# -ne 0 ]; then
    parse_args $@
fi


if [[ ${TAG_RELEASE} == '' ]]; then
    echo "Finding latest git tag..."
    TAG_RELEASE=`git tag | tail -n1`
    if [[ $? -ne 0 ]]; then
        echo "Failed to find latest git tag! Exiting."
        exit 1
    fi
    echo "Set tag to: ${TAG_RELEASE}"
fi


${PYIR_PATH} generate --blacklist '.*\/tests\/.*','.*\._(\w*)' ${PACKAGE} > "${TMPDIR}/${PACKAGE}.master.json.txt"

install_project
${PYIR_PATH} generate --blacklist '.*\/tests\/.*','.*\._(\w*)' ${TMPDIR}/${PROJECT}/${PACKAGE} > "${TMPDIR}/${PACKAGE}.${TAG_RELEASE}.json.txt"


echo "==========================================================="
echo "Changes between current commit and release tag ${TAG_RELEASE}"
echo "==========================================================="

${PYIR_PATH} diff "${TMPDIR}/${PACKAGE}.master.json.txt" "${TMPDIR}/${PACKAGE}.${TAG_RELEASE}.json.txt"

