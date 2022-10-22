from project.factory.database import Database
from project.factory.validation import Validator
from project.factory.response import ResponseMessage
from project.algorithm.machineModel import MachineModel

import pandas as pd


class Predict(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()
        self.machine_model = MachineModel()

        self.collection_name = "predict_result"

        self.fields = {
            "input_text": "string",
            "result_prediction": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["input_text ","input_prediction"]

        # Fields optional for CREATE
        self.create_optional_fields = ["input_text ","input_prediction"]

        # Fields required for UPDATE
        self.update_required_fields = ["input_text ","input_prediction"]

        # Fields optional for UPDATE
        self.update_optional_fields = ["input_text ","input_prediction"]

    def classify(self, input_text):
        cleaned_text = self.machine_model.clean_text(input_text)
        series_text = pd.Series(cleaned_text)
        preprocessed_text = series_text.apply(self.machine_model.preprocess_tweet)
        vectorized_text = self.machine_model.TFIDFVector.transform(preprocessed_text.astype("U"))
        result_test = self.machine_model.ModelML.predict(vectorized_text)
        final_result = self.machine_model.difine_result(result_test)
        return final_result
        
    def create(self, predict):
        # Validator will throw error if invalid
        validated = self.validator.validateTypes(predict, self.fields)
        if validated:
            err = self.validator.validate(predict, self.fields, self.create_required_fields, self.create_optional_fields)
            if err is None:
                res = self.db.insert(predict, self.fields)
                return ResponseMessage(res, "Data validated").send()
            else:
                return ResponseMessage(err, "Data required is missing").send()

        else:
            return ResponseMessage(validated, "Data type is missing").send()

    def find(self, predict):  # find all
        return self.db.find(predict, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, predict):
        self.validator.validate(predict, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, predict,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
