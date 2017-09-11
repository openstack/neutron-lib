# Copyright 2011, VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile


def replace_file(file_name, data, file_mode=0o644):
    """Replaces the contents of file_name with data in a safe manner.

    First write to a temp file and then rename. Since POSIX renames are
    atomic, the file is unlikely to be corrupted by competing writes.

    We create the tempfile on the same device to ensure that it can be renamed.

    :param file_name: Path to the file to replace.
    :param data: The data to write to the file.
    :param file_mode: The mode to use for the replaced file.
    :returns: None.
    """

    base_dir = os.path.dirname(os.path.abspath(file_name))
    with tempfile.NamedTemporaryFile('w+',
                                     dir=base_dir,
                                     delete=False) as tmp_file:
        tmp_file.write(data)
    os.chmod(tmp_file.name, file_mode)
    os.rename(tmp_file.name, file_name)
