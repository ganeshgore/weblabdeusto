#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
#
# Copyright (C) 2005-2009 University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
# 

from voodoo.override import Override
from weblab.core.coordinator.scheduler import Scheduler
from weblab.core.coordinator.clients.weblabdeusto import WebLabDeustoClient
from voodoo.log import logged

class ExternalWebLabDeustoScheduler(Scheduler):

    def __init__(self, generic_scheduler_arguments, baseurl, username, password, **kwargs):
        super(ExternalWebLabDeustoScheduler, self).__init__(generic_scheduler_arguments, **kwargs)

        self.baseurl  = baseurl
        self.username = username
        self.password = password

    def stop(self):
        pass

    @logged()
    @Override(Scheduler)
    def removing_current_resource_slot(self, session, resource_instance_id):
        return False

    # TODO: pooling
    def _create_client(self):
        client = WebLabDeustoClient(self.baseurl)
        session_id  = self.client.login(self.username,self.password)
        return client, session_id

    #######################################################################
    # 
    # Given a reservation_id, it returns in which state the reservation is
    # 
    @logged()
    @Override(Scheduler)
    def reserve_experiment(self, reservation_id, experiment_id, time, priority, initialization_in_accounting, client_initial_data):

        # TODO: map reservation_id with external reservation_id AND cookie!!!
        consumer_data = {
            'time_allowed'                 : time,
            'priority'                     : priority,
            'initialization_in_accounting' : initialization_in_accounting
        }

        client, session_id = self._create_client()
        reservation_status = client.reserve_experiment(session_id, experiment_id, client_initial_data, consumer_data)

        # TODO: establish a relationship

        return 

    #######################################################################
    # 
    # Given a reservation_id, it returns in which state the reservation is
    # 
    @logged()
    @Override(Scheduler)
    def get_reservation_status(self, reservation_id):
        # TODO
        raise NotImplementedError("")


    ################################################################
    #
    # Called when it is confirmed by the Laboratory Server.
    #
    @logged()
    @Override(Scheduler)
    def confirm_experiment(self, reservation_id, lab_session_id, initial_configuration):
        pass

    ################################################################
    #
    # Called when the user disconnects or finishes the resource.
    #
    @logged()
    @Override(Scheduler)
    def finish_reservation(self, reservation_id):
        pass

    ##############################################################
    # 
    # ONLY FOR TESTING: It completely removes the whole database
    # 
    @Override(Scheduler)
    def _clean(self):
        pass

