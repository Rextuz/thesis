import datetime

from mooc_stats_analyzer.tasks import task_names, id_from_order


class SubmissionEntry:
    def __init__(self, row):
        self.submission_id = row['submission_id']
        self.step_id = row['step_id']
        self.user_id = row['user_id']
        self.attempt_time = row['attempt_time']
        self.submission_time = row['submission_time']
        self.status = row['status']
        self.dataset = row['dataset']
        self.clue = row['clue']
        self.reply = row['reply']
        self.reply_clear = row['reply_clear']
        self.hint = row['hint']

    def time(self):
        return datetime.datetime.utcfromtimestamp(
            float(self.submission_time)).strftime('%Y-%m-%d %H:%M')

    @property
    def get_hint(self):
        return self.hint.split('\n')  # encode('utf-8')  # replace('\n', '\\n')

    @property
    def task_name(self):
        try:
            task_name = task_names[self.step_id]
        except KeyError:
            task_name = ''

        return task_name

    def __repr__(self):
        return '{}: #{} user={} \'{}\' {}'.format(self.time(),
                                                  self.submission_id,
                                                  self.user_id, self.task_name,
                                                  self.status.upper())


class SubmissionManager:
    def __init__(self, submissions):
        self.submissions = submissions

    def sub_count(self):
        return len(self.submissions)

    @property
    def unique_users(self):
        users = [x.user_id for x in self.submissions]
        return set(users)

    def tasks(self):
        return set([x.step_id for x in self.submissions])

    def subs_user(self, user_id):
        return [x for x in self.submissions if x.user_id == user_id]

    def users_attempted_task(self, task_id):
        return set(
            [x.user_id for x in self.submissions if x.step_id == task_id])

    def subs_task(self, task_id):
        return [x for x in self.submissions if x.step_id == task_id]

    def subs_user_task(self, user_id, task_id):
        return [x for x in self.submissions if
                x.step_id == task_id and x.user_id == user_id]

    def tasks_user(self, user_id):
        return set([x.step_id for x in self.subs_user(user_id)])

    def last_task_user(self, user_id):
        orderded_tasks = []
        for x in self.tasks_user(user_id):
            try:
                orderded_tasks.append(task_names[x])
            except KeyError:
                pass
        orderded_tasks = sorted(orderded_tasks, key=lambda t: t[0],
                                reverse=True)

        return orderded_tasks[0]

    def last_task_count(self, task_order):
        count = 0
        for user in self.unique_users:
            if self.last_task_user(user)[0] == task_order:
                count += 1

        return count

    def dropout(self):
        dropout = []
        for n in [x[0] for x in task_names.values()]:
            dropout.append(self.last_task_count(n))

        return dropout

    def succ_fail(self, task_order):
        task_id = id_from_order(task_order)
        succ = [x for x in self.submissions if
                x.step_id == task_id and x.status == 'correct']
        fail = [x for x in self.submissions if
                x.step_id == task_id and x.status == 'wrong']

        return len(succ), len(fail)

    def n_of_subs(self, task_order):
        succ, fail = self.succ_fail(task_order)
        return succ + fail
