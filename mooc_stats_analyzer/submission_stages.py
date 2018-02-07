from mooc_stats_analyzer.submissions import SubmissionManager
from mooc_stats_analyzer.tasks import id_from_order, name_from_order


def stage_parser_by_order(task_order):
    if task_order == 1:
        return HelloStages
    if task_order == 2:
        return CallAnotherStages
    if task_order == 3:
        return KObjectsStages
    if task_order == 4:
        return ParamsStages
    if task_order == 5:
        return FOpsStages
    if task_order == 6:
        return CDevStages
    if task_order == 7:
        return DynamicNodeStages
    if task_order == 8:
        return LinkedLists
    if task_order == 9:
        return IOCtl


def stages_for_all(subs, task_order):
    print('\n{} all submissions'.format(name_from_order(task_order)))

    task_subs = subs.subs_task(id_from_order(task_order))
    task_sm = SubmissionManager(task_subs)
    stages = stage_parser_by_order(task_order)()
    task_stages = stages.all_stages(task_subs)

    print('Total: {} submissions, {} users'.format(len(task_subs), len(task_sm.unique_users)))
    stage_n = 0
    for stage in task_stages:
        percents = 100 / len(task_subs) * stage[1]
        print('Stage {}: {} ({:.2f}%) submissions passed \'{}\''.format(stage_n, stage[1], percents, stage[0]))
        stage_n += 1


def stages_for_best(subs, task_order):
    print('\n{} best submissions per user'.format(name_from_order(task_order)))

    task_subs = subs.subs_task(id_from_order(task_order))
    task_sm = SubmissionManager(task_subs)
    stages = stage_parser_by_order(task_order)()
    best_by_user = []
    for user in task_sm.unique_users:
        best_by_user.append(stages.best_sub_user(task_subs, user))
    task_best_stages = stages.all_stages(best_by_user)

    print('Total: {} submissions, {} users'.format(len(best_by_user), len(task_sm.unique_users)))
    stage_n = 0
    for stage in task_best_stages:
        percents = 100 / len(best_by_user) * stage[1]
        print('Stage {}: {} ({:.2f}%) submissions passed \'{}\''.format(stage_n, stage[1], percents, stage[0]))
        stage_n += 1


class TaskStage:
    def __init__(self):
        self.stages = {
            1: 'Compilation log',
            2: 'Solution compiled successfuly.',
        }

        self.stage_desc = {
            1: 'Solution uploaded correctly',
            2: 'Solution compiled successfully',
        }

    def last_stage(self):
        return max(self.range_stages())

    def range_stages(self):
        return sorted(self.stages.keys())

    def sub_passed_stage(self, sub, stage_number):
        if stage_number == 1:
            if self.stages[stage_number] in sub.hint:
                return True

            return False

        if self.sub_passed_stage(sub, stage_number - 1):
            if self.stages[stage_number] in sub.hint:
                return True

        return False

    def best_stage(self, sub):
        for stage_number in reversed(self.range_stages()):
            if self.sub_passed_stage(sub, stage_number):
                return stage_number

        return -1

    def n_sub_passed_stage(self, subs, stage_number):
        passed = 0
        for sub in subs:
            if self.sub_passed_stage(sub, stage_number):
                passed += 1

        return passed

    def all_stages(self, subs):
        stages = []
        for stage in self.stages:
            n_passed = self.n_sub_passed_stage(subs, stage)
            desc = self.stage_desc[stage]
            stages.append((desc, n_passed))

        return stages

    def best_sub(self, subs):
        best = subs[0]
        for sub in subs:
            if self.best_stage(sub) > self.best_stage(best):
                best = sub

        return best

    def best_sub_user(self, subs, user_id):
        subs = [x for x in subs if x.user_id == user_id]

        return self.best_sub(subs)

    @staticmethod
    def print_stages(stages):
        stage_n = 0
        for stage in stages:
            print('Stage {}: {} submissions passed \'{}\''.format(stage_n, stage[1], stage[0]))
            stage_n += 1


class HelloStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'Module was successfully loaded'
        self.stages[4] = 'Module was successfully removed'
        self.stage_desc[3] = 'Module was successfully loaded'
        self.stage_desc[4] = 'Module was successfully removed'


class CallAnotherStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'Execution log: solution.ko was loaded successfuly!'
        self.stages[4] = 'Function was called'

        self.stage_desc[3] = 'Execution log: solution.ko was loaded successfuly!'
        self.stage_desc[4] = 'Function was called'


class KObjectsStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'Execution log: solution.ko was loaded successfuly!'
        self.stages[4] = 'Correct.'

        self.stage_desc[3] = 'Execution log: solution.ko was loaded successfully!'
        self.stage_desc[4] = 'Kobject returned valid number of cats.'


class ParamsStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'Execution log: solution.ko was loaded successfuly!'
        self.stages[4] = 'Correct.'

        self.stage_desc[3] = 'Execution log: solution.ko was loaded successfully!'
        self.stage_desc[4] = 'The sum was calculated correctly.'


class FOpsStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'Execution log: solution.ko was loaded successfuly!'
        self.stages[4] = 'Success!'

        self.stage_desc[3] = 'Execution log: solution.ko was loaded successfully!'
        self.stage_desc[4] = 'Read and write operations produced correct result.'


class CDevStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'solution.ko was loaded successfuly!'
        self.stages[4] = 'Testing that first read returns valid sid'
        self.stages[5] = 'Testing simutanious writes and reads'
        self.stages[6] = 'Success!'

        self.stage_desc[3] = 'Module was loaded without errors'
        self.stage_desc[4] = 'Device file opened successfully'
        self.stage_desc[5] = 'First read returned valid sid'
        self.stage_desc[6] = 'All writes and reads worked correctly'


class DynamicNodeStages(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'solution.ko was loaded successfuly!'
        self.stages[4] = 'Device gives valid major number during reading'
        self.stages[5] = 'Success!'

        self.stage_desc[3] = 'Module was loaded without errors'
        self.stage_desc[4] = self.stages[4]
        self.stage_desc[5] = 'Device was removed properly by driver during unloading.'


class LinkedLists(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'solution.ko was loaded successfuly!'
        self.stages[4] = 'Correct result!'

        self.stage_desc[3] = 'Module was loaded without errors'
        self.stage_desc[4] = 'List was read correctly'


class IOCtl(TaskStage):
    def __init__(self):
        super().__init__()
        self.stages[3] = 'solution.ko was loaded successfuly!'
        self.stages[4] = 'Success!'

        self.stage_desc[3] = 'Module was loaded without errors'
        self.stage_desc[4] = 'All checks passed successfully!'
