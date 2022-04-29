import unittest
from pyqubo import Array, Placeholder
from snakes.nets import *
from pxi4jss import main as pxi4jss

class TestMain(unittest.TestCase):
    def setUp(self):
        snakes_net = self.init_petrinet()
        self.res = pxi4jss(snakes_net)

    def init_petrinet(self):
        n = PetriNet('Job Shop Scheduling')
        n.add_place(Place('p0', [1]))
        n.add_place(Place('p1'))
        n.add_place(Place('p2'))
        n.add_place(Place('p3'))
        n.add_place(Place('p4'))
        n.add_place(Place('p5', [1]))
        n.add_place(Place('p6'))
        n.add_place(Place('p7'))
        n.add_place(Place('p8'))
        n.add_place(Place('p9'))
        n.add_place(Place('p10', [1]))
        n.add_place(Place('p11'))
        n.add_place(Place('p12'))
        n.add_place(Place('p13'))
        n.add_place(Place('p14'))

        n.add_place(Place('m0'))
        n.add_place(Place('m1'))
        n.add_place(Place('m2'))

        pt = {'t1': '1',
              't2': '1',
              't3': '2',
              't0': '2',
              't4': '1',
              't6': '2',
              't7': '1',
              't5': '3',
              't8': '2',
              't9': '3',
              't10': '2',
              't11': '2'}

        t_num = 12  # Number of operations
        for i in range(t_num):
            t_name = f't{i}'
            t_pt = pt[t_name]
            n.add_transition(Transition(t_name, Expression(t_pt)))

        start = 0
        end = per_p = 4
        job_num = 3
        for j in range(job_num):
            for i in range(start, end):
                n.add_input('p{}'.format(i+j), 't{}'.format(i), Variable('x'))
                n.add_output('p{}'.format(i+j+1),
                             't{}'.format(i), Variable('x'))

            start = end
            end += per_p

        # Machines
        m_dict = {'m1': {'t2', 't5', 't6', 't1'},
                  'm2': {'t7', 't3', 't11', 't10'},
                  'm0': {'t8', 't9', 't4', 't0'}}
        for m, t in m_dict.items():
            for e in t:
                n.add_input(m, e, Variable('x'))
                n.add_output(m, e, Variable('x'))

        return n

    def test_starttime_is_greater_than(self):
        if self.res['solution']['energy'] == 0:
            self.assertTrue(self.res['solution']['start_time'] >= 11 )

    def test_endtime_is_greater_than(self):
        if self.res['solution']['energy'] == 0:
            self.assertTrue(self.res['solution']['end_time'] >= 13 )

    def test_calc_energy_of_subH(self):
        if self.res['solution']['energy'] == 0:
            subH = self.res['solution']['subH']
            self.assertEqual(subH['H_conflict'], 0.0)
            self.assertEqual(subH['H_prece'], 0.0)
            self.assertEqual(subH['H_firing'], 0.0)

    def test_extract_pt(self):
        if self.res['solution']['energy'] == 0:
            expected = {'t1': 1,
                        't2': 1,
                        't3': 2,
                        't0': 2,
                        't4': 1,
                        't6': 2,
                        't7': 1,
                        't5': 3,
                        't8': 2,
                        't9': 3,
                        't10': 2,
                        't11': 2}

            self.assertEqual(self.res['topology']['processing_times'], expected)

    def test_extract_resources_by_trans(self):
        if self.res['solution']['energy'] == 0:
            expected = {'t0': {'m0'}, 't1': {'m1'}, 't2': {'m1'}, 't3': {'m2'}, 't4': {'m0'}, 't5': {
                'm1'}, 't6': {'m1'}, 't7': {'m2'}, 't8': {'m0'}, 't9': {'m0'}, 't10': {'m2'}, 't11': {'m2'}}

            self.assertEqual(self.res['topology']['resources_by_trans'], expected)

    def test_calc_num_of_var(self):
        expected = 252
        self.assertEqual(self.res['topology']['num_var'], expected)

    def test_extract_jobs(self):
        expected = {0: ['t0', 't1', 't2', 't3'],
                    1: ['t4', 't5', 't6', 't7'],
                    2: ['t8', 't9', 't10', 't11']}

        actual = self.res['topology']['jobs']
        self.assertTrue(self.assert_equal_jobs(expected, actual))

    # Without considering the order of the keys
    def assert_equal_jobs(self, jobs, jobs2):
        def subtract_list(lst1, lst2):
            lst = lst1.copy()
            for element in lst2:
                try:
                    lst.remove(element)
                except ValueError:
                    return False
            if not lst:
                return True
            return False

        jobs_values = list(jobs.values())
        jobs2_values = list(jobs2.values())
        if not (subtract_list(jobs_values, jobs2_values) or subtract_list(jobs2_values, jobs_values)):
            return False

        return True

if __name__ == "__main__":
    unittest.main()
