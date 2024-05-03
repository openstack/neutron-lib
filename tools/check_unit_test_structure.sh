#!/usr/bin/env bash

# This script identifies the unit test modules that do not correspond
# directly with a module in the code tree.  See TESTING.rst in neutron
# repo for the intended structure.

neutron_path=$(cd "$(dirname "$0")/.." && pwd)
base_test_path=neutron_lib/tests/unit
test_path=$neutron_path/$base_test_path

test_files=$(find ${test_path} -iname 'test_*.py')

ignore_regexes=(
    "^test_neutron_lib.py$"
    "^callbacks/test_callback_exceptions.py$"
    "^exceptions/test_exceptions.py$"
    "^api/validators/test_validators.py$"
    "^api/definitions/test_l3_multi_ext_gw.py$"
    "^api/definitions/test_l2_adjancency.py$"
    "^api/definitions/test_bgpvpn_router_assoc_stdattrs.py$"
    "^api/definitions/test_admin_state_down_before_update.py$"
    "^api/definitions/test_bgpvpn_net_assoc_stdattrs.py$"
    "^api/definitions/test_bgpvpn_port_assoc_stdattrs.py$"
    "^api/definitions/test_segment_peer_subnet_host_routes.py$"
    "^api/definitions/test_port_hardware_offload.py$"
    "^api/definitions/test_floating_ip_port_forwarding_port_range.py$"
    "^api/definitions/test_floating_ip_port_forwarding_extension.py$"
)

error_count=0
ignore_count=0
total_count=0
for test_file in ${test_files[@]}; do
    relative_path=${test_file#$test_path/}
    expected_path=$(dirname $neutron_path/neutron_lib/$relative_path)
    test_filename=$(basename "$test_file")
    expected_filename=${test_filename#test_}
    # Module filename (e.g. foo/bar.py -> foo/test_bar.py)
    filename=$expected_path/$expected_filename
    # Package dir (e.g. foo/ -> test_foo.py)
    package_dir=${filename%.py}
    if [ ! -f "$filename" ] && [ ! -d "$package_dir" ]; then
        for ignore_regex in ${ignore_regexes[@]}; do
            if [[ "$relative_path" =~ $ignore_regex ]]; then
                ignore_count=$((ignore_count + 1))
                continue 2
            fi
        done
        echo "Unexpected test file: $base_test_path/$relative_path"
        error_count=$((error_count + 1))
    fi
    total_count=$((total_count + 1))
done

if [ "$ignore_count" -ne 0 ]; then
    echo "$ignore_count unmatched test modules were ignored"
fi

if [ "$error_count" -eq 0 ]; then
    echo 'Success!  All test modules match targets in the code tree.'
    exit 0
else
    echo "Failure! $error_count of $total_count test modules do not match targets in the code tree."
    exit 1
fi
