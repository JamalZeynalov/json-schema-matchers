from hamcrest.core.base_matcher import BaseMatcher
from jsonschema import Draft7Validator, exceptions, RefResolutionError
from jsonschema.exceptions import UnknownType


class MatchesJsonSchema(BaseMatcher):

    def __init__(self, json_schema: dict):
        self.json_schema = json_schema
        self.error = ''

    def _matches(self, instance):
        try:
            self.validator = Draft7Validator(self.json_schema)
            self.validator.validate(instance)
            return True

        except exceptions.ValidationError:
            for error in sorted(self.validator.iter_errors(instance), key=str):
                self.error += f"\n{error}\n\n------------"
            return False

        except (AttributeError, RefResolutionError, KeyError, UnknownType) as attr_e:
            raise Exception(f" Schema is invalid:\n\n{attr_e}\n\n{self.json_schema}")

        # except RefResolutionError as ref_e:
        #     raise RefResolutionError(f" Schema is invalid:\n\n{ref_e}\n\n{self.json_schema}")

    def describe_to(self, description):
        title = self.json_schema.get("title", None)
        title = f' "{title}"' if title else ''
        description.append_text(f'\n     JSON object should match schema{title}')

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(f'\n     mismatches occurred: \n{self.error}')


def matches_json_schema(json_schema: dict):
    return MatchesJsonSchema(json_schema)
