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

    @staticmethod
    def extract_time(date_input) -> str:
        """Extract only the time in 'HH:MM AM/PM' format"""
        try:
            if isinstance(date_input, datetime):
                return date_input.strftime("%I:%M %p")

            if isinstance(date_input, str):
                date_obj = datetime.fromisoformat(date_input.replace("Z", "+00:00"))
                return date_obj.strftime("%I:%M %p")

            return str(date_input)
        except Exception:
            return str(date_input)

    @staticmethod
    def extract_date(date_input) -> str:
        """Extract only the date in 'MM/DD/YYYY' format"""
        try:
            if isinstance(date_input, datetime):
                return date_input.strftime("%m/%d/%Y")

            if isinstance(date_input, str):
                date_obj = datetime.fromisoformat(date_input.replace("Z", "+00:00"))
                return date_obj.strftime("%m/%d/%Y")

            return str(date_input)
        except Exception:
            return str(date_input)
