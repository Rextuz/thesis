import csv

from mooc_stats_analyzer.submissions import SubmissionManager, SubmissionEntry

csv.field_size_limit(1024 * 1024)


def prepare_csv(filename):
    prepared_name = '_{}'.format(filename)
    line = open(filename, encoding='utf-8').read().replace('\0', '')

    with open(prepared_name, encoding='utf-8', mode='w') as prepared:
        prepared.write(line)

    return prepared_name


def get_full_submissions(filename):
    filename = prepare_csv(filename)
    entries = []
    with open(filename, encoding='utf-8') as full:
        field_names = ['submission_id', 'step_id', 'user_id', 'first_name',
                       'last_name', 'attempt_time',
                       'submission_time', 'status', 'dataset', 'clue', 'reply',
                       'reply_clear', 'hint']
        reader = csv.DictReader(full, fieldnames=field_names)

        for row in reader:
            try:
                float(row['submission_id'])
                submission = SubmissionEntry(row)
                if 'Service is busy right now. Try to submit again a bit later.' not in submission.hint:
                    entries.append(submission)
            except ValueError:
                pass

    return SubmissionManager(entries)
