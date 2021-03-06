# -*- coding: utf-8 -*-
# Copyright 2013 Bors Ltd
# This file is part of django-gitstorage.
#
#    django-gitstorage is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, print_function, unicode_literals

from django import forms
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _


class UsersChoiceField(forms.ModelMultipleChoiceField):

    def __init__(self, **kwargs):
        # Since superusers always are allowed, filter them out by default
        queryset = auth_models.User.objects.filter(is_superuser=False)
        super(UsersChoiceField, self).__init__(queryset, **kwargs)

    def label_from_instance(self, user):
        return "{0.first_name} {0.last_name} <{0.email}>".format(user)


class RemoveUsersForm(forms.Form):
    users = UsersChoiceField(label=_("Users"), widget=forms.CheckboxSelectMultiple)

    def __init__(self, current_user_ids, **kwargs):
        super(RemoveUsersForm, self).__init__(**kwargs)
        self.fields['users'].queryset = self.fields['users'].queryset.filter(pk__in=current_user_ids)


class AddUsersForm(forms.Form):
    users = UsersChoiceField(label=_("Users"), widget=forms.CheckboxSelectMultiple)

    def __init__(self, current_user_ids, **kwargs):
        super(AddUsersForm, self).__init__(**kwargs)
        self.fields['users'].queryset = self.fields['users'].queryset.exclude(pk__in=current_user_ids)


class UploadForm(forms.Form):
    file = forms.FileField(label=_("File"))
