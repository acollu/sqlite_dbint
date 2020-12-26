class FieldFormatter:
    comparison_operators = ["=", "<>", ">", "<", ">=", "<="] # equal, not equal, higher, lower, higher equal, lower equal
    logical_operators = ["AND", "OR"]

    @staticmethod
    def format_attributes(attributes):
        if attributes is all:
            return "*"
        elif isinstance(attributes, list):
            return ", ".join(attributes)
        else:
            TypeError

    @staticmethod
    def format_value(value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, str):
            return '"' + value + '"'
        else:
            raise TypeError

    @staticmethod
    def format_values(values):
        return ", ".join([self.format_value(value) for value in values])

    @staticmethod
    def format_condition(condition):
       if condition is None:
           return ""
       elif isinstance(condition, list):
           formatted_condition = "WHERE "
           for i, member in enumerate(condition):
               if i % 2:
                   if i + 1 == len(condition):
                       raise InvalidCondition
                   if member not in self.logical_operators:
                       raise InvalidLogicalOperator
                   formatted_condition += " " + member + " "
               else:
                   if len(member) != 3:
                      raise InvalidComparisonMember
                   if member[1] not in self.comparison_operators:
                       raise InvalidConditionalOperator
                   member[2] = FieldFormatter.format_value(member[2])
                   formatted_condition += " ".join(member)
           return formatted_condition
       else:
           raise TypeError

    @staticmethod
    def format_order(order_attributes, order_type):
        if order_attributes is None:
            return ""
        elif isinstance(order_attributes, list):
            return "ORDER BY " + self.format_attributes(order_attributes) + " " + order_type
        else:
            raise TypeError
