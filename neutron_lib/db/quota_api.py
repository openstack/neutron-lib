# Copyright (c) 2021 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc


class QuotaDriverAPI(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_default_quotas(context, resources, project_id):
        """Retrieve the default quotas for the list of resources and project.

        :param context: The request context, for access checks.
        :param resources: A dictionary of the registered resource keys.
        :param project_id: The ID of the project to return default quotas for.
        :return: dict from resource name to dict of name and limit
        """

    @staticmethod
    @abc.abstractmethod
    def get_project_quotas(context, resources, project_id):
        """Retrieve the quotas for the given list of resources and project

        :param context: The request context, for access checks.
        :param resources: A dictionary of the registered resource keys.
        :param project_id: The ID of the project to return quotas for.
        :return: dict from resource name to dict of name and limit
        """

    @staticmethod
    @abc.abstractmethod
    def get_detailed_project_quotas(context, resources, project_id):
        """Retrieve detailed quotas for the given list of resources and project

        :param context: The request context, for access checks.
        :param resources: A dictionary of the registered resource keys.
        :param project_id: The ID of the project to return quotas for.
        :return dict: mapping resource name in dict to its corresponding limit
                      used and reserved. Reserved currently returns default
                      value of 0
        """

    @staticmethod
    @abc.abstractmethod
    def delete_project_quota(context, project_id):
        """Delete the quota entries for a given project_id.

        After deletion, this project will use default quota values in conf.
        Raise a "not found" error if the quota for the given project was
        never defined.

        :param context: The request context, for access checks.
        :param project_id: The ID of the project to return quotas for.
        """

    @staticmethod
    @abc.abstractmethod
    def get_all_quotas(context, resources):
        """Given a list of resources, retrieve the quotas for the all tenants.

        :param context: The request context, for access checks.
        :param resources: A dictionary of the registered resource keys.
        :return: quotas list of dict of project_id:, resourcekey1:
                 resourcekey2: ...
        """

    @staticmethod
    @abc.abstractmethod
    def update_quota_limit(context, project_id, resource, limit):
        """Update the quota limit for a resource in a project

        :param context: The request context, for access checks.
        :param project_id: The ID of the project to update the quota.
        :param resource: the resource to update the quota.
        :param limit: new resource quota limit.
        """

    @staticmethod
    @abc.abstractmethod
    def make_reservation(context, project_id, resources, deltas, plugin):
        """Make multiple resource reservations for a given project

        :param context: The request context, for access checks.
        :param resources: A dictionary of the registered resource keys.
        :param project_id: The ID of the project to make the reservations for.
        :return: ``ReservationInfo`` object.
        """

    @staticmethod
    @abc.abstractmethod
    def commit_reservation(context, reservation_id):
        """Commit a reservation register

        :param context: The request context, for access checks.
        :param reservation_id: ID of the reservation register to commit.
        """

    @staticmethod
    @abc.abstractmethod
    def cancel_reservation(context, reservation_id):
        """Cancel a reservation register

        :param context: The request context, for access checks.
        :param reservation_id: ID of the reservation register to cancel.
        """

    @staticmethod
    @abc.abstractmethod
    def limit_check(context, project_id, resources, values):
        """Check simple quota limits.

        For limits--those quotas for which there is no usage
        synchronization function--this method checks that a set of
        proposed values are permitted by the limit restriction.

        If any of the proposed values is over the defined quota, an
        OverQuota exception will be raised with the sorted list of the
        resources which are too high.  Otherwise, the method returns
        nothing.

        :param context: The request context, for access checks.
        :param project_id: The ID of the project to make the reservations for.
        :param resources: A dictionary of the registered resource.
        :param values: A dictionary of the values to check against the
                       quota.
        """

    @staticmethod
    @abc.abstractmethod
    def get_resource_usage(context, project_id, resources, resource_name):
        """Return the resource current usage

        :param context: The request context, for access checks.
        :param project_id: The ID of the project to make the reservations for.
        :param resources: A dictionary of the registered resources.
        :param resource_name: The name of the resource to retrieve the usage.
        :return: The current resource usage.
        """

    @staticmethod
    @abc.abstractmethod
    def quota_limit_check(context, project_id, resources, deltas):
        """Check the current resource usage against a set of deltas.

        This method will check if the provided resource deltas could be
        assigned depending on the current resource usage and the quota limits.
        If the resource deltas plus the resource usage fit under the quota
        limit, the method will pass. If not, a ``OverQuota`` will be raised.

        :param context: The request context, for access checks.
        :param project_id: The ID of the project to make the reservations for.
        :param resources: A dictionary of the registered resource.
        :param deltas: A dictionary of the values to check against the
                       quota limits.
        :return: None if passed; ``OverQuota`` if quota limits are exceeded,
                 ``InvalidQuotaValue`` if delta values are invalid.
        """

    @staticmethod
    @abc.abstractmethod
    def get_workers():
        """Return the quota driver workers to be spawned during initialization

        This method returns the quota driver workers that needs to be spawned
        during the plugin initialization. For example, ``DbQuotaNoLockDriver``
        requires a ``PeriodicWorker`` to clean up the expired reservations left
        in the database.

        :return: list of ``worker.BaseWorker`` or derived instances.
        """
