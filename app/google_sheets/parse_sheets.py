import gspread
from config import CREDENTIALS_FILENAME, SPREADSHEET_URL


class Sheet:
    def __init__(self, spreadsheet_url=SPREADSHEET_URL):
        self.account = gspread.service_account(filename=CREDENTIALS_FILENAME)
        self.spreadsheet = self.account.open_by_url(spreadsheet_url)
        self.topics = {
            elem.title: elem.id for elem in self.spreadsheet.worksheets()
        }
        self.answers = self.spreadsheet.get_worksheet_by_id(self.topics.get("Orders"))

    def get_topics(self):
        return {key: value for key, value in self.topics.items() if key != "Orders"}

    def get_writes_topic(self, topic_name):
        if topic_name in self.topics:
            worksheet = self.spreadsheet.get_worksheet_by_id(self.topics.get(topic_name))
            return worksheet.get_all_records()
        return []

    def questions_and_answers(self, topic_name):
        questions = self.get_writes_topic(topic_name)
        result = []
        for elem in questions:
            new_format = {
                "id": elem["ID"],
                "product": elem["Товар"],
                "price": elem["Стоимость"],
                "date": elem["Дата покупки"],
            }
            result.append(new_format)

        return result

    def write_answer_to_result_cell(self, id, product, price, date):
        index = len(list(filter(None, self.answers.col_values(1)))) + 1
        self.answers.update(f"A{index}:E{index}", [[
            id, product, price, date
        ]])






