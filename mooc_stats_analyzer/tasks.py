task_names = {
    '199469': (1, 'kernel_module_1_load'),
    '199468': (2, 'kernel2_call_another'),
    '200832': (3, 'kernel3_kobjects'),
    '200833': (4, 'kernel_params'),
    '201083': (5, 'kernel_fops'),
    '202442': (6, 'kernel_cdev_private'),
    '202444': (7, 'kernel_dynamic_node'),
    '205014': (8, 'kernel_linked_lists'),
    '205015': (9, 'kernel_ioctl'),
    # '226086': (9, 'kernel_interrupts'),
    # '231089': (10, ''),
}


def id_from_order(order):
    for key in task_names:
        if task_names[key][0] == order:
            return key


def name_from_order(task_order):
    task_id = id_from_order(task_order)

    return task_names[task_id][1]


def orders():
    orders_list = []
    for key in task_names:
        orders_list.append(task_names[key][0])

    return orders_list
