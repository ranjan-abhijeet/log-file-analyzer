import os
import pandas


class FileNotFoundException(Exception):
    """ Raised when file at file path is not found"""
    pass


class LogAnalyzer():
    """
    Analyzes log files..
    Works with log files with the following format, but can be extended to work 
    with other formats as well:

        2022-12-07 19:13:11.030 > PROCESS: Blah blah blah
    """
    def __init__(self, file_path: str, log_file_timestamp_separator=" > "):
        self.file_path = self.__check_path(file_path)
        self.separator = log_file_timestamp_separator

    def __check_path(self, file_path):
        if os.path.exists(file_path):
            return file_path
        else:
            raise FileNotFoundException(f'Could not find file at: {file_path}')

    def get_dataframe(self):
        """
        Reads the log file and converts into a pandas DataFrame object

        Args:
            None
        Returns:
            (pandas.DataFrame) pandas DataFrame object with rows containing each line of .log file
        """
        rows = []
        with open(self.file_path, 'r') as file:
            for count, line in enumerate(file):
                if line != "\n":
                    info = line.rstrip().split(self.separator)
                    row_dict = {}
                    try:
                        row_dict["timestamp"] = info[0]
                        row_dict["log"] = info[1]
                        rows.append(row_dict)
                    except IndexError:
                        continue

        df = pandas.DataFrame(rows)
        df['timestamp'] = pandas.to_datetime(df['timestamp'])
        return df
        
    def search_substring(self, substring: str, export: bool=False, file_write_path: str=None):
        """
        Searches a substring in the log file

        Args:
            substring: (str) the string which needs to be searched
            export: (bool) if the data found after searching needs to be exported
            file_write_path: (str) the path where data should be exported
        Returns:
            (pandas.DataFrame) pandas DataFrame object with rows containing substring
        """
        data = self.get_dataframe()
        sub_data = data[data["log"].str.contains(substring)]
        if export:
            if file_write_path is None:
                file_write_path = self.file_path.split(".log")[0] + f"_{substring}" + ".csv"
            sub_data.to_csv(file_write_path, index=False)
        return sub_data

    def count_substring_occurence(self, substring: str):
        """
        Counts the number of occurences of a substring

        Args:
            substring: (str) the string which needs to be searched
        
        Returns
            (int) number of occurences of substring
        """
        data = self.search_substring(substring=substring)
        print(f'Found {len(data)} occurences of "{substring}"')
        return len(data)

    def export_as_csv(self, file_write_path: str=None):
        """
        Exports the .log file to .csv file

        Args:
            file_write_path: (str) the path where data should be written

        Return:
            None
        """
        if file_write_path is None:
            file_write_path = self.file_path.split(".log")[0] + ".csv"
        data = self.get_dataframe()
        data.to_csv(file_write_path, index=False)
        print(f'Exported data to: {file_write_path}')