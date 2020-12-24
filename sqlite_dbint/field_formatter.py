class FieldFormatter:
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
           condition[-1] = FieldFormatter.format_value(condition[-1])
           return "WHERE " + " ".join(condition)
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
