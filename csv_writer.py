import csv

def write_post_csv(file_path, post_rows):
    fieldnames = ['type_id', 'post_id', 'post_text', 'posted_at',
                  'user_name', 'user_id', 'tags', 'image', 'total_likes']

    with open(file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(post_rows)
