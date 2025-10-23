from datetime import datetime


class DateUtils:
    @staticmethod
    def format_date(date_input) -> str:
        """Format date to 'Month Day, Year' format"""
        try:
            if isinstance(date_input, datetime):
                return date_input.strftime("%B %d, %Y")

            if isinstance(date_input, str):
                date_obj = datetime.fromisoformat(date_input.replace("Z", "+00:00"))
                return date_obj.strftime("%B %d, %Y")

            return str(date_input)
        except Exception:
            return str(date_input)
