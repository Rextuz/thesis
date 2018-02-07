from mooc_stats_analyzer.submission_stages import stage_parser_by_order
from mooc_stats_analyzer.tasks import id_from_order


def best_sub(subm, user_id, task_order):
    task_id = id_from_order(task_order)
    subs = subm.subs_user_task(user_id, task_id)
    stages = stage_parser_by_order(task_order)()
    return stages.best_sub(subs)


def stopouts_number(subm, task_order, stage):
    stopout_this = 0
    stages = stage_parser_by_order(task_order)()
    task_id = id_from_order(task_order)
    for user_id in subm.users_attempted_task(task_id):
        best = best_sub(subm, user_id, task_order)
        stopout_stage = stages.best_stage(best)
        if stopout_stage == stage:
            stopout_this += 1

    total_users = len(subm.users_attempted_task(task_id))
    percentage = 100 / total_users * stopout_this

    return stopout_this, total_users, percentage


def stopout(subm, task_order):
    stages = stage_parser_by_order(task_order)()
    stopout_all = {}
    for stage in stages.stages:
        stopout_all[stage] = stopouts_number(subm, task_order, stage)

    return stopout_all
