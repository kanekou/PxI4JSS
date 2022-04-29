from collections import defaultdict
import neal
from .utils import simulator as simulator_utils
import itertools
from pyqubo import Array, Placeholder, Constraint, SubH
from snakes.nets import *
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")

def main(petrinet, feed_dict={'A': 1.0, 'B': 1.0, 'C': 1.0}):
    # NOTE: If you put 0 in a feed_dict, it won't be able to judge correctly.
    if not (feed_dict['A'] and feed_dict['B'] and feed_dict['C']):
        print('incorrent feed_dict')
        exit(1)

    solution_dict = {}
    start_time, end_time, feasible_solution, subH, bs_log = binary_search(petrinet, feed_dict)

    if feasible_solution:
        solution_dict = simulator_utils.format_solution_to_2Ddict(feasible_solution.sample)

    sorted_solution = sorted(solution_dict.items(), key=lambda x: x[0])
    return {'solution': {'start_time': start_time, 'end_time': end_time, 'energy': sum(subH.values()), 'spins': sorted_solution,
            'subH': { 'H_prece': subH['H_precedence'], 'H_conflict': subH['H_conflict'], 'H_firing': subH['H_firing']}},
            'topology': {'jobs': petrinet.jobs,
                         'processing_times': petrinet.pt,
                         'resources_by_trans': dict(petrinet.resources_trans_map),
                         'num_var': len(petrinet.preplaces_trans_map(resource=False)) * (sum(petrinet.pt.values()) - min(petrinet.pt.values()))
                         },
            'bs_log': bs_log,
            'mode': 'simulator'
            }


def binary_search(n, feed_dict):
    t_num = len(n.preplaces_trans_map(resource=False))
    a = Placeholder("A")
    b = Placeholder("B")
    c = Placeholder("C")
    machine_num = len(n.trans_resource_map)
    # Divide the sum of all task lengths by the number of fastest machines.
    earliest_time = sum(n.pt.values()) // machine_num
    # (The sum of all task lengths executed on the fastest machine) - (the smallest pt)
    latest_time = sum(n.pt.values()) - min(n.pt.values())
    feasible_solution = []
    feasible_subH = defaultdict(int)
    bs_cnt = 0
    bs_log = {}
    bs_log.setdefault('total_cnt', 0)
    bs_log.setdefault('cnt', {})

    while earliest_time <= latest_time:
        mid_time = (earliest_time + latest_time) // 2
        x = Array.create('x', (t_num, mid_time), 'BINARY')
        H_precedence = set_precedence(n, x, mid_time)
        H_conflict = set_conflict(n, x, mid_time)
        H_firing = set_firing(t_num, x, mid_time)
        H = SubH(a * H_precedence, 'H_precedence') + SubH(b * H_conflict, 'H_conflict') + SubH(c * H_firing, 'H_firing')
        model = H.compile()
        bqm = model.to_bqm(feed_dict=feed_dict)
        sampler = neal.SimulatedAnnealingSampler()
        sampleset = sampler.sample(bqm)
        decoded_samples = model.decode_sampleset(sampleset, feed_dict=feed_dict)
        decoded_solution = min(decoded_samples, key=lambda x: x.energy)
        broken = False if decoded_solution.energy == 0 else True

        if not broken:
            latest_time = mid_time - 1
            feasible_solution = decoded_solution
        else:
            earliest_time = mid_time + 1

        bs_log['cnt'].setdefault(bs_cnt, {'using_var_num': t_num * mid_time})
        bs_cnt += 1

    bs_log['total_cnt'] = bs_cnt

    # No existng feasible solution
    if not feasible_solution:
        return (-1, -1, [], {'H_precedence': decoded_solution.subh['H_precedence'],
                             'H_conflict': decoded_solution.subh['H_conflict'],
                             'H_firing': decoded_solution.subh['H_firing']},
                             bs_log
                )

    feasible_subH = {'H_precedence': feasible_solution.subh['H_precedence'],
                     'H_conflict': feasible_solution.subh['H_conflict'],
                     'H_firing': feasible_solution.subh['H_firing']}
    start_time, end_time = simulator_utils.calculate_processing_time(earliest_time, feasible_solution.sample, n.pt)

    return start_time, end_time, feasible_solution, feasible_subH, bs_log


def set_firing(t_num, x, time):
    H_firing = 0.0
    for i in range(t_num):
        H_firing += Constraint((1-sum(x[i, j] for j in range(time)))
                               ** 2, label=f"one_fired_t{i}", condition=lambda x: x == 0.0)
    return H_firing


def set_precedence(n, x, time):
    H_precedence = 0.0
    for j in range(time):
        for trans in n.preplaces_trans_map(resource=False):
            # Putting precedence constraints based on pre transition and post transition
            pre_t = int(re.sub("\\D", "", trans))

            if not(trans in n.postplaces_trans_map(resource=False)):
                continue

            post_p = n.postplaces_trans_map(resource=False)[trans]
            if not(post_p in n.posttrans_place_map):
                continue

            post_t = int(re.sub("\\D", "", n.posttrans_place_map[post_p]))
            for nj in range(time):
                if (j + n.pt[f"t{pre_t}"] > nj):
                    H_precedence += Constraint(x[pre_t, j] * x[post_t, nj],
                                               label=f"adjacent(t{pre_t},t{post_t})", condition=lambda x: x == 0.0)
    return H_precedence


def set_conflict(n, x, time):
    H_conflict = 0.0
    H_conflict_dict = defaultdict(int)
    pair = []
    for value in n.trans_resource_map.values():
        value = list(value)
        pair.append(list(itertools.combinations(value, 2)))

    for i, k in list(itertools.chain.from_iterable(pair)):
        i = int(re.sub("\\D", "", i))
        k = int(re.sub("\\D", "", k))

        for t in range(time):
            for nt in range(t, time):
                if (t + n.pt[f"t{i}"] > nt and n.pt[f"t{k}"] > 0):
                    H_conflict += Constraint(x[i, t] * x[k, nt],
                                             label=f"one_job_t{i}_and_t{k}")
                    H_conflict_dict[f"{k}{nt}{i}{t}"] = 1

                if ((t + n.pt[f"t{k}"] > nt) and ((f"{k}{t}{i}{nt}" in H_conflict_dict) == False and n.pt[f"t{i}"] > 0)):
                    H_conflict += Constraint(x[k, t] * x[i, nt],
                                             label=f"one_job_t{k}_and_t{i}", condition=lambda x: x == 0.0)
    return H_conflict
