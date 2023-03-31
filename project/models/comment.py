from project.factory.validation import Validator
from project.factory.database import Database
from project.factory.response import ResponseMessage


class Comment(object):

    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = "comments"

        self.fields = {
            "fullname": "string",
            "email": "string",
            "comment": "string",
            "rate": "int",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["fullname", "email", "comment", "rate"]

        # Fields optional for CREATE
        self.create_optional_fields = ["fullname", "email", "comment", "rate"]

        # Fields required for UPDATE
        self.update_required_fields = ["fullname", "email", "comment", "rate"]

        # Fields optional for UPDATE
        self.update_optional_fields = ["fullname", "email", "comment", "rate"]
        
    def create(self, comment):
        # Validator will throw error if invalid
        validated = self.validator.validateTypes(comment, self.fields)
        if validated:
            err = self.validator.validate(comment, self.fields, self.create_required_fields, self.create_optional_fields)
            if err is None:
                res = self.db.insert(comment, self.collection_name)
                return ResponseMessage(res, "Data validated").send()
            else:
                return ResponseMessage(err, "Data required is missing").send()

        else:
            return ResponseMessage(validated, "Data type is missing").send()

    def find(self, comment, sortValue, skipValue, limitValue):  # find all
        return self.db.find(comment, self.collection_name, sortValue=sortValue, skipValue=skipValue, limitValue=limitValue)

    def count(self):
        return self.db.count(self.collection_name)


    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, comment):
        self.validator.validate(comment, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, comment,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
