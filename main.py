from mooc_stats_analyzer.csv_parser import get_full_submissions
from mooc_stats_analyzer.stopout_stages import stopout
from mooc_stats_analyzer.submission_stages import stages_for_all
from mooc_stats_analyzer.tasks import name_from_order, orders


def main():
    subs = get_full_submissions('submissions-full.csv')
    print('sub_count', subs.sub_count())
    print('unique_users', len(subs.unique_users), subs.unique_users)
    print('tasks', subs.tasks())
    print('dropout', subs.dropout())
    print('dropout', [100 / len(subs.unique_users) * x for x in subs.dropout()])
    for task_order in orders():
        task_name = name_from_order(task_order)
        succ, fail = subs.succ_fail(task_order)
        total = subs.n_of_subs(task_order)
        print('succ/fail [total] {}: {}/{} [{}]'.format(task_name, succ, fail,
                                                        total))

    for task_order in range(1, 10):
        stages_for_all(subs, task_order)

    for task_order in range(1, 10):
        print(name_from_order(task_order), stopout(subs, task_order))


if __name__ == '__main__':
    main()
