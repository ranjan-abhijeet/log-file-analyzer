**How to use**

- Create object of LogAnalyzer class by passing the path of log file:

    `log = LogAnalyzer('data_files/info.log')`

- Export the log file to a .csv file:

    `log.export_as_csv(file_write_path='data_files/info.csv')`

- Search for a substring in the logs, set `export=True` to export data:

    `mpudata_154 = log.search_substring('mpudata_154', export=True)`
    
