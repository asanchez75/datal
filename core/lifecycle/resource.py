# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from core.choices import StatusChoices
from core.daos import ActivityStreamDAO
from workspace.exceptions import IlegalStateException
from core.lib.datastore import *
from core.models import User


class AbstractLifeCycleManager():
    """ Manage a Resource Life Cycle"""

    __metaclass__ = ABCMeta

    CREATE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.PUBLISHED]
    PUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED]
    UNPUBLISH_ALLOWED_STATES = [StatusChoices.PUBLISHED]
    SEND_TO_REVIEW_ALLOWED_STATES = [StatusChoices.DRAFT]
    ACCEPT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
    REJECT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
    REMOVE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED ]
    EDIT_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED]

    @abstractmethod
    def create(self, allowed_states=CREATE_ALLOWED_STATES, **fields):
        """ create a new dataset """
        """ collect_type is COLLECT_TYPE_CHOICES (0, 1, 2) """

   
        # Check for allowed states
        status = fields.get('status', StatusChoices.DRAFT)
        
        if status not in allowed_states:
            raise IlegalStateException(allowed_states)


    @abstractmethod
    def publish(self, allowed_states=PUBLISH_ALLOWED_STATES):
        """ Publish a dataset revision together with its datastreams """

        if self.dataset_revision.status not in allowed_states:
            ## Trying to publish a published revision? Uhmmm, something is wrong.
            raise IlegalStateException(allowed_states, self.dataset_revision)

    @abstractmethod
    def _publish_childs(self):
        pass        

    @abstractmethod
    def unpublish(self, killemall=False, allowed_states=UNPUBLISH_ALLOWED_STATES):
        """ unpublish dataset revision"""

        if self.dataset_revision.status not in allowed_states:
            raise IlegalStateException(allowed_states, self.dataset_revision)


    @abstractmethod
    def _unpublish_all(self):
        pass

    @abstractmethod
    def send_to_review(self, allowed_states=SEND_TO_REVIEW_ALLOWED_STATES):
        """ send a dataset revision to review"""

        if self.dataset_revision.status not in allowed_states:
            raise IlegalStateException(allowed_states, self.dataset_revision)
    
    @abstractmethod
    def _send_childs_to_review(self):
        pass  

    @abstractmethod
    def accept(self, allowed_states=ACCEPT_ALLOWED_STATES):

        if self.dataset_revision.status not in allowed_states:
            raise IlegalStateException(allowed_states, self.dataset_revision)

    @abstractmethod
    def reject(self, allowed_states=REJECT_ALLOWED_STATES):
        """ reject a resource revision """

        if self.dataset_revision.status not in allowed_states:
            raise IlegalStateException(allowed_states, self.dataset_revision )

    @abstractmethod
    def remove(self, killemall=False, allowed_states=REMOVE_ALLOWED_STATES):
        """ Remove a revision or the entire dataset """

        if self.dataset_revision.status not in allowed_states:
            raise IlegalStateException(allowed_states, self.dataset_revision)

    @abstractmethod
    def _remove_all(self):
        pass

    @abstractmethod
    def edit(self, allowed_states=EDIT_ALLOWED_STATES, changed_fields=None, **fields):
        """create new revision or update it"""

        old_status = self.dataset_revision.status
        if old_status  not in allowed_states:
            raise IlegalStateException(allowed_states, self.dataset_revision)

    @abstractmethod
    def _move_childs_to_draft(self):
        pass

    @abstractmethod
    def save_as_draft(sef):
        pass

    @abstractmethod
    def _log_activity(self, action_id, resource_id, resource_type, revision_id, resource_title):
        return ActivityStreamDAO().create(account_id=self.user.account.id, user_id=self.user.id,
                                          resource_id=resource_id, revision_id=revision_id, resource_type=resource_type,
                                          resource_title=resource_title, action_id=action_id)

    @abstractmethod
    def _update_last_revisions(self):
        pass

    def __init__(self, user, language):
        self.user = type(user) is not int and user or User.objects.get(pk=user)
        self.language = language
