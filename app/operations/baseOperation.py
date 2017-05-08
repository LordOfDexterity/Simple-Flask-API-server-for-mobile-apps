from importlib import import_module
from flask import request
import logging as log
from app import db, engine
from app.libs.reponse import format_response
import json
from sqlalchemy import or_


class BaseOperation(object):
    def __init__(self):
        self.params = request.form
        db.create_all()

    def __del__(self):
        log.warn('Releasing resource')
        # Release db resources here

    def model(self):
        imported_module = import_module('app.models.%s' % self.application_name())
        try:
            model = getattr(imported_module, self.application_name())
            return model
        except AttributeError:
            error_msg = 'Define model for "%s" in Shop.py ' % self.application_name()
            raise NotImplementedError(error_msg)

    def application_name(self):
        """
            Implement in all operations.
            Helps to obtain class name dynamically
        """
        raise NotImplementedError('Derived class should override this method')

    def create(self):
        record = self._prepare_record()
        if isinstance(record, str):
            return format_response(record)
        else:
            db.session.add(record)
            db.session.commit()
            return format_response('%s added successfully' % self.application_name())

    def lists(self):
        """
            List all records of current context
        """
        search_fields_from_params = self._collect_searchable_fields()
        # If no condition if found, all records are listed
        conditions = self._get_conditions_from_parameters(search_fields_from_params)
        records = self.model().query.filter(or_(*conditions)).all()
        lists = []
        for record in records:
            record_dict = record.__dict__
            del record_dict['_sa_instance_state']
            lists.append(record_dict)
        return format_response(lists)

    def delete(self):
        """
            Delete record by id(s)
        """
        if not self.params.get('id'):
            return format_response('Insufficient parameter: id not given')
        record_ids = json.loads(self.params.get('id'))
        if not isinstance(record_ids, list):
            record_ids = [record_ids, ]

        deleted_records = []
        no_of_records_deleted = 0
        for record_id in record_ids:
            current_delete_count = self.model().query.filter_by(id=record_id).delete()
            no_of_records_deleted += current_delete_count
            db.session.commit()
            if current_delete_count != 0:
                deleted_records.append(record_id)

        if len(deleted_records) == 1:
            deleted_ids = deleted_records[0]
            delete_message = 'Record deleted successfully [id = %s]' % deleted_ids
        elif deleted_records:
            deleted_ids = ', '.join(deleted_records)
            delete_message = '%s record deleted successfully [ids = %s]' % (no_of_records_deleted, deleted_ids)
        else:
            delete_message = 'Could not find records with specified ids'
        return format_response(delete_message)

    def drop(self):
        """
            Deletes the table of current context
        """
        self.model().__table__.drop(engine)
        return format_response('%s table dropped' % self.application_name())

    def _prepare_record(self):
        """
            1. Check for all the required/unique fields for a model.
            2. Also does validation check
            3. :Returns: An instance of model class
            4. :Returns: Error message if any
        """

        required_columns = self.model().required_columns()
        missing = []
        for required_column in required_columns:
            if required_column not in self.params:
                missing.append(required_column)
        if missing:
            return 'Required parameters missing: %s' % ', '.join(missing)

        unique_fields = self.model().unique_columns()
        for unique_field in unique_fields:
            condition = {unique_field: self.params.get(unique_field)}
            shop = self.model().query.filter_by(**condition).first()
            if shop:
                unique_field_value = self.params.get(unique_field)
                return '%s %s already exists' % (unique_field, str(unique_field_value))

        columns = {}
        for param in self.params:
            columns.update({param: self.params.get(param)})

        if not self.model().is_valid(**columns):
            return 'Invalid parameters given'

        return self.model()(**columns)

    def _collect_searchable_fields(self):
        # Collect searchable fields if present in parameters
        searchable_fields = self.model().searchable_columns()
        search_fields_from_params = []
        for search_field in searchable_fields:
            field = self.params.get(search_field)
            if field:
                search_fields_from_params.append(search_field)
        return search_fields_from_params

    def _get_conditions_from_parameters(self, search_fields_from_params):
        # Get all conditions for search (if any searchable fields are present in parameters sent)
        conditions = []
        if not search_fields_from_params:
            return conditions
        for search_fields_from_param in search_fields_from_params:
            search_field = getattr(self.model(), search_fields_from_param)
            search_value = self.params.get(search_fields_from_param)
            if search_fields_from_param == 'id':
                condition = (search_field == search_value)
            else:
                condition = search_field.startswith(search_value)
            conditions.append(condition)
        return conditions
