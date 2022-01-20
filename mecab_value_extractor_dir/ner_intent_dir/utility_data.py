import csv


def read_csv(data_dir):
    with open(data_dir, 'r', encoding='utf-8-sig') as reader_csv:
        reader = csv.reader(reader_csv, delimiter=',')
        return list(reader)


def write_csv(data_dir, csv_list):
    with open(data_dir, 'w', encoding='utf-8-sig', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
        for idx, csv_item in enumerate(csv_list):
            writer.writerow([idx, *csv_item])