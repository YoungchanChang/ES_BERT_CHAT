import csv


def read_txt(data_path):
    with open(data_path, "r", encoding='utf-8-sig') as file:
        txt_list = file.read().splitlines()
        return sorted(list(txt_list), key=len, reverse=True)


def write_txt(data_path, txt_list):
    with open(data_path, "w", encoding='UTF8') as file:
        for txt_item in txt_list:
            data = txt_item + "\n"
            file.write(data)


def read_csv(data_dir):
    with open(data_dir, 'r', encoding='utf-8-sig') as reader_csv:
        reader = csv.reader(reader_csv, delimiter=',')
        return list(reader)


def write_csv(data_dir, csv_list):
    with open(data_dir, 'w', encoding='utf-8-sig', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
        for idx, csv_item in enumerate(csv_list):
            writer.writerow([idx, *csv_item])